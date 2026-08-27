import asyncio

from errors import CommandException, ServiceException
from models.monitor import MonitorModeResponse
from state import app_state
from utils.network import (
    check_network_card_mode,
    network_services_awake,
    network_services_kill,
)
from utils.system import check_depends, run_command


async def set_monitor_mode_service() -> MonitorModeResponse:
    device = app_state.current_card
    if not device:
        raise ServiceException(
            code=500,
            detail="No network card selected. Call /set_current_network_card first.",
        )
   
    wanted_depends = ["ip", "iw"]
    missing_depends = await check_depends(wanted_depends) 

    if missing_depends:
        raise ServiceException(
            code=500,
            detail=f"Required dependencies are missing: {missing_depends}"
        )
        
    network_card_state = check_network_card_mode(device)
    network_card_wanted_state = 'managed' if network_card_state == "monitor" else 'monitor'

    async def handle_error(code: int, failed_command: str, stderr: str):
        if code != 0:
            try:
                await run_command("ip", "link", "set", device, "up")
                await network_services_awake(device)
            except Exception:
                pass
            
            raise CommandException(
                code=500,
                detail=f"Command '{failed_command}' failed: {stderr}" 
            )

    if network_card_wanted_state == "monitor":
        await network_services_kill(device)
    else:
        await network_services_awake(device)

    await asyncio.sleep(1)

    code_down, _, stderr_down = await run_command("ip", "link", "set", device, "down")
    await handle_error(code_down, f"ip link set {device} down", stderr_down)

    code_change, _, stderr_change = await run_command("iw", "dev", device, "set", "type", network_card_wanted_state)
    await handle_error(code_change,f"iw dev {device} set type {network_card_wanted_state}", stderr_change)

    code_up, _, stderr_up = await run_command("ip", "link", "set", device, "up")
    await handle_error(code_up, f"ip link set {device} up", stderr_up)
        
    return MonitorModeResponse(
         success=True,
         current_mode=network_card_wanted_state
    )
