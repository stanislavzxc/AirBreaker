# SPDX-License-Identifier: GPL-3.0-or-later
import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from models.scanning import WifiNetworkModel
from services.wifi_scanning import WifiScanningService


class TestWifiScanning():
    @pytest.fixture(autouse=True)
    def setup_tests(self, mocker):
        self.hopper_mock = mocker.patch("services.wifi_scanning.channel_hopper", new_callable=AsyncMock)
        
        self.packets_clear_mock = mocker.patch("services.wifi_scanning.wifi_packets_clear")
        self.packets_callback_mock = mocker.patch("services.wifi_scanning.wifi_packets_callback")

        self.sniffer_instance_mock = MagicMock()
        self.sniffer_instance_mock.running = False
        self.sniffer_mock = mocker.patch("services.wifi_scanning.AsyncSniffer", return_value=self.sniffer_instance_mock)

        self.service = WifiScanningService()


    async def test_start_scanning(self):
        await self.service.start_scanning("wlan0")
        
        self.packets_clear_mock.assert_called_once()
        self.hopper_mock.assert_called_once_with("wlan0")
        self.sniffer_mock.assert_called_once()
        self.sniffer_instance_mock.start.assert_called_once()
        assert self.service._hopper_task is not None
    
    async def test_scanning_duplicate_prevent(self):
        self.service._sniffer = self.sniffer_instance_mock
        self.sniffer_instance_mock.running = True
        
        self.packets_clear_mock.reset_mock()
        self.hopper_mock.reset_mock()

        await self.service.start_scanning("wlan0")

        self.packets_clear_mock.assert_not_called()
        self.hopper_mock.assert_not_called()

    async def test_stop_scanning(self):
        self.sniffer_instance_mock.running = True
        self.service._sniffer = self.sniffer_instance_mock
        
        loop = asyncio.get_running_loop()
        fake_task = loop.create_future()
        fake_task.cancel()
        
        self.service._hopper_task = fake_task

        await self.service.stop_scanning()

        self.sniffer_instance_mock.stop.assert_called_once()
        assert self.service._hopper_task is None
        assert self.service._sniffer is None



    async def test_stream_results_come(self, mocker):
        mock_network_data = {
            "ssid": "Test_Home", 
            "bssid": "00:11:22:33:44:55",
            "wpa": "WPA2",
            "rssi": -45,
            "channel": 6,
            "clients_mac": ["AA:BB:CC:DD:EE:FF"]
        } 
        
        await self.service.queue.put({"type": "network_update", "data": mock_network_data})

        model_instance = MagicMock(spec=WifiNetworkModel)
        mock_model_cls = mocker.patch("services.wifi_scanning.WifiNetworkModel", return_value=model_instance)

        generator = self.service.stream_results()
        
        result = await apocalypse_safe_anext(generator)

        assert result == model_instance
        mock_model_cls.assert_called_once_with(**mock_network_data)


async def apocalypse_safe_anext(gen):
    return await gen.__anext__()
