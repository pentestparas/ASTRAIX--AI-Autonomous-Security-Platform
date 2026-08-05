# Supply Chain Attacks → Dependency Confusion & Malicious Libraries Attacks

## Hijacking Internal Package via Typo Match

- **Attack Type**: Dependency Confusion
- **Target**: Developer Environment
- **Vulnerability**: Typosquatting Internal Dependency
- **MITRE**: T1195.002
- **Impact**: Credential or code leak from developer environment
- **Tools**: PyPI, Python
- **Scenario**: An attacker publishes a package with a slightly misspelled name of an internal dependency (e.g., internl-utils instead of internal-utils) hoping a developer mistypes it.
- **Attack Steps**: 1. Attacker identifies an internal package used inside the target organization’s codebase (e.g., internal-utils).2. Attacker creates a malicious package named with a common typo (internl-utils) containing a payload (e.g., exfiltrate .git/config).3. They publish it to a public registry like PyPI.4. A developer mistakenly types the wrong name in requirements.txt or during pip install.5. The malicious package is installed.6. Once the code runs, it sends out sensitive data from the developer’s environment to the attacker's server.
- **Detection**: Monitor unusual traffic from dev systems, scan typosquatted packages
- **Solution**: Validate all dependency names; use internal mirrors
- **Tags**: typosquatting, dependency attack, internal repo

## Dependency Confusion in GitHub Actions Workflow

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipeline
- **Vulnerability**: Misconfigured Registry Precedence
- **MITRE**: T1195.002
- **Impact**: CI/CD credential theft, supply chain poisoning
- **Tools**: GitHub, npm
- **Scenario**: The attacker exploits public availability of GitHub Actions YAML to infer internal dependency names used during CI builds and publishes malicious versions on a public registry.
- **Attack Steps**: 1. Attacker browses a public GitHub repo that contains .github/workflows/build.yml.2. They observe private dependencies like mycompany-utils being used.3. They publish a public version of mycompany-utils with the same version number.4. GitHub Actions may fetch the public one if registry priority is misconfigured.5. Malicious code executes during CI build — can steal secrets or modify artifacts.6. Attacker receives CI environment variables or secrets through exfiltration.
- **Detection**: Check logs for unexpected external package resolution
- **Solution**: Enforce private registry priority in CI
- **Tags**: github-actions, ci-cd, devsecops

## Compromised Maintainer Account Pushes Malicious Update

- **Attack Type**: Malicious Libraries
- **Target**: Application Servers
- **Vulnerability**: Maintainer Account Takeover
- **MITRE**: T1556.001
- **Impact**: Widespread secret leaks or RCE
- **Tools**: npm, Node.js
- **Scenario**: An attacker gains access to a legitimate maintainer’s account of a popular open-source library and injects malicious code in a new release.
- **Attack Steps**: 1. Attacker obtains credentials via phishing or credential reuse of a known maintainer.2. They log into the npm account and push version 2.3.5 of a widely used package (e.g., express-helper).3. The update contains obfuscated code to steal environment variables and send them to a remote server.4. Developers globally begin installing this update via npm install.5. When apps are deployed, malicious code runs silently on prod systems.6. Attacker collects secrets, tokens, or credentials from hundreds of apps.
- **Detection**: Sudden spike in package download behavior, unexpected network calls
- **Solution**: MFA on maintainer accounts, signed releases
- **Tags**: maintainer compromise, malicious update

## Confusing Versioning to Trick Build Tools

- **Attack Type**: Dependency Confusion
- **Target**: DevOps Pipeline
- **Vulnerability**: Semver Resolution Abuse
- **MITRE**: T1195.002
- **Impact**: Build environment compromise
- **Tools**: npm, semver
- **Scenario**: Attacker exploits the way semver is resolved by publishing version numbers that sort higher, e.g., 1.0.0-alpha.9999.
- **Attack Steps**: 1. Attacker sees internal dependency my-lib@1.0.0 used in private builds.2. They publish a package with the same name and version 1.0.0-alpha.9999.3. Some tools, depending on how version precedence is calculated, may resolve this version as newer.4. During build or npm update, this version may be pulled in.5. Malicious package payload exfiltrates .env, .ssh, or AWS credentials.6. Attacker gains unauthorized access to the internal cloud resources.
- **Detection**: Version anomaly detection tools (e.g., Renovate alerts)
- **Solution**: Pin versions and audit unexpected updates
- **Tags**: versioning abuse, semver tricks

