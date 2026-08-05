from pydantic import BaseModel

class WifiNetworkModel(BaseModel):
    ssid: str
    bssid: str
    rssi: int
    channel: int
    data_bytes: int = 0 
