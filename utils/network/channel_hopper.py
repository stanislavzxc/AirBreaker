# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
import re

from state import app_state
from utils.system.run_command import run_command


async def get_available_channels(device: str) -> list[int]:
    try:
        code, stdout, _ = await run_command("iwlist", device, "channel")
        if code == 0:
            channels = sorted({int(ch) for ch in re.findall(r"Channel\s+(\d+)", stdout)})
            if channels:
                return channels
    except Exception as e:
        print(f"Error reading channels for {device}: {e}")
    
    print(f"Cannot get channels for {device} now. Using default (1-13).")
    return list(range(1, 14))


async def channel_hopper(device: str):
    channels = await get_available_channels(device)
    print(f"Hopper started for {device} with channels: {channels}")
    
    try:
        while True:
            for channel in channels:
                try:
                    code, _, stderr = await run_command(
                        "iw", "dev", device, "set", "channel", str(channel)
                    )
                    if code != 0:
                        print(f"Cannot change channel to {channel}: {stderr.strip()}")
                    else:
                        app_state.current_channel = channel
                        print(f"Changed channel to {channel}")
                        
                except Exception as e:
                    print(f"Unknown error in hopper loop: {e}")
                
                await asyncio.sleep(0.25)
                
    except asyncio.CancelledError:
        print("Hopper was stopped successfully")
        app_state.current_channel = None
        raise 
