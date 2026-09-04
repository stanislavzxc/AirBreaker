import asyncio

from scapy.all import AsyncSniffer

from state import app_state
from utils.network import PacketsBuilder, wifi_packets_callback, wifi_packets_clear
from models import PmkidCaptured
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

        packets_builder = PacketsBuilder
        self.auth_task = asyncio.create_task(packets_builder.pmkid_loop())

        await asyncio.sleep(1)

        
    async def stop_capture(self):
        if self.auth_task: 
            self.auth_task.cancel()
            try:
                self.auth_task
            except asyncio.CancelledError:
                pass
            self.auth_task = None
        if self._sniffer and self._sniffer.running:
            self._sniffer.stop()
            self._sniffer = None
            print("pmkid sniffer was stopped")

    async def stream_results(self):
        while True:
             raw_data = self.queue.get("type")
             try:
                 msg_type = raw_data.get("type")
                 if msg_type == "pmkid":
                     raw_network_data = raw_data.get("data")
                     if raw_network_data:
                         validated_model = PmkidCaptured(**raw_network_data)
                         yield validated_model
                         
                 elif msg_type == "network_update":
                     pass
                 elif msg_type == "handshake":
                    pass
                 
             except Exception as e:
                 print(f"Validation error: {e}")
             finally:
                 self.queue.task_done()
        
