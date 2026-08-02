import asyncio
import re
import shutil

async def GetWifiChipsets():
    if not shutil.which("airmon-ng"):
        return {"error": "airmon-ng is not installed"}
    try:
        process = await asyncio.create_subprocess_exec(
            "sudo", "airmon-ng",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode().strip() or stdout.decode().strip() or "Unknown error"
            return {"success": False, "error": f"OS error: {error_msg}"}

        lines = stdout.decode('utf-8', errors='ignore').strip().split('\n')
        interfaces = []
        start_working = False

        for line in lines:
            if not line.strip(): 
                continue
            if "interface" in line.lower() and "chipset" in line.lower():
                start_working = True
                continue
            if start_working:
                parts = re.split(r'\t+|\s{2,}', line.strip())
                if len(parts) >= 4:
                    interfaces.append({
                        "phy": parts[0],
                        "interface": parts[1],
                        "driver": parts[2],
                        "chipset": parts[3]
                    })
        return interfaces 
    
    except Exception as e:
        return {"success": False, "error": str(e)}
