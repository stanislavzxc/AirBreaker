from pydantic import BaseModel, ComputedField, Field

class PmkidCaptured(BaseModel):
    type: str = "pmkid_captured"
    bssid: str
    client_mac: str
    pmkid: bytes 
    packet: any = Field(exclude=True) 
    ssid: str = "<Hidden>"
    channel: int = 1

    @ComputedField
    def pmkid_hex(self) -> str:
        return self.pmkid.hex()

    @ComputedField
    def hashcat_format(self) -> str:
        bssid_clean = self.bssid.replace(":", "").lower()
        client_clean = self.client_mac.replace(":", "").lower()
        ssid_hex = self.ssid.encode('utf-8', errors='ignore').hex()
        return f"22000*{self.pmkid_hex}*{bssid_clean}*{client_clean}*{ssid_hex}"
