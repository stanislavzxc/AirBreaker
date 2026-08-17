from errors import CommandException
from utils.system.run_command import run_command


async def network_services_kill(device: str) -> bool:
    code_disconnect,_, err_disconnect= await run_command("nmcli", "device", "disconnect", device)
    await _handle_error(code_disconnect, f"iw dev {device} disconnect", err_disconnect)
    
    code_nm,_, error_nm = await run_command("nmcli", "device", "set", device, "managed", "no",)
    await _handle_error(code_nm,f"nmcli device set {device} managed no", error_nm)

    code_nm_kill,_, error_nm_kill = await run_command("nmcli", "device", "set", device, "managed", "no",)
    await _handle_error(code_nm,f"nmcli device set {device} managed no", error_nm)

    code_wpa_supplicant,_ ,error_wpa_supplicant = await run_command("systemctl", "stop", "wpa_supplicant")
    await _handle_error(code_wpa_supplicant, f"systemctl stop wpa_supplicant", error_wpa_supplicant)
  
    return True

async def network_services_awake(device: str) -> bool:
    code_nm,_, error_nm = await run_command("nmcli", "device", "set", device, "managed", "yes",)
    await _handle_error(code_nm,f"nmcli device set {device} managed no", error_nm)

    
    code_wpa_supplicant,_ ,error_wpa_supplicant = await run_command("systemctl", "start", "wpa_supplicant")
    await _handle_error(code_wpa_supplicant, f"systemctl stop wpa_supplicant", error_wpa_supplicant)
    
    return True

async def _handle_error(status_code, failed_cmd, err) -> None:
    if status_code != 0:
        raise CommandException(failed_cmd=failed_cmd, stderr=err)
