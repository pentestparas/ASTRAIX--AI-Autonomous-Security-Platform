FROM kalilinux/kali-rolling:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    nikto \
    sqlmap \
    nuclei \
    gobuster \
    sslscan \
    dirb \
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
RUN pip3 install --no-cache-dir --break-system-packages \
    setuptools \
    fake-useragent==0.1.14 \
    raccoon-scanner \
    > /dev/null 2>&1 || true
# Curated wordlists (amitlttwo/All-Wordlists, jeanphorn/wordlist, trickest/wordlists,
# gmelodie/awesome-wordlists) + nuclei templates (projectdiscovery/nuclei-templates).
# Baked at build time into /opt/wordlists; symlinked onto stock /usr/share/wordlists
# paths that tools look for by default (dirb package provides the base tree).
COPY docker/scripts/fetch-wordlists.sh /opt/astraix/fetch-wordlists.sh
RUN chmod +x /opt/astraix/fetch-wordlists.sh && /opt/astraix/fetch-wordlists.sh
CMD ["bash"]
