import asyncio

from scapy.all import AsyncSniffer

from state import app_state
from utils.network import wifi_packets_callback, wifi_packets_clear

#current target. mass-attack will be add in future, maybe

class PmkidService():
    def __init__(self):
        self._sniffer : AsyncSniffer | None = None
        self.queue : asyncio.Queue = asyncio.Queue()
        self.auth_task : asyncio.Task | None = None

    async def start_capture(self, device):
        if self._sniffer and self._sniffer.running:
            return
        self.queue = asyncio.Queue
        wifi_packets_clear()

        loop = asyncio.get_running_loop()
        self._sniffer = AsyncSniffer(
            iface=device,
            prn=lambda pkt : wifi_packets_callback(pkt, self.queue, loop),
            store=0
        )
        self._sniffer.start()
        print("pmkid sniffer was started")

        await asyncio.sleep(1)

        
    async def stop_capture():
        pass

    async def stream_results():
        pass
