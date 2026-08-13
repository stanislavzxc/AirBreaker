import asyncio
from scapy.all import AsyncSniffer

from schemas.scanning import WifiNetworkModel
from state import app_state
from utils.network import channel_hopper, wifi_packets_callback, wifi_packets_clear


class WifiScanningService:
    def __init__(self):
        self._hopper_task: asyncio.Task | None = None
        self._sniffer: AsyncSniffer | None = None
        self.queue: asyncio.Queue = asyncio.Queue()

    async def start_scanning(self):
        device = app_state.current_card
        if not device:
            raise ValueError("No network card selected in app_state")

        if self._hopper_task or (self._sniffer and self._sniffer.running):
            return

        wifi_packets_clear()
        self.queue = asyncio.Queue()

        self._hopper_task = asyncio.create_task(channel_hopper(device))

        loop = asyncio.get_running_loop()
        self._sniffer = AsyncSniffer(
            iface=device,
            prn=lambda pkt: wifi_packets_callback(pkt, self.queue, loop),
            store=0
        )
        self._sniffer.start()
        
        print(f"Scanning started successfully on device: {device}")

    async def stop_scanning(self):
        if self._hopper_task:
            self._hopper_task.cancel()
            try:
                await self._hopper_task
            except asyncio.CancelledError:
                pass
            self._hopper_task = None

        if self._sniffer and self._sniffer.running:
            self._sniffer.stop()
            self._sniffer = None
            print("Sniffer stopped successfully")

    async def stream_results(self):
        while True:
            raw_network_data = await self.queue.get()
            try:
                validated_model = WifiNetworkModel(**raw_network_data)
                yield validated_model
            except Exception as e:
                print(f"Validation error: {e}")
            finally:
                self.queue.task_done()
