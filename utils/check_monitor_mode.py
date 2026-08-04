from fastapi import HTTPException, status
import os

def check_monitor_mode(device: str) -> str:
    wanted_dir = f"/sys/class/net/{device}/type"

    if not os.path.exists(wanted_dir):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"dir {wanted_dir} not found"
        )
    
    try:
        with open(wanted_dir, 'r') as file:
            code = file.read().strip()
            if code == '803':
                return 'monitor'
            return 'managed'
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read interface type: {str(e)}"
        )