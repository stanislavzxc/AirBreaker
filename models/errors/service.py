# SPDX-License-Identifier: GPL-3.0-or-later
from pydantic import BaseModel, Field


class ServiceErrorResponse(BaseModel):
    code: int = Field(
        default=500,
        description="http error"
    )
    detail: str = Field(
        default=None,
        description="comment about exception"   
    )
