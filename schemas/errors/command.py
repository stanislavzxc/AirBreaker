from pydantic import BaseModel, Field

class CommandErrorResponse(BaseModel):
    detail: str = Field(
        default=None,
        description="comment about exception"   
    )
    code: int = Field(
        default=500,
        description="http code"
    )
    failed_cmd: str = Field(
        default=None,
        description="linux command thath cannot be succesfull"
    )
    strderr: str = Field(
        default=None,
        detail="exit code from linux terminal"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "linux error",
                "system_error": "Command 'iw dev wlan0 set type monitor' failed: Device or resource busy",
                "code": 500,
                "failed_command": "iw dev wlan0 set type monitor",
                "stderr": "command failed: Device or resource busy (-16)"
            }
        }
