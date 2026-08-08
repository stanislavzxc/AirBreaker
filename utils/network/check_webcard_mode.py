import os


def check_webcard_mode(device: str) -> str:
    wanted_dir = f"/sys/class/net/{device}/type"

    if not os.path.exists(wanted_dir):
       raise FileNotFoundError(f"Interface folder '{wanted_dir}' not found")
    
    try:
        with open(wanted_dir, 'r') as file:
            code = file.read().strip()
            if code == '803':
                return 'monitor'
            return 'managed'
        
    except Exception as e:
        raise ValueError(f"Failed to read interface type for {device}: {e}")
