import asyncio
import threading

from scapy.all import sniff

from schemas.scanning import WifiNetworkModel
from state import app_state
from utils.network import channel_hopper, wifi_packets_callback, wifi_packets_clear


class WifiScanningService():
    def __init__(self):
        self._hopper_task: asyncio.Task | None = None
        self._sniff_thread: threading.Thread | None = None
        self._stop_sniff_event = threading.Event()
        self.queue: asyncio.Queue = asyncio.Queue()

    async def start_scanning(self):
        device = app_state.current_card
        if not device:
            raise ValueError("No network card selected in app_state")

        if self._hopper_task or (self._sniff_thread and self._sniff_thread.is_alive()):
            return
        wifi_packets_clear()
        self.queue = asyncio.Queue()
        self._stop_sniff_event.clear()

        self._hopper_task = asyncio.create_task(channel_hopper(device))

        loop = asyncio.get_running_loop()
        
        def run_scapy():
            sniff(
                iface=device,
                prn=lambda pkt: wifi_packets_callback(pkt, self.queue, loop),
                stop_filter=lambda pkt: self._stop_sniff_event.is_set(),
                store=0 
            )

        self._sniff_thread = threading.Thread(target=run_scapy, daemon=True)
        self._sniff_thread.start()
        print(f"process ended succesfully {device}")

    async def stop_scanning(self):
        if self._hopper_task:
            self._hopper_task.cancel()
            try:
                await self._hopper_task
            except asyncio.CancelledError:
                pass
            self._hopper_task = None

        if self._sniff_thread and self._sniff_thread.is_alive():
            self._stop_sniff_event.set()
            await asyncio.to_thread(self._sniff_thread.join, timeout=2.0)
            self._sniff_thread = None

    async def stream_results(self):
        while True:
            raw_network_data = await self.queue.get()
            
            try:
                validated_model = WifiNetworkModel(**raw_network_data)
                yield validated_model
            except Exception as e:
                print(f"valid error: {e}")
            finally:
                self.queue.task_done()
