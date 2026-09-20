```text
./AirBreaker
├── Dockerfile                   # Docker backend container configuration
├── docker-compose.yaml          # Docker services configuration
├── LICENSE                      # Project license (GPL-3.0-or-later)
├── main.py                      # Application entry point
├── Makefile                     # Automation tasks (e.g., running tests, linting)
├── pyproject.toml               # Project metadata, ruff, and tool dependencies
├── readme.md                    # Project documentation
├── requirements.txt             # Python package dependencies
├── ROADMAP.md                   # Future project development plans
├── STRUCTURE.md                 # Structure overview file
├── add_license.py               # Utility script to append license headers
├── contributing.md              # Guidelines for contributing to the project
├── state.py                     # Application state management (app_state)
│
├── db/                          # Database utility modules
│   ├── __init__.py              # Package initialization
│   └── db,py                    # Database core (with file name typo intact)
│
├── deps/                        # Custom Dependency Injection for router validations
│   ├── rest/                    # DI for REST endpoints
│   │   ├── __init__.py          # Package initialization
│   │   └── monitor_device.py    # Get a network_card that is set in monitor mode
│   └── ws/                      # DI for WebSocket endpoints
│       ├── __init__.py          # Package initialization
│       └── monitor_device.py    # Get a network_card that is set in monitor mode
│
├── errors/                      # Custom error handlers and exceptions
│   ├── __init__.py              # Package initialization
│   ├── app.py                   # FastAPI application error handlers
│   ├── command.py               # CLI command execution errors
│   ├── network_card.py          # Network interface card errors
│   └── service.py               # Business logic layer exceptions
│
├── images/                      # Documentation assets
│   └── logo.jpg                 # Project logo image
│
├── models/                      # Pydantic data validation models
│   ├── __init__.py              # Package initialization
│   ├── base_response.py         # Base response schema for all APIs
│   ├── handshake.py             # Handshake validation model
│   ├── monitor.py               # Wi-Fi monitor mode models
│   ├── networkcards.py          # Network interface card models
│   ├── pmkid.py                 # PMKID capture models
│   ├── scanning.py              # Wi-Fi scanning request/response models
│   ├── enums/                   # Enumerations for typed data
│   │   ├── __init__.py          # Package initialization
│   │   └── deauth.py            # Deauthentication frame enums
│   └── errors/                  # Error response schemas
│       ├── __init__.py          # Package initialization
│       ├── command.py           # Command execution error models
│       └── service.py           # Service layer error models
│
├── routers/                     # API route handlers
│   ├── __init__.py              # Package initialization
│   ├── rest/                    # REST API endpoints
│   │   ├── __init__.py          # Package initialization
│   │   ├── choose_network.py    # Network selection endpoints
│   │   ├── monitor_mode.py      # Monitor mode management endpoints
│   │   └── network_cards.py     # Network card management endpoints
│   └── ws/                      # WebSocket API endpoints
│       ├── __init__.py          # Package initialization
│       ├── handshake.py         # WPA handshake capture endpoints
│       ├── pmkid.py             # PMKID capture endpoints
│       └── wifi_scanning.py     # Wi-Fi scanning endpoints
│
├── services/                    # Business logic layer
│   ├── __init__.py              # Package initialization
│   ├── handshake.py             # Handshake capture business logic
│   ├── monitor_mode.py          # Monitor mode operations
│   ├── pmkid.py                 # PMKID capture business logic
│   └── wifi_scanning.py         # Wi-Fi scanning business logic
│
├── utils/                       # Utility modules
│   ├── __init__.py              # Package initialization
│   ├── network/                 # Network-related utilities
│   │   ├── __init__.py          # Package initialization
│   │   ├── channel_hopper.py    # Channel hopping for scanning
│   │   ├── generate_mac.py      # Generate random MAC address
│   │   ├── get_bssid.py         # BSSID extraction utilities
│   │   ├── network_services.py  # Network service utilities
│   │   ├── packets_builder.py   # Deauthentication and management packet injection
│   │   ├── wifi_core.py         # Core low-level Wi-Fi operations
│   │   └── network_card/        # Submodule for individual interface cards logic
│   │       ├── __init__.py      # Package initialization
│   │       ├── check_network_card_mode.py # Check network card operation mode
│   │       ├── check_network_card.py      # Validate current active network card
│   │       └── network_cards.py           # Network card operations
│   └── system/                  # System-level utilities
│       ├── __init__.py          # Package initialization
│       ├── check_depends.py     # Dependency verification (e.g., checking for iw, iwlist)
│       └── run_command.py       # Secure asynchronous command execution wrapper
│
└── tests/                       # Pytest test suite mirroring application layout
    ├── __init__.py              # Package initialization
    ├── api/                     # Integration tests for routes
    │   ├── rest/                # REST endpoint tests
    │   │   └── __init__.py      # Package initialization
    │   └── ws/                  # WebSocket endpoint tests
    │       └── __init__.py      # Package initialization
    ├── errors/                  # Custom exceptions tests
    │   └── __init__.py          # Package initialization
    ├── models/                  # Pydantic schemas tests
    │   └── __init__.py          # Package initialization
    ├── service/                 # Business logic tests
    │   └── __init__.py          # Package initialization
    └── utils/                   # Unit tests for helper functions
        ├── __init__.py          # Package initialization
        ├── system/              # System utility tests
        │   ├── __init__.py      # Package initialization
        │   ├── test_check_depends.py # Tests for check_depends utility
        │   └── test_run_command.py   # Tests for subprocess execution
        └── network/             # Network utility tests
            ├── __init__.py      # Package initialization
            ├── test_channel_hopper.py # Tests for channel hopping lifecycle and mocks
            ├── test_generate_mac.py   # Tests for MAC randomizer
            └── network_card/    # Interface manager unit tests
                ├── __init__.py  # Package initialization
                ├── test_check_network_card_mode.py # Mock file reading for modes
                ├── test_check_network_card.py      # State check exceptions tests
                └── test_network_cards.py           # Interface parsing tests

```