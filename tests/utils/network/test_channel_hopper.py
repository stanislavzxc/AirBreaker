# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from state import app_state
from utils.network import channel_hopper, get_available_channels


def test_get_available_channels_success():
    fake_stdout = "Channel 06\nChannel 01\nChannel 06\nChannel 11"
    
    with patch("utils.network.channel_hopper.run_command", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = (0, fake_stdout, "")
        
        result = asyncio.run(get_available_channels("wlan0"))
        
        assert result == [1, 6, 11]
        mock_run.assert_called_once_with("iwlist", "wlan0", "channel")


def test_get_available_channels_fallback():
    with patch("utils.network.channel_hopper.run_command", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = (1, "", "Device not found")
        
        result = asyncio.run(get_available_channels("wlan0"))
        assert result == list(range(1, 14))


def test_channel_hopper_lifecycle():
    app_state.current_channel = None

    async def run_lifecycle_test():
        with patch("utils.network.channel_hopper.run_command", new_callable=AsyncMock) as mock_run, \
             patch("utils.network.channel_hopper.get_available_channels", new_callable=AsyncMock) as mock_get_channels:
            
            mock_get_channels.return_value = [1, 6]
            mock_run.return_value = (0, "", "")

            task = asyncio.create_task(channel_hopper("wlan0"))

            await asyncio.sleep(0.3)

            assert app_state.current_channel in [1, 6]

            task.cancel()

            with pytest.raises(asyncio.CancelledError):
                await task
                
            assert app_state.current_channel is None

    asyncio.run(run_lifecycle_test())
