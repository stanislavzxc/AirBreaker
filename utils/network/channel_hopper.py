import asyncio
import re

from utils.system.run_command import run_command


async def get_available_channels(device: str) -> list[int]:
    try:
        code, stdout, _ = await run_command("iwlist", device, "channel")
        if code == 0:
            channels = [int(ch) for ch in re.findall(r"Channel\s+(\d+)", stdout)]
            if channels:
                return sorted(list(set(channels))) 
    except Exception:
        pass
    
    print(f"cannot get channels for {device} now using default (1-13).")
    return list(range(1, 14))


async def channel_hopper(device):
    channels = await get_available_channels(device)
    print("hopper was started")
    while True:
        for channel in channels:
            try:
                code, stderr, _ = await run_command("iw", "dev", device, "set", "channel", str(channel))
                if code != 0:
                    print(f"cannot change channel {stderr}") 
                    continue
                print(f"change the channel {channel}")
            except asyncio.CancelledError:
                break
            except Exception:
                print("unkown error in hopper")
            await asyncio.sleep(0.25)
    
