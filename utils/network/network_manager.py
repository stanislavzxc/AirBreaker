from utils import run_command


async def network_manager_kill(device: str) -> bool:
    code,_,_ = await run_command("nmcli", "device", "set", device, "managed", "no",)
    return code == 0
async def network_manager_awake(device: str):
    code,_,_ = await run_command("nmcli", "device", "set", device, "managed", "yes")
    return code == 0
