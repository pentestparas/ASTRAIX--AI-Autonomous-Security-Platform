FROM kalilinux/kali-rolling:latest
ENV DEBIAN_FRONTEND=noninteractive
# Tool inventory converges on what AI pentest platforms (Dark-Moon, Xalgorix,
# PentAGI, RedAmon, Zen-AI-Pentest) drive natively: recon (masscan, dnsrecon,
# subfinder, naabu, dnsx, httpx, whatweb), web fuzz (ffuf, wfuzz, dirsearch),
# vuln (commix, arjun, wafw00f, wpscan, joomscan), brute (hydra),
# TLS (testssl.sh). dalfox (Go XSS scanner) is NOT in Kali repos - install it
# later via GitHub release binary if needed.
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
    jq \
    wordlists \
    ca-certificates \
    curl \
    wget \
    git \
    python3-pip \
    > /dev/null 2>&1 && rm -rf /var/lib/apt/lists/* && update-ca-certificates --fresh > /dev/null 2>&1
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
CMD ["bash"]
