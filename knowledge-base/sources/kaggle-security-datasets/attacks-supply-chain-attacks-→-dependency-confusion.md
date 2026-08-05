# Supply Chain Attacks → Dependency Confusion Attacks

## Typosquatting Common PyPI Libs in Dev Containers

- **Attack Type**: Typosquatting
- **Target**: Dev Containers, CI/CD
- **Vulnerability**: Typosquatting + auto-builds
- **MITRE**: T1195.002 (Compromise Software Supply Chain)
- **Impact**: Credential theft, lateral movement
- **Tools**: PyPI, Docker Hub, pip
- **Scenario**: An attacker publishes a typo-variant of a popular PyPI package like requessts instead of requests, targeting developers using prebuilt Docker containers with pip installs.
- **Attack Steps**: 1. The attacker searches for typos in high-usage packages like numpy, requests, pandas.2. They publish malicious packages with typo'd names such as requessts to PyPI with backdoor code.3. A developer’s Dockerfile includes pip install requessts, unknowingly pulling in the attacker’s package.4. On container build, the package installs and executes code that collects environment secrets or sets up a reverse shell.5. The attacker gets access to container internals, including cloud API tokens and service credentials.6. This can propagate if the container is used in staging or production CI/CD pipelines.
- **Detection**: Monitor new PyPI package installs in containers
- **Solution**: Use pip hash pinning and validate dependency names
- **Tags**: devsecops, containers, typosquatting, pypi

## Injected Malicious Package via GitHub Actions Cache Poisoning

- **Attack Type**: Cache Poisoning
- **Target**: CI/CD (GitHub Actions)
- **Vulnerability**: Poisoned cache reuse
- **MITRE**: T1554 (Compromise Software Dependencies)
- **Impact**: Persistent malware in builds, exfiltration
- **Tools**: GitHub Actions, npm
- **Scenario**: A malicious package is injected by manipulating GitHub Actions’ caching mechanism, allowing compromised package versions to persist across workflows and be reused inadvertently.
- **Attack Steps**: 1. The attacker creates a PR to a public repo and uses custom Actions steps that poison the build cache with a malicious npm package version.2. GitHub Actions caches this version for performance.3. Maintainers unknowingly reuse the poisoned cache in future workflows.4. When they build/test, the malicious code is already present and may exfiltrate environment variables.5. Attackers may trigger builds via PRs or forks to observe stolen tokens in their controlled endpoints.6. The poisoned package stays persistent until cache keys or hashes are manually changed.7. This can affect dozens of downstream builds that rely on GitHub Actions.
- **Detection**: Monitor cache key integrity and use hash-locked deps
- **Solution**: Rotate GitHub Actions cache regularly; use scoped secrets
- **Tags**: github, ci/cd, caching, npm

## Malicious Scoped NPM Package Masquerading as Private Org Dependency

- **Attack Type**: Namespace Impersonation
- **Target**: Devs, CI environments
- **Vulnerability**: Misconfigured registry scoping
- **MITRE**: T1199 (Trusted Relationship Abuse)
- **Impact**: Secret leakage, internal package spoofing
- **Tools**: npm, npmrc, whoami, netcat
- **Scenario**: An attacker publishes a malicious NPM package with a scoped name like @org/utils that mimics private organization packages, exploiting misconfigured .npmrc files.
- **Attack Steps**: 1. The attacker identifies a target company using private packages under scope @org.2. They publish a public version of @org/utils to the global npm registry.3. Developers with misconfigured .npmrc (missing private registry settings) unintentionally fetch from the public source.4. During install, the attacker’s package executes a postinstall script that exfiltrates credentials via HTTP.5. Sensitive tokens and build secrets leak to attacker-controlled server.6. This affects local environments and CI/CD pipelines that reuse the same config.7. Detection is difficult unless proper registry scoping or auditing is enforced.
- **Detection**: Check package source registry in audit logs
- **Solution**: Enforce scoped registry rules and lock .npmrc config
- **Tags**: npm, private registry, ci/cd, internal repos

## Malicious Package with Postinstall Botnet Beacon