## Shadowing Scoped Internal Package

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD & Dev Workstations
- **Vulnerability**: Registry Fallback Misuse
- **MITRE**: T1195.002
- **Impact**: Unintentional installation of shadow package
- **Tools**: npm
- **Scenario**: Attacker creates a public version of a private scoped package like @org/internal-lib by dropping the scope, tricking the registry resolution logic.
- **Attack Steps**: 1. Target org uses scoped packages like @org/internal-lib which exist only in private registries.2. Attacker creates and publishes internal-lib on public npm with matching interface.3. Due to misconfigured fallback rules in .npmrc, public version may resolve first.4. During build, public package is installed.5. Malicious logic in the package executes, exfiltrating secrets.6. CI or prod system gets compromised without anyone noticing during a patch update.
- **Detection**: Registry logs and DNS logs showing external fetches
- **Solution**: Lock dependency to private scope; disable fallback
- **Tags**: scoped package, shadowing, npmrc flaw

## Fake Popular Package With Extra Hyphen

- **Attack Type**: Typosquatting
- **Target**: Developers
- **Vulnerability**: Hyphenation Typosquatting
- **MITRE**: T1555.003
- **Impact**: Developer secrets stolen silently
- **Tools**: npm
- **Scenario**: Attacker mimics a popular package by publishing a similar name with a hyphen added (e.g., react-router-dom vs react--router-dom).
- **Attack Steps**: 1. Attacker notes popular npm package name (e.g., react-router-dom).2. They publish react--router-dom (with double hyphen), mimicking documentation and keywords.3. Developers may accidentally install it via typo in package.json.4. Package executes code during postinstall to steal SSH keys or config.5. Exfiltrated data reaches attacker server.6. Attack may remain undetected unless reviewed manually.
- **Detection**: Monitor npm audit and analyze package metadata
- **Solution**: Use IDE auto-complete; avoid manual entry of packages
- **Tags**: typosquatting, npm security

## Publishing Python Package With Same Name in PyPI

- **Attack Type**: Dependency Confusion
- **Target**: Python Developer Machines
- **Vulnerability**: Unclaimed PyPI Package Name
- **MITRE**: T1195.002
- **Impact**: Unauthorized access via dev machines
- **Tools**: PyPI
- **Scenario**: A malicious actor notices that a Python package used internally is not published on PyPI and decides to publish it there with a backdoor.
- **Attack Steps**: 1. Attacker gains access to internal requirements (e.g., via leaked GitHub repo or Dockerfile).2. They find a private library inhouse-tools.3. They publish inhouse-tools==1.0.0 to PyPI.4. A developer without registry segregation installs it assuming it’s legit.5. Code runs backdoor that sends environment variables and API tokens to attacker.6. They gain further access into internal systems.
- **Detection**: Watch install sources, hash-verify packages
- **Solution**: Always check package authorship and source
- **Tags**: python, pypi attack, dependency confusion

## Code Obfuscation in Dependency

- **Attack Type**: Malicious Libraries
- **Target**: Any Dev Environment
- **Vulnerability**: Code Obfuscation in Libraries
- **MITRE**: T1027
- **Impact**: Reverse shell or token exfiltration
- **Tools**: JavaScript, obfuscator.io
- **Scenario**: Attacker uses obfuscation and innocent-looking code (e.g., base64 payloads) to hide malicious behavior in a published library.
- **Attack Steps**: 1. Attacker publishes a library that performs a simple utility task (e.g., color converter).2. Inside, they include base64-encoded strings which decode into a malicious script.3. Obfuscated loader decrypts and executes the payload upon import.4. Once imported, it creates reverse shell or grabs tokens.5. Behavior is stealthy and bypasses static analysis tools.6. The package gains traction due to good README and star count.
- **Detection**: Runtime sandboxing, de-obfuscation tools
- **Solution**: Perform deep inspection before adoption
- **Tags**: obfuscation, evasion, javascript

## Dependency Confusion from Public Docker Image

- **Attack Type**: Dependency Confusion
- **Target**: Containerized Applications
- **Vulnerability**: Public Dockerfile with Unclaimed Packages
- **MITRE**: T1195.002
- **Impact**: Compromised container image
- **Tools**: Docker, PyPI
- **Scenario**: Dockerfiles referencing internal dependencies in pip install get exploited by attackers who publish those names publicly.
- **Attack Steps**: 1. A public Dockerfile in GitHub shows RUN pip install internal-client.2. Attacker notices the dependency doesn’t exist on PyPI.3. They publish internal-client with a payload.4. Any user building that Docker image installs the malicious version.5. The image gets built and distributed with a backdoor.6. Downstream consumers now unknowingly run compromised images.
- **Detection**: Monitor package install logs, verify image layers
- **Solution**: Host internal registry, audit Dockerfiles
- **Tags**: docker, pip, public image abuse

