# app/dependencies.py
import os
from typing import Annotated

from fastapi import Depends, HTTPException, status

from state import AppState, app_state


def get_app_state() -> AppState:
    return app_state

def get_monitor_device(state: Annotated[AppState, Depends(get_app_state)] ) -> str:
    device = state.current_card
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wi-Fi device is not selected in app state"
        )
        
    wanted_dir = f"/sys/class/net/{device}/type"

    if not os.path.exists(wanted_dir):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interface folder '{wanted_dir}' not found"
        )
    
    try:
        with open(wanted_dir, 'r') as file:
            code = file.read().strip()
            
        if code != '803':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Device '{device}' is not in monitor mode (type code: {code})"
            )
            
        return device  
        
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read interface type for {device}: {e}"
        )
