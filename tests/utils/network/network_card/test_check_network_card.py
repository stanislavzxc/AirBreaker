# SPDX-License-Identifier: GPL-3.0-or-later

from state import app_state
from utils.network.network_card import check_network_card


def test_check_card():
    app_state.current_card = "wlan0"

    card = check_network_card()

    assert card == "wlan0"