## Trick Package Reviewers with Fake Tests

- **Attack Type**: Malicious Libraries
- **Target**: Security Review Team
- **Vulnerability**: Social Engineering via Good Docs
- **MITRE**: T1204.002
- **Impact**: Whitelisting malicious package
- **Tools**: Jest, Mocha, README.md
- **Scenario**: Attacker includes legitimate-looking unit tests and documentation to deceive reviewers into trusting a malicious library.
- **Attack Steps**: 1. Attacker builds a malicious package with backdoor payload.2. They add high-quality unit tests that all pass.3. README shows clear API usage, badges, and docs.4. It looks legitimate to security reviewers or automated scanners.5. Upon import, the payload activates — e.g., sends home directory files.6. Organization unknowingly whitelists the package.
- **Detection**: Static code analysis, verify network calls
- **Solution**: Don’t trust test quality alone, inspect behavior
- **Tags**: social engineering, code trust, review deception

## Private Scoped Package Name Clash

- **Attack Type**: Dependency Confusion
- **Target**: CI/CD Pipeline
- **Vulnerability**: Registry precedence misconfiguration
- **MITRE**: T1195.002
- **Impact**: CI secrets leak, attacker foothold in internal infra
- **Tools**: npm, MITMproxy
- **Scenario**: A developer publishes a public package with the same name as a scoped internal package used by an enterprise CI pipeline.
- **Attack Steps**: 1. The attacker identifies a private scoped npm package used internally (e.g., @corp/utils) through GitHub leaks or internal code shared in forums.2. They publish a public package using the same name, exploiting cases where registries don’t properly isolate scopes.3. The enterprise's CI/CD misconfigures .npmrc to default to the public registry.4. When the pipeline installs dependencies, it unknowingly fetches the attacker’s version.5. A malicious preinstall script exfiltrates CI credentials, environment variables, or IAM tokens from the build runner.6. Attacker uses these to pivot into internal systems.
- **Detection**: Monitor source registry of packages during install
- **Solution**: Use strict .npmrc scoping rules and internal registry enforcement
- **Tags**: #npm #ScopedPackages #CI/CD #SupplyChain

## Hijacking Abandoned Namespace on Python Package Index

- **Attack Type**: Malicious Libraries
- **Target**: Internal CI Systems
- **Vulnerability**: Namespace reuse due to unmaintained packages
- **MITRE**: T1195.002
- **Impact**: Developer and pipeline compromise
- **Tools**: PyPI, pip, whois
- **Scenario**: The attacker takes over an abandoned PyPI package namespace once used by an internal team and reuses the name to deliver malware.
- **Attack Steps**: 1. Attacker monitors for removed or abandoned PyPI projects by tracking names with no updates, issues, or ownership activity for years.2. Registers a long-unused package name (e.g., internal_utils) once used in internal tooling.3. Publishes a package with identical function names and metadata but embeds obfuscated backdoor code inside utility functions.4. A developer reuses the old dependency in requirements.txt without realizing it points to the new, malicious version.5. The CI pulls the attacker’s package, and embedded code silently runs post-install, leaking AWS/GCP tokens or SSH keys.
- **Detection**: Watch for unknown authors or sudden reappearing packages
- **Solution**: Maintain internal mirrors of critical packages and auto-reserve historical project names
- **Tags**: #PyPI #Abandonware #MaliciousCode #InternalReuse

## Typosquatting Critical SDK in Infra-as-Code

- **Attack Type**: Malicious Libraries
- **Target**: Infrastructure Automation
- **Vulnerability**: Developer typos + misleading metadata
- **MITRE**: T1195.002
- **Impact**: Cloud credential theft through IaC
- **Tools**: Terraform, pip, VirusTotal
- **Scenario**: Attacker typosquats a critical SDK like aws-sdk-core by publishing aws_sdk-core, which gets mistakenly used in Terraform automation scripts.
- **Attack Steps**: 1. Attacker identifies commonly used SDKs in IaC tools like aws-sdk-core or gcp-auth.2. Crafts similarly named typosquats such as aws_sdk-core and pushes them to PyPI or npm with a similar project description.3. Malicious package includes a setup.py or install script that silently leaks AWS access keys via HTTP requests to attacker-controlled servers.4. A developer mistypes the dependency name in IaC or Terraform module and unknowingly pulls the attacker’s version.5. During pipeline execution, secrets are exfiltrated and attacker gains cloud access.
- **Detection**: Analyze dependency typo patterns and track external calls
- **Solution**: Implement allow-lists and dependency typo detection tools
- **Tags**: #Typosquatting #IaC #Cloud #Python

## Injected Dependency in Submodule via GitHub Action

- **Attack Type**: Dependency Confusion
- **Target**: GitHub CI
- **Vulnerability**: Unverified third-party forks in CI scripts
- **MITRE**: T1195.002
- **Impact**: Secrets exfiltration from GitHub runners
- **Tools**: GitHub Actions, git-submodule
- **Scenario**: A GitHub Action references a submodule that includes a dependency injected by an attacker via a poisoned fork.
- **Attack Steps**: 1. A GitHub Action pipeline references a public repository forked from a trusted one (e.g., for a utility library).2. Attacker modifies the requirements.txt inside the fork to include a malicious package (internal-lib-fix).3. This package is published to PyPI, containing post-install scripts that dump secrets from environment variables.4. The main GitHub Action executes this submodule without validating the dependency.5. Upon execution, the poisoned dependency installs and exfiltrates tokens.6. Attacker uses these to further compromise workflows.
- **Detection**: Monitor indirect dependencies from forks in actions
- **Solution**: Pin dependencies explicitly and verify upstream forks before use
- **Tags**: #GitHubActions #Submodules #CI #MaliciousLibraries

## Dependency Confusion via npm Install Fallback

- **Attack Type**: Dependency Confusion
- **Target**: Internal Dev Pipelines
- **Vulnerability**: npm registry fallback misconfiguration
- **MITRE**: T1195.002
- **Impact**: Source code or secrets exposure via install fallback
- **Tools**: npm, Burp Suite
- **Scenario**: An attacker publishes a package with the same name as an internal dependency. Due to fallback behavior, npm fetches it from the public registry.
- **Attack Steps**: 1. Attacker finds a package name like corp-utils mentioned in internal docs or Dockerfiles.2. Publishes a public version of corp-utils on npm.3. If the enterprise registry fails or isn't properly enforced via .npmrc, npm falls back to the public registry.4. CI/CD pipeline installing dependencies resolves it from npmjs.com instead of internal Artifactory.5. Malicious package installs with telemetry-stealing scripts or opens reverse shell to attacker IP.6. The attacker collects sensitive logs, credentials, or source code.
- **Detection**: Log registry URLs, monitor DNS lookups during install
- **Solution**: Disable fallback behavior, enforce scoped registry config
- **Tags**: #npm #CI/CD #RegistryFallback #DependencyHijack

## JavaScript Loader Misuse with Poisoned Transitive Lib

- **Attack Type**: Malicious Libraries
- **Target**: JavaScript Build Systems
- **Vulnerability**: Malicious code in transitive dependency
- **MITRE**: T1195.002
- **Impact**: Stealthy compromise during build
- **Tools**: Node.js, npm audit
- **Scenario**: An attacker publishes a JS utility library that is pulled as a transitive dependency and used with require() loaders.
- **Attack Steps**: 1. Attacker publishes a library like fast-path-helper that mimics a legitimate npm tool.2. It includes malicious logic triggered when imported via require().3. The attacker ensures this package is used by a popular framework or plugin indirectly (transitive dependency).4. A dev installs a main library (cool-framework) which pulls fast-path-helper.5. Upon CI build, the loader executes the hidden logic which modifies environment variables or opens a socket.6. Attacker receives CI runner info, tokens, or build logs.
- **Detection**: Monitor require() calls and package tree audit
- **Solution**: Use npm audit, lockfiles, and avoid unknown transitive libraries
- **Tags**: #npm #require #TransitiveDependencies #Malware

## Fake GitHub Repository with Poisoned Requirements.txt

- **Attack Type**: Malicious Libraries
- **Target**: Developer Workstations
- **Vulnerability**: Blind install from unverified GitHub sources
- **MITRE**: T1204.001
- **Impact**: Full developer environment takeover
- **Tools**: GitHub, PyPI, pip
- **Scenario**: An attacker creates a fake GitHub repo with popular project name and poisoned requirements.txt that installs malicious packages.
- **Attack Steps**: 1. Attacker forks a popular GitHub repo or creates a fake one with similar name (e.g., pytorch-utils-v2).2. Adds malicious packages like data-collector==1.0.0 in requirements.txt.3. Repo is SEO-optimized and linked on StackOverflow/forums.4. Developer clones the repo and blindly runs pip install -r requirements.txt.5. The malicious dependency runs post-install shell commands to upload .ssh and .aws folders.6. Attacker compromises developer’s environment.
- **Detection**: Alert on uncommon packages, inspect install logs
- **Solution**: Verify sources and hash-check requirements before install
- **Tags**: #GitHub #FakeRepos #requirements.txt #Malware

