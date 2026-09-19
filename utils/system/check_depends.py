# SPDX-License-Identifier: GPL-3.0-or-later
import shutil


async def check_depends(wanted_depends: list) -> list:
    missing = []
    for d in dict.fromkeys(wanted_depends):
        if not shutil.which(d):
            missing.append(d)
    return missing 
        
