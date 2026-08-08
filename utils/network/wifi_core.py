import asyncio
from typing import Dict

from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt

from utils.network.get_bssid import get_bssid

networks : Dict[str, dict] = {}

def wifi_packets_callback(packet, queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
    if not packet.haslayer(Dot11):
        return 
    
    bssid = get_bssid(packet)
    if not bssid: return 

    if packet.haslayer(Dot11Beacon):
        try:
            rssi = packet.dBm_AntSignal
        except AttributeError:
            rssi = -99

        ssid = ""
        channel = 1
        layer = packet[Dot11Elt]
        while isinstance(layer, Dot11Elt):
            if layer.ID == 0:  # SSID
                try:
                    ssid = layer.info.decode('utf-8', errors='ignore')
                except:
                    pass
            elif layer.ID == 3:  # Channel
                try:
                    channel = int(layer.info)
                except:
                    pass
            layer = layer.payload.getlayer(Dot11Elt)

        if bssid not in networks:
            networks[bssid] = {
                "ssid": ssid if ssid else "<Hidden>",
                "bssid": bssid,
                "rssi": rssi,
                "channel": channel,
                "data_bytes": 0
            }
        else:
            networks[bssid]["rssi"] = rssi
            networks[bssid]["channel"] = channel
        loop.call_soon_threadsafe(queue.put_nowait, networks[bssid])
    elif packet[Dot11].type == 2:
        if bssid in networks:
            packet_size = len(packet)  
            networks[bssid]["data_bytes"] += packet_size
            
            loop.call_soon_threadsafe(queue.put_nowait, networks[bssid])


def wifi_packets_clear():
    networks.clear()
