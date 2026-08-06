import asyncio
from fastapi import HTTPException, status

from state import app_state

from utils.check_webcard_mode import check_webcard_mode 
from utils.network_manager import network_manager_kill, network_manager_awake
from utils.run_command import run_command 
from utils.check_depends import check_depends
from schemas.monitor import MonitorModeResponse

async def set_monitor_mode_service() -> MonitorModeResponse:
    device = app_state.current_card
    if not device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No network card selected. Call /set_current_network_card first.",
        )
    wanted_depends = ["ip", "iw"]
    missing_depends = check_depends(wanted_depends) 
    if missing_depends:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Required dependencies are missing: {missing_depends}"
        )
        
    webcard_state = check_webcard_mode(device)
    webcard_wanted_state = 'managed' if webcard_state == "monitor" else 'monitor'

    async def handle_error(failed_command: str, stderr: str):
        await run_command("ip", "link", "set", device, "up")
        await network_manager_awake(device)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Command '{failed_command}' failed: {stderr}" 
        )

    if webcard_wanted_state == "monitor":
        await network_manager_kill(device)
    else:
        await network_manager_awake(device)

    await asyncio.sleep(1)

    code_down, _, stderr_down = await run_command("ip", "link", "set", device, "down")
    if code_down != 0:
        await handle_error(f"ip link set {device} down", stderr_down)

    code_change, _, stderr_change = await run_command("iw", "dev", device, "set", "type", webcard_wanted_state)
    if code_change != 0:
        await handle_error(f"iw dev {device} set type {webcard_wanted_state}", stderr_change)

    code_up, _, stderr_up = await run_command("ip", "link", "set", device, "up")
    if code_up != 0:
        await network_manager_awake(device)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Command 'ip link set {device} up' failed: {stderr_up}" 
        )
        
    return MonitorModeResponse(
         success=True,
         current_mode=webcard_wanted_state
    )