- **Attack Type**: Malicious Script
- **Target**: Developer endpoints
- **Vulnerability**: Postinstall script execution
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Remote access, botnet participation
- **Tools**: npm, Netcat, ncat, MITMf
- **Scenario**: A fake package is created that mimics leftpad2 and contains a postinstall script to ping a C2 server, enrolling the host into a botnet silently.
- **Attack Steps**: 1. The attacker publishes leftpad2 with similar metadata to the original leftpad.2. They insert a postinstall script in package.json that triggers a script to ping a C2 domain.3. A developer accidentally installs leftpad2, especially via unpinned dependencies.4. Upon install, the script executes and connects the machine to a botnet.5. From then, the attacker can send commands to this client system.6. The beacon remains silent until triggered, evading normal usage checks.7. The compromise may persist across updates due to dependency caching or bundling tools like Webpack.
- **Detection**: Monitor outbound C2 traffic after package install
- **Solution**: Block postinstall execution in dev environments
- **Tags**: npm, botnet, malware, postinstall

## Dependency Confusion in .NET Private NuGet Feeds

- **Attack Type**: Dependency Confusion
- **Target**: .NET Builds, CI/CD
- **Vulnerability**: Feed resolution order not prioritized
- **MITRE**: T1195.002 (Supply Chain Compromise)
- **Impact**: Internal code compromise, backdoors
- **Tools**: Visual Studio, NuGet CLI
- **Scenario**: Attackers upload public NuGet packages that match names from an enterprise's private NuGet feed, exploiting Visual Studio’s default resolution order.
- **Attack Steps**: 1. The attacker identifies internal NuGet package names via leaked .csproj files or internal docs.2. They publish public packages with those names on the public NuGet registry.3. Visual Studio or automated builds attempt to resolve packages and may pull from public registry first.4. If no priority is set for internal feeds, public malicious version is installed.5. The malicious package includes scripts that steal credentials or manipulate MSBuild logic.6. Upon build, the attacker gains access or plants persistent logic in the compiled output.7. This can silently poison releases or local developer builds.
- **Detection**: Audit NuGet source priority and package origin
- **Solution**: Set private feed as top priority and pin package versions
- **Tags**: nuget, dotnet, ci/cd, visualstudio

## Malware Injection via Yarn Plug'n'Play Shared Cache

- **Attack Type**: Cache Injection
- **Target**: Monorepos, internal developer envs
- **Vulnerability**: Shared PnP cache + write access
- **MITRE**: T1554 (Supply Chain Injection)
- **Impact**: Stealth malware across all workspaces
- **Tools**: Yarn, Node.js, PnP
- **Scenario**: An attacker targets shared Yarn Plug'n'Play (PnP) caches in monorepo setups, inserting malware that persists in .pnp.cjs files used by all downstream modules.
- **Attack Steps**: 1. The attacker commits to a shared monorepo where Yarn PnP is used for dependency management.2. They inject a malicious dependency into the .pnp.cjs file or lockfile.3. All dependent workspaces resolve packages through this shared graph.4. When another developer runs yarn install, the malicious dependency is auto-injected.5. The malware activates on build or test steps and exfiltrates secrets.6. Due to the lack of node_modules, traditional audit tools may miss the malware.7. The issue spreads rapidly across internal projects sharing the same PnP context.
- **Detection**: Monitor .pnp.cjs diffs and validate shared caches
- **Solution**: Enforce readonly package lockfiles, disable auto-merge in monorepos
- **Tags**: yarn, pnp, monorepo, supplychain

## Compromised Python Wheel with Obfuscated One-liner Backdoor

- **Attack Type**: Malicious Packaging
- **Target**: Python environments
- **Vulnerability**: Backdoor in binary .whl
- **MITRE**: T1204.002 (Malicious File Execution)
- **Impact**: C2 access, remote command execution
- **Tools**: PyPI, Python, base64, pyminifier
- **Scenario**: A Python .whl file uploaded to PyPI contains obfuscated one-liner backdoor in __init__.py, exploiting trust in binary wheels.
- **Attack Steps**: 1. The attacker publishes a .whl binary distribution on PyPI for a package with a generic name like stringhelper.2. Inside the wheel, they embed an obfuscated base64-encoded Python one-liner in __init__.py.3. When imported, this line connects to an external C2 server.4. Because it’s binary and auto-built, it passes basic code reviews.5. Developers or apps installing via pip install stringhelper unknowingly run the payload.6. The C2 channel is established, and attacker can execute arbitrary Python code remotely.7. Cleanup is difficult without full wheel unpacking and manual static analysis.
- **Detection**: Inspect wheel contents pre-install
- **Solution**: Prefer source installs with integrity checks; unpack wheels for sensitive apps
- **Tags**: python, pypi, wheel, obfuscation

## Attacker Leverages Popular JS Lib Abandonment to Inject Malware

- **Attack Type**: Abandoned Library Takeover
- **Target**: JS Webapps, node-based apps
- **Vulnerability**: Takeover of stale libraries
- **MITRE**: T1554 (Compromise Software Dependencies)
- **Impact**: Mass compromise of web apps
- **Tools**: npm, GitHub, Renovate
- **Scenario**: An attacker waits for a popular JavaScript library to go unmaintained, then takes control of the repo or registry listing to insert malicious code.
- **Attack Steps**: 1. The attacker monitors abandoned or deprecated JavaScript libraries with thousands of downloads.2. They contact the maintainer or fork the project and publish an "updated" version with malicious code.3. Due to outdated lockfiles or * semver ranges, the malicious version gets pulled.4. The malware exfiltrates API keys, modifies UI logic, or logs user sessions.5. If the package is a transitive dependency, many apps unknowingly become vulnerable.6. Attackers may even submit PRs upstream to reintroduce the malware.7. Maintainers often discover too late due to auto-publishing pipelines.
- **Detection**: Audit contributor activity and version diffs
- **Solution**: Monitor abandoned packages; freeze versions via lockfiles
- **Tags**: js, takeover, npm, legacy deps

## Fake GitHub Repo Hosting Lookalike Package Linked in README

- **Attack Type**: Social Engineering
- **Target**: Developers researching on GitHub
- **Vulnerability**: Social engineering via docs
- **MITRE**: T1566.002 (Spearphishing via Service)
- **Impact**: SSH key theft, reverse shells
- **Tools**: GitHub, PyPI, npm
- **Scenario**: A malicious GitHub repo mimics a legitimate one, but links to an attacker-controlled package in the README, tricking developers into pip install or npm install.
- **Attack Steps**: 1. The attacker forks a popular repo and updates its README to point to a lookalike malicious package (pip install realfast vs legit real-fast).2. The GitHub project looks valid and indexed by search engines.3. A developer finds this project, follows the README, and installs the fake package.4. The fake package contains scripts that steal SSH keys or install persistent reverse shells.5. Due to the trust in GitHub-hosted content, the attack spreads via cloning or shared links.6. Maintainers of the original repo may not notice the fork for weeks.7. This tactic relies heavily on trust and README visibility rather than dependency managers.
- **Detection**: Monitor unusual forks and cloned repo traffic
- **Solution**: Use pip and npm only with verified maintainers, never from README copy-paste
- **Tags**: github, socialengineering, pip, typosquatting

## Fake Scoped Rust Crate Targeting Supply Chain via cargo

- **Attack Type**: Namespace Spoofing
- **Target**: Rust monorepos, CI/CD
- **Vulnerability**: Insecure crate resolution
- **MITRE**: T1195.002 (Supply Chain Compromise)
- **Impact**: Code exfiltration, poisoned builds
- **Tools**: Rust, cargo, crates.io
- **Scenario**: A fake @company/math crate is published to crates.io, mimicking private internal crates used in large Rust monorepos, exploiting missing source enforcement in Cargo.toml.
- **Attack Steps**: 1. The attacker publishes a crate named company-math or @company/math with metadata mimicking an internal crate.2. Due to misconfigured Cargo.toml without [patch] or explicit source control, cargo build fetches the public malicious version.3. The malicious crate executes code during build.rs or postbuild hooks.4. This payload may extract environment variables, AWS keys, or manipulate the target build output.5. Internal Rust apps unknowingly incorporate the backdoored crate.6. Detection is hard unless binary output is analyzed or crates are reproducibly built.7. This tactic is increasingly used in Rust-heavy CI/CD environments where private crates are common.
- **Detection**: Audit Cargo.lock and crate sources
- **Solution**: Always lock crates and enforce [patch] overrides
- **Tags**: rust, crates.io, cargo, namespace spoofing

