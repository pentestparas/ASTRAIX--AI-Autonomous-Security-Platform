# WAF Bypass Payload List

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/payload-box/waf-bypass-payload-list/graphs/commit-activity)

**A comprehensive collection of WAF (Web Application Firewall) bypass payloads designed for security assessment and penetration testing.** 

This repository serves as a centralized resource for security professionals, penetration testers, and bug bounty hunters to test the robustness of WAF implementations.

<img src="https://github.com/payload-box/waf-bypass-payload-list/blob/main/assets/waf-bypass-payload-list-ismailtasdelen.jpeg">

---

## 📋 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
  - [Burp Suite Intruder](#burp-suite-intruder)
  - [OWASP ZAP](#owasp-zap)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Author](#author)

---

## 📖 Introduction

Web Application Firewalls (WAFs) are a critical line of defense for web applications. However, they are often dependent on signature-based detection and can be bypassed with creativity and specific encoding techniques. This repository compiles known bypass techniques and payloads into organized lists for ease of use during security engagements.

## ✨ Features

- **Protocol Agnostic:** Payloads suitable for various injection points in HTTP requests.
- **Categorized Lists:** Payloads organized by attack vector (SQLi, XSS, RCE, etc.).
- **Tool-Ready:** Formats optimized for popular tools like Burp Suite and OWASP ZAP.
- **Evasion Techniques:** Includes polyglots, obfuscation, and encoding bypasses.

## 📂 Directory Structure

```text
waf-bypass-payload-list/
├── intruder/
│   └── waf_bypass_payloads.txt  # Comprehensive list for Burp Intruder
├── LICENSE                      # MIT License
└── README.md                    # Project Documentation
```

## 🚀 Getting Started

To use these payloads, simply clone the repository to your local machine:

```bash
git clone https://github.com/payload-box/waf-bypass-payload-list.git
cd waf-bypass-payload-list
```

## 🛠️ Usage

### Burp Suite Intruder

1.  Open **Burp Suite** and verify your target is in scope.
2.  Send a request to **Intruder** (`Ctrl+I` / `Cmd+I`).
3.  Go to the **Positions** tab and select the insertion point (e.g., a parameter value, header, or cookie).
4.  Navigate to the **Payloads** tab.
5.  In **Payload Options**, click **Load...** and select `intruder/waf_bypass_payloads.txt`.
6.  Start the attack.
7.  Analyze the results for anomalies (HTTP status codes, response length differences, time delays) that indicate a successful bypass.

### OWASP ZAP

1.  Right-click a request in the **History** tab and select **Fuzz...**.
2.  Highlight the injection point and click **Add...**.
3.  Click **Add...** in the payload dialog.
4.  Choose **File Fuzzer** as the type.
5.  Load the `intruder/waf_bypass_payloads.txt` file.
6.  Start the fuzzer and monitor the results.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/NewPayloads`)
3.  Commit your Changes (`git commit -m 'Add new WAF bypass payloads'`)
4.  Push to the Branch (`git push origin feature/NewPayloads`)
5.  Open a Pull Request

Please ensure your payloads are verified and effective before submitting.

## ⚠️ Disclaimer

**For Educational and Ethical Testing Purposes Only.**

This project is intended for security research, authorization testing, and educational purposes. The author allows the use of this software/list only on systems where the user has explicit permission to test. Using this data to attack targets without prior mutual consent is illegal. The author assumes no liability and is not responsible for any misuse or damage caused by this program.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**İsmail Taşdelen**

- GitHub: [@ismailtsdln](https://github.com/ismailtsdln)
- LinkedIn: [ismailtasdelen](https://www.linkedin.com/in/ismailtasdelen)
