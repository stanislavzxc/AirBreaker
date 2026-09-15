# SPDX-License-Identifier: GPL-3.0-or-later
from pydantic import BaseModel
from scapy.packet import Packet


class HandshakeModel(BaseModel):
    type: str 
    step: str 
    bssid: str
    client_mac: str 
    packet: bytes
