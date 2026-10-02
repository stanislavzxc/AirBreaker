# SPDX-License-Identifier: GPL-3.0-or-later

FROM python:3.11-slim

#needs libpcap-dev and tcpdump for scapy 
# also: iw, ip, iwlist, network_manager, wpa_supplicant

RUN apt-get update && apt-get install -y --no-install-recommends \ 
    libpcap-dev \
    tcpdump \
    iw \
    iproute2 \
    network-manager \
    wpasupplicant \
    wireless-tools \
    systemd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app","--host","0.0.0.0","--port","5000"]
