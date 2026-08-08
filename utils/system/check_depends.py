import shutil


async def check_depends(wanted_depends: list) -> list:
    missing = []
    for d in wanted_depends:
        if not shutil.which(d):
            missing.append(d)
    return missing 
        
