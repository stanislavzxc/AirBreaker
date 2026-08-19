from pydantic import BaseModel
from typing import List

class WifiNetworkModel(BaseModel):
    wpa: str
    ssid: str
    bssid: str
    rssi: int
    channel: int
    data_bytes: int = 0 
    clients_mac : List[str]
