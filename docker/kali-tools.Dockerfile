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
    > /dev/null 2>&1 && rm -rf /var/lib/apt/lists/* && update-ca-certificates --fresh > /dev/null 2>&1
CMD ["bash"]
