# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import mock_open

from utils.network.network_card import check_network_card_mode


def test_monitor_mode(monkeypatch) -> None:
    monkeypatch.setattr('os.path.exists', lambda path: True) 

    mocked_open = mock_open(read_data = "803")
    monkeypatch.setattr("builtins.open", mocked_open)

    mode = check_network_card_mode("wlan0") 

    assert mode == "monitor"

def test_managed_mode(monkeypatch) -> None:
    monkeypatch.setattr('os.path.exists', lambda path: True) 
    
    mocked_open = mock_open(read_data = "1")
    monkeypatch.setattr("builtins.open", mocked_open)
    
    mode = check_network_card_mode("wlan0") 
    
    assert mode == "managed"



