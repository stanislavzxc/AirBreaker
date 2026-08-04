import asyncio
import shutil
from fastapi import HTTPException, status
from utils.check_monitor_mode import check_monitor_mode 
from schemas.monitor import MonitorModeResponse

async def set_monitor_mode_service(device: str) -> MonitorModeResponse:
    for cmd in ["ip", "iw"]:
        if not shutil.which(cmd):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"System library '{cmd}' is not installed"
            )
        
    webcard_state = check_monitor_mode(device)
    webcard_wanted_state = 'managed' if webcard_state == "monitor" else 'monitor'

    down = await asyncio.create_subprocess_exec(
        "ip", "link", "set", device, "down",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE 
    )
    stdout_down, stderr_down = await down.communicate()
    
    if down.returncode != 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Command 'ip link set {device} down' failed: {stderr_down.decode().strip()}"
        )
    
    change_mode = await asyncio.create_subprocess_exec(
        "iw", "dev", device, "set", "type", webcard_wanted_state,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout_change, stderr_change = await change_mode.communicate()
    
    if change_mode.returncode != 0:
        rollback = await asyncio.create_subprocess_exec("ip", "link", "set", device, "up")
        await rollback.communicate()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Command 'iw dev {device} set type {webcard_wanted_state}' failed: {stderr_change.decode().strip()}"
        )

    up = await asyncio.create_subprocess_exec(
        "ip", "link", "set", device, "up",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE 
    )
    stdout_up, stderr_up = await up.communicate() 
    
    if up.returncode != 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Command 'ip link set {device} up' failed: {stderr_up.decode().strip()}"
        )
        
    return MonitorModeResponse(
         success=True,
         current_mode=webcard_wanted_state
    )
