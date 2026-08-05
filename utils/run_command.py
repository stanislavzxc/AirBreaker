import asyncio
from typing import Tuple

async def run_command(*args: str) -> Tuple[int, str, str]:
    proc = await asyncio.create_subprocess_exec(
        "sudo", *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    
    return (
        proc.returncode, 
        stdout.decode(errors="replace").strip(), 
        stderr.decode(errors="replace").strip()
    )