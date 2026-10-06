# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from unittest.mock import AsyncMock, MagicMock, patch
from models.scanning import WifiNetworkModel

class TestwifiScanning():

    def setup_tests(self):
        with patch("utils/networkchannel_hopper", new_callable=AsyncMock) as hoppper_mock, \
            patch("utils/network/wifi_packets_clear", new_callable=AsyncMock) as packets_clear_mock, \
            patch("scapy.all.AsyncSniffer", new_callable=AsyncMock) as sniffer_mock:  

            self.hopper_mock = self.hopper_mock
            self.packets_clear_mock = self.packets_clear_mock
            self.hopper_mock = self.hopper_mock

    async def test_start_scanning():
        pass
    
    async def test_scanning_duplicate_prevent():
        pass

    async def test_stop_scanning():
        pass

    async def test_stream_results_come():
    `pass