<<<<<<< HEAD
<h1 align="center">AirBreaker</h1>
<h3 align="center" style="color: #23f7c9;">Wi-Fi Security Framework</h3>
=======
# <h1 align="center">AirBreaker</h1>
### <h3 align="center" style="color: #23f7c9;">Wi-Fi Security Framework</h3>
>>>>>>> 11362d0 (some changes)
<p align="center">
  <img src="images/logo.jpg" alt="AirBreaker Logo" width="auto"/>
</p>

## ⚠️ Disclaimer
This project is created strictly for educational purposes and authorized security testing (penetration testing). 
The developer assumes no liability for any misuse, damage, or illegal activities caused by this tool. 
Only use AirBreaker on networks you own or have explicit, written permission to test.

# Work In Progress

## 📄 License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

[![License: GPL v3](https://shields.io)](https://gnu.org)

# Structure
```text
.
├── docker-compose.yaml          # Docker services configuration
├── errors/                      # Custom error handlers and exceptions
│   ├── __init__.py              # Package initialization
│   ├── app.py                   # FastAPI application error handlers
│   ├── command.py               # CLI command execution errors
│   └── service.py               # Business logic layer exceptions
├── LICENSE                      # Project license
├── main.py                      # Application entry point
├── models/                      # Pydantic data validation models
│   ├── __init__.py              # Package initialization
│   ├── base_response.py         # Base response schema for all APIs
│   ├── errors/                  # Error response models
│   │   ├── __init__.py          # Package initialization
│   │   ├── command.py           # Command execution error models
│   │   └── service.py           # Service layer error models
│   ├── monitor.py               # Wi-Fi monitor mode models
│   ├── networkcards.py          # Network interface card models
│   └── scanning.py              # Wi-Fi scanning request/response models
├── pyproject.toml               # Project metadata and dependencies
├── readme.md                    # Project documentation
├── requirements.txt             # Python package dependencies
├── routers/                     # API route handlers
│   ├── ws/                      # websocket endpoints
│   │   ├── __init__.py          # Package initialization
│   │   ├── wifi_scanning.py     # Wi-Fi scanning endpoints
│   │   └──handshake.py          # WPA handshake capture endpoints
│   ├── __init__.py              # Package initialization
│   ├── choose_network.py        # Network selection endpoints
│   ├── monitor_mode.py          # Monitor mode management endpoints
│   ├── network_cards.py         # Network card management endpoints
├── service/                     # Business logic layer
│   ├── __init__.py              # Package initialization
│   ├── handshake.py             # Handshake capture business logic
│   ├── monitor_mode_service.py  # Monitor mode operations
│   └── wifi_scanning_service.py # Wi-Fi scanning business logic
├── state.py                     # Application state management
└── utils/                       # Utility modules
    ├── __init__.py              # Package initialization
    ├── network/                 # Network-related utilities
    │   ├── __init__.py          # Package initialization
    │   ├── channel_hopper.py    # Channel hopping for scanning
    │   ├── check_webcard_mode.py# Check network card operation mode
    │   ├── deauth_packets.py    # Deauthentication packet injection
    │   ├── get_bssid.py         # BSSID extraction utilities
    │   ├── network_cards.py     # Network card operations
    │   ├── network_services.py  # Network service utilities
    │   └── wifi_core.py         # Core Wi-Fi operations
    └── system/                  # System-level utilities
        ├── __init__.py          # Package initialization
        ├── check_depends.py     # Dependency verification
        └── run_command.py       # Secure command execution wrapper
```

# 🗺️ Roadmap

## 📋 Phase 1: Core Infrastructure (✅ Completed)

- [x] FastAPI backend setup
- [x] Network card management
- [x] Monitor mode activation
- [x] Basic Wi-Fi scanning (beacon, data, eapol frames)
- [x] Channel hopping
- [x] Handshake capture (in work)

---

## 🔬 Phase 2: WPA/WPA2 Attacks (🔄 In Progress)

### PMKID Attack
- [ ] PMKID extraction from AP beacon frames
- [ ] PMKID hash capture (without handshake)
- [ ] Hashcat/JtR integration for cracking
- [ ] PMKID vs Handshake comparison
- [ ] Automated PMKID collection from multiple APs
- [ ] PMKID database management

### Multi-MAC DoS Attack
- [ ] MAC address randomization/spoofing
- [ ] Multiple MAC address generation
- [ ] Deauthentication flood from multiple sources
- [ ] Beacon flooding with fake MACs
- [ ] Association/Disassociation DoS
- [ ] Targeted MAC flooding (specific AP)
- [ ] MAC blacklist/whitelist bypass techniques

### Deauthentication Attacks
- [ ] Targeted deauth attack
- [ ] Broadcast deauth attack
- [ ] Deauth with PMKID capture
- [ ] Deauth frame customization
- [ ] Deauth flood detection bypass

---

## 🌐 Phase 3: Evil Twin Attack (📅 Planned)

### Rogue AP Setup
- [ ] AP cloning with same ESSID/BSSID
- [ ] Automated captive portal creation
- [ ] Rogue AP setup (hostapd)
- [ ] DHCP server configuration (dnsmasq)
- [ ] Traffic interception (MITM)
- [ ] SSL stripping (mitmproxy)

### Credential Harvesting
- [ ] Phishing page templates
- [ ] Browser fingerprinting
- [ ] User-agent based phishing
- [ ] OAuth/OpenID impersonation
- [ ] Social engineering templates
- [ ] Credential storage and analysis

### Advanced Features
- [ ] MAC address filtering bypass
- [ ] Beacon frame spoofing
- [ ] Channel switch announcement (CSA) attacks
- [ ] Hidden SSID disclosure
- [ ] WPS PIN brute force

---

## 🔐 Phase 4: PMF (Protected Management Frames) Attacks (📅 Planned)

### PMF Detection
- [ ] PMF detection (802.11w support check)
- [ ] PMF configuration analysis
- [ ] Capability negotiation analysis
- [ ] Driver capability detection

### PMF Exploitation
- [ ] PMF downgrade attacks (disable PMF)
- [ ] PMF bypass techniques
- [ ] Deauth with PMF (overcome protection)
- [ ] PMF vulnerability exploitation
- [ ] PMF vs SAE interaction
- [ ] PMF negotiation spoofing
- [ ] PMF configuration weakness detection

### Advanced PMF Attacks
- [ ] Mixed-mode exploitation
- [ ] Legacy device targeting
- [ ] Driver-specific bugs exploitation
- [ ] Software-defined radio (SDR) attacks
- [ ] Timing attacks on PMF

---

## 🚀 Phase 5: WPA3 Attacks (📅 Planned)

### WPA3-Personal (SAE) Attacks
- [ ] Dragonfly handshake capture
- [ ] SAE (Simultaneous Authentication of Equals) analysis
- [ ] SAE commit message capture
- [ ] Password hash extraction
- [ ] Dictionary attacks against SAE
- [ ] Side-channel timing attacks
- [ ] Padding Oracle attacks on Dragonfly
- [ ] ECC (Elliptic Curve Cryptography) weakness exploitation
- [ ] PMKID capture (WPA3 version)

### WPA3-Enterprise (Suite-B) Attacks
- [ ] TLS certificate validation bypass
- [ ] Downgrade to WPA2-Enterprise
- [ ] EAP-TLS attacks
- [ ] Certificate chain exploitation
- [ ] RADIUS reflection attacks

### WPA3 Transition Mode Attacks
- [ ] Forced downgrade to WPA2
- [ ] Transition disable attack
- [ ] Mixed-mode vulnerabilities
- [ ] Credential capture in transition mode

---

## 🛡️ Phase 6: Detection & Mitigation (📅 Planned)

### Attack Detection
- [ ] Deauth flood detection
- [ ] Evil twin detection
- [ ] Beacon anomaly detection
- [ ] MAC address change detection
- [ ] PMKID capture attempt detection
- [ ] WPA3 downgrade detection
- [ ] Rogue AP detection
- [ ] KRACK attack detection

### Mitigation Tools
- [ ] 802.11w enforcement
- [ ] PMF forced activation
- [ ] Deauth attack prevention
- [ ] MAC address filtering
- [ ] Beacon protection
- [ ] Intrusion Detection System (IDS) integration
- [ ] Automatic countermeasures

---

## 📊 Phase 7: Reporting & Analysis (📅 Planned)

### Reporting Features
- [ ] Automated pentest reports
- [ ] Vulnerability scoring (CVSS)
- [ ] Security recommendations
- [ ] Attack timeline generation
- [ ] Network audit trail
- [ ] Compliance reporting (PCI-DSS, HIPAA)
- [ ] PDF/HTML report export

### Analysis Tools
- [ ] Wireshark integration
- [ ] pcap analysis
- [ ] Handshake analysis
- [ ] PMKID analysis
- [ ] Frequency/channel analysis
- [ ] Signal strength mapping
- [ ] Performance metrics

---

## 🧪 Phase 8: Automation & Integration (📅 Planned)

### Automation
- [ ] Automated attack chains
- [ ] Scheduled security audits
- [ ] Continuous monitoring
- [ ] Alert system (Telegram/Email)
- [ ] API integration with security tools
- [ ] CI/CD security pipeline integration
- [ ] Auto-remediation scripts

### Integration
- [ ] Metasploit module integration
- [ ] Kali Linux tool integration
- [ ] Nessus/OpenVAS integration
- [ ] SIEM integration (Splunk, ELK)
- [ ] Custom plugin architecture
- [ ] Docker containerization
- [ ] Cloud deployment support

---

## 🎯 Phase 9: Advanced Exploitation (📅 Planned)

### KRACK Attack
- [ ] Four-way handshake manipulation
- [ ] Nonce reuse exploitation
- [ ] Zeroing of group key
- [ ] Fast BSS Transition (FT) reinstallation
- [ ] KRACK detection and mitigation

### Fragmentation Attacks
- [ ] Aggregation and fragmentation frame manipulation
- [ ] A-MSDU injection
- [ ] FragAttacks implementation
- [ ] CVE exploitation (CVE-2020-24586, CVE-2020-24587)
- [ ] Fragmentation attack detection

### Wi-Fi Jamming
- [ ] Channel jamming
- [ ] Frequency hopping jamming
- [ ] Selective jamming
- [ ] Reactive jamming
- [ ] Jamming detection

---

## 🛠️ Phase 10: Hardware & Performance (📅 Planned)

### Hardware Support
- [ ] Support for multiple chipsets (Atheros, Intel, Broadcom)
- [ ] SDR integration (HackRF, BladeRF)
- [ ] External antenna control
- [ ] GPS positioning for war-driving
- [ ] Multiple interface management
- [ ] Concurrent scanning/attacking
- [ ] USB WiFi adapter support

### Performance Optimizations
- [ ] Multi-threading for scanning
- [ ] GPU acceleration for cracking
- [ ] Distributed attack support
- [ ] Memory optimization for large captures
- [ ] Real-time packet processing
- [ ] Asynchronous operations

---

## 🔮 Phase 11: Emerging Technologies (📅 Planned)

### Wi-Fi 6E (6GHz) Attacks
- [ ] 6GHz scanning support
- [ ] Band steering attacks
- [ ] Channel coexistence attacks
- [ ] CQI (Channel Quality Indicator) manipulation
- [ ] 6GHz spectrum analysis

### Wi-Fi 7 (802.11be) Attacks
- [ ] MLO (Multi-Link Operation) exploitation
- [ ] 320MHz channel attacks
- [ ] EHT (Extremely High Throughput) vulnerabilities
- [ ] Multi-AP coordination attacks
- [ ] New frame type exploitation

### AI/ML Integration
- [ ] ML-based attack detection
- [ ] Automated attack selection
- [ ] Predictive vulnerability analysis
- [ ] Neural network-based password cracking
- [ ] Anomaly detection with AI
- [ ] Intelligent channel hopping

---

## 📝 Additional Features

### Security Features
- [ ] Audit logging
- [ ] Role-based access control
- [ ] API key management
- [ ] Secure configuration storage
- [ ] Encrypted communication
- [ ] Forensic capabilities
- [ ] Two-factor authentication

### Developer Experience
- [ ] Comprehensive API documentation
- [ ] Unit and integration tests
- [ ] Code coverage reports
- [ ] Performance benchmarks
- [ ] Plugin development SDK
- [ ] Example scripts and templates

### UI/UX
- [ ] Web dashboard (Vue.js, Chart.js)
- [ ] Real-time monitoring (websocket)
- [ ] Interactive visualizations
- [ ] Mobile responsive design (adaptive site)
- [ ] Dark/light theme
- [ ] Keyboard shortcuts
- [ ] Export/import configurations

---

## 🛠️ Tools Integration
 soon

>>>>>>> 11362d0... some changes