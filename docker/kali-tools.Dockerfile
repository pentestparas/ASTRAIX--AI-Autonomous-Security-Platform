FROM kalilinux/kali-rolling:latest
ENV DEBIAN_FRONTEND=noninteractive
# Tool inventory converges on what AI pentest platforms (Dark-Moon, Xalgorix,
# PentAGI, RedAmon, Zen-AI-Pentest) drive natively: recon (masscan, dnsrecon,
# subfinder, naabu, dnsx, httpx, whatweb), web fuzz (ffuf, wfuzz, dirsearch,
# katana, feroxbuster), API (kiterunner, graphqlmap, smuggler), vuln
# (commix, arjun, wafw00f, wpscan, joomscan, xsstrike), brute (hydra),
# exploit (searchsploit, metasploit, john, hashcat), source review
# (semgrep, bandit, gitleaks, trufflehog), TLS (testssl.sh). dalfox and
# kiterunner ship as GitHub binaries (not in Kali repos).
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    nikto \
    sqlmap \
    nuclei \
    gobuster \
    sslscan \
    dirb \
    masscan \
    dnsrecon \
    ffuf \
    wfuzz \
    testssl.sh \
    whatweb \
    wafw00f \
    arjun \
    commix \
    hydra \
    wpscan \
    joomscan \
    dirsearch \
    subfinder \
    naabu \
    dnsx \
    httpx-toolkit \
    feroxbuster \
    xsstrike \
    gitleaks \
    trufflehog \
    bandit \
    exploitdb \
    john \
    hashcat \
    metasploit-framework \
    jq \
    wordlists \
    ca-certificates \
    curl \
    wget \
    git \
    python3-pip \
    unzip \
    > /dev/null 2>&1 && rm -rf /var/lib/apt/lists/* && update-ca-certificates --fresh > /dev/null 2>&1
# dalfox (Go XSS scanner), kiterunner (API/content discovery) + katana
# (crawler) - GitHub binaries not in Kali repos. Asset names verified against
# the releases API 2026-08: dalfox uses x86_64 (not amd64) since v3.x.
RUN set -eux; \
    DALFOX_VER=$(curl -s https://api.github.com/repos/hahwul/dalfox/releases/latest | jq -r .tag_name); \
    curl -sL "https://github.com/hahwul/dalfox/releases/download/${DALFOX_VER}/dalfox-${DALFOX_VER}-linux-x86_64.tar.gz" -o /tmp/dalfox.tgz; \
    tar -xzf /tmp/dalfox.tgz -C /usr/local/bin --strip-components=1; \
    KR_VER=$(curl -s https://api.github.com/repos/assetnote/kiterunner/releases/latest | jq -r .tag_name); \
    curl -sL "https://github.com/assetnote/kiterunner/releases/download/${KR_VER}/kiterunner_${KR_VER#v}_linux_amd64.tar.gz" -o /tmp/kr.tgz; \
    tar -xzf /tmp/kr.tgz -C /usr/local/bin; \
    KATANA_VER=$(curl -s https://api.github.com/repos/projectdiscovery/katana/releases/latest | jq -r .tag_name); \
    curl -sL "https://github.com/projectdiscovery/katana/releases/download/${KATANA_VER}/katana_${KATANA_VER#v}_linux_amd64.zip" -o /tmp/katana.zip; \
    unzip -o -q /tmp/katana.zip -d /usr/local/bin; \
    find /usr/local/bin -maxdepth 1 -type f \( -name 'dalfox' -o -name 'kr' -o -name 'katana' \) -exec chmod +x {} +; \
    dalfox --version 2>&1 | head -1; kr --version 2>&1 | head -1; katana --version 2>&1 | head -1
# pip tools: semgrep (SAST). graphqlmap (GraphQL scanner) is NOT on PyPI -
# cloned from GitHub like smuggler (request smuggling detector, also not
# packaged in Kali; both used via /usr/local/bin wrappers).
RUN set -eux; \
    pip3 install --no-cache-dir --break-system-packages --ignore-installed \
    semgrep \
    > /dev/null 2>&1; \
    git clone -q --depth 1 https://github.com/defparam/smuggler /opt/smuggler; \
    git clone -q --depth 1 https://github.com/swisskyrepo/GraphQLmap /opt/graphqlmap; \
    printf '#!/bin/bash\nexec python3 /opt/smuggler/smuggler.py "$@"\n' > /usr/local/bin/smuggler; \
    printf '#!/bin/bash\nexec python3 /opt/graphqlmap/graphqlmap.py "$@"\n' > /usr/local/bin/graphqlmap; \
    chmod +x /usr/local/bin/smuggler /usr/local/bin/graphqlmap; \
    python3 -c "import requests; import readline; print('deps ok')"; \
    semgrep --version 2>&1 | head -1; smuggler --help 2>&1 | head -1; graphqlmap --help 2>&1 | head -1
# External adapter tools (app.vapt.adapters) - setuptools provides the
# distutils shim that raccoon requires on Python 3.13+; fake-useragent is
# pinned to 0.1.x because 1.x dropped the verify_ssl kwarg raccoon uses.
# NOTE: no `|| true` here - a failed install must fail the build loudly.
RUN pip3 install --no-cache-dir --break-system-packages \
    setuptools \
    fake-useragent==0.1.14 \
    raccoon-scanner \
    > /dev/null 2>&1
# Curated wordlists (amitlttwo/All-Wordlists, jeanphorn/wordlist, trickest/wordlists,
# gmelodie/awesome-wordlists) + nuclei templates (projectdiscovery/nuclei-templates).
# Baked at build time into /opt/wordlists; symlinked onto stock /usr/share/wordlists
# paths that tools look for by default (dirb package provides the base tree).
COPY docker/scripts/fetch-wordlists.sh /opt/astraix/fetch-wordlists.sh
RUN chmod +x /opt/astraix/fetch-wordlists.sh && /opt/astraix/fetch-wordlists.sh
# Web form / API / chatbot scanner used by the 'forms' tool
COPY docker/scripts/web_form_scanner.py /opt/vapt/web_form_scanner.py
CMD ["bash"]
