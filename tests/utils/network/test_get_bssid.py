# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import pytest

from utils.network import get_bssid


def test_no_do11_layer():
    pkt_mock = MagicMock()
    pkt_mock.haslayer.return_value = False

    result = get_bssid(pkt_mock)

    assert result is None 
