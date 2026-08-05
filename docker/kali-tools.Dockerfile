FROM kalilinux/kali-rolling:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    nikto \
    sqlmap \
    nuclei \
    gobuster \
    sslscan \
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
CMD ["bash"]
