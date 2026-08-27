import os

from fastapi import Depends, WebSocket, status

from state import AppState, app_state


def get_app_state() -> AppState:
    return app_state

async def get_monitor_device_ws(ws: WebSocket, state: AppState = Depends(get_app_state)) -> str:
    device = state.current_card
    
    if not device:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason="No device selected")
        raise RuntimeError("No device selected")
        
    wanted_dir = f"/sys/class/net/{device}/type"

    if not os.path.exists(wanted_dir):
        await ws.close(code=status.WS_1011_INTERNAL_ERROR, reason="Interface not found")
        raise RuntimeError("Interface not found")
    
    try:
        with open(wanted_dir, 'r') as file:
            code = file.read().strip()
            
        if code != '803':
            await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason="Monitor mode required")
            raise RuntimeError("Not in monitor mode")
            
        return device 
        
    except Exception as e:
        await ws.close(code=status.WS_1011_INTERNAL_ERROR, reason=f"FS error: {e}")
        raise RuntimeError(f"Failed to read interface: {e}")
