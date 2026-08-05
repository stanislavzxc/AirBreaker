from fastapi import HTTPException, status
import shutil

def check_depends(wanted_depends: list):
     for d in wanted_depends:
        if not shutil.which(d):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"System library '{d}' is not installed"
            )