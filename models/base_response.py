# SPDX-License-Identifier: GPL-3.0-or-later
from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool = True
    message: str