## Confusion via Docker + Malicious Layer with Dependency

- **Attack Type**: Dependency Confusion
- **Target**: Docker Build Systems
- **Vulnerability**: Untrusted Docker image includes malicious lib
- **MITRE**: T1203
- **Impact**: Container compromise + lateral movement
- **Tools**: Docker, DockerHub
- **Scenario**: Attacker builds a Docker image layer that installs a poisoned dependency with the same name as an internal-only package.
- **Attack Steps**: 1. Attacker builds a public Docker image that mimics a company image (e.g., corp/node-builder).2. Adds a malicious RUN npm install corp-internal-lib step.3. This lib is not available in public, so attacker creates and publishes it with hidden postinstall scripts.4. A user or script pulls the attacker’s DockerHub image by mistake.5. During container build or run, the poisoned dependency executes, stealing tokens or tampering with config files.6. Attacker gains remote access or credentials.
- **Detection**: Scan Dockerfiles + monitor image pull source
- **Solution**: Always verify image signatures and self-host trusted images
- **Tags**: #Docker #npm #DependencyConfusion #ContainerSecurity

## Scoped Package Typo Abuse in GitLab Runner

- **Attack Type**: Dependency Confusion
- **Target**: GitLab CI Pipelines
- **Vulnerability**: Typos in scoped package names
- **MITRE**: T1195.002
- **Impact**: Full CI runner abuse and access to artifacts
- **Tools**: GitLab CI, npm
- **Scenario**: Typo in GitLab CI pipeline config causes pull of a similarly named public npm package instead of internal scoped one.
- **Attack Steps**: 1. A GitLab CI config refers to @corp/toolkit-dev which is actually @corp/toolkit_dev.2. Attacker pre-registered the typo version (@corp/toolkit_dev) with a malicious script.3. When the pipeline executes npm install, it mistakenly pulls from the public registry.4. The install script exfiltrates GitLab runner tokens and env vars like CI_JOB_TOKEN or AWS_SECRET_ACCESS_KEY.5. Attacker reuses these tokens to run pipelines, inject further malicious jobs, or access sensitive repos.
- **Detection**: Detect unexpected registry pulls during build
- **Solution**: Validate all CI dependencies and lock scope usage strictly
- **Tags**: #GitLab #CI #npm #TypoAttack

## Malicious Release in a Forked Monorepo Package

- **Attack Type**: Malicious Libraries
- **Target**: JavaScript Developers
- **Vulnerability**: Trusting unofficial submodules as standalone libs
- **MITRE**: T1195.002
- **Impact**: Stealthy token leaks + shell injection
- **Tools**: Lerna, npm, git
- **Scenario**: Attacker forks a monorepo and injects malicious code into one of the sub-packages before publishing it as a standalone package.
- **Attack Steps**: 1. Attacker forks a monorepo project using tools like Lerna (managing multiple npm packages).2. Publishes one sub-package (e.g., lerna-utils-core) as a standalone package.3. Adds malicious code in that package’s lifecycle scripts or utility functions.4. The package is designed to look legitimate, even linking to the original GitHub project.5. Developers looking for specific modules install the standalone version from npm.6. Malicious code runs in dev environments or pipelines, stealing tokens and injecting shell commands.
- **Detection**: Scan package install scripts + monitor for suspicious forks
- **Solution**: Publish only signed modules and monitor registry usage trends
- **Tags**: #Lerna #Monorepo #npm #PackagePoisoning

## Malicious Release in a Forked Monorepo Package

- **Attack Type**: Malicious Libraries
- **Target**: JavaScript Developers
- **Vulnerability**: Trusting unofficial submodules as standalone libs
- **MITRE**: T1195.002
- **Impact**: Stealthy token leaks + shell injection
- **Tools**: Lerna, npm, git
- **Scenario**: Attacker forks a monorepo and injects malicious code into one of the sub-packages before publishing it as a standalone package.
- **Attack Steps**: 1. Attacker forks a monorepo project using tools like Lerna (managing multiple npm packages).2. Publishes one sub-package (e.g., lerna-utils-core) as a standalone package.3. Adds malicious code in that package’s lifecycle scripts or utility functions.4. The package is designed to look legitimate, even linking to the original GitHub project.5. Developers looking for specific modules install the standalone version from npm.6. Malicious code runs in dev environments or pipelines, stealing tokens and injecting shell commands.
- **Detection**: Scan package install scripts + monitor for suspicious forks
- **Solution**: Publish only signed modules and monitor registry usage trends
- **Tags**: #Lerna #Monorepo #npm #PackagePoisoning

