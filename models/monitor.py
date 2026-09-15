# SPDX-License-Identifier: GPL-3.0-or-later
from pydantic import BaseModel


class MonitorModeResponse(BaseModel):
    success: bool
    current_mode: str
