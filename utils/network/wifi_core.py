import asyncio
from typing import Dict

from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt

from state import app_state
from utils.network.get_bssid import get_bssid

networks: Dict[str, dict] = {}

def wifi_packets_callback(packet, queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
    if not packet.haslayer(Dot11):
        return 
    
    bssid: str = get_bssid(packet)
    if not bssid: 
        return 

    current_channel: int = getattr(app_state, "current_channel", 1)

    if bssid not in networks:
        networks[bssid] = {
            "wpa": "open",
            "ssid": "<Hidden>",
            "bssid": bssid,
            "rssi": -99,
            "channel": current_channel,
            "data_bytes": 0,
            "clients_mac": [] 
        }

    addr1: str = packet.addr1  # (Recipient)
    addr2: str = packet.addr2  # (Sender)
    client_mac: str = ''

    if addr1 == bssid and addr2 and addr2 != "ff:ff:ff:ff:ff:ff" and addr2 != bssid:
        client_mac = addr2
    elif addr2 == bssid and addr1 and addr1 != "ff:ff:ff:ff:ff:ff" and addr1 != bssid:
        client_mac = addr1

    if client_mac and client_mac not in networks[bssid]["clients_mac"]:
        networks[bssid]["clients_mac"].append(client_mac)
        loop.call_soon_threadsafe(queue.put_nowait, networks[bssid].copy())

    if packet.haslayer(Dot11Beacon):
        try:
            rssi: int = packet.dBm_AntSignal
        except AttributeError:
            rssi = -99

        wpa_version: str = "open"
        ssid: str = ""
        layer = packet[Dot11Elt]

        while isinstance(layer, Dot11Elt):
            if layer.ID == 0:  # SSID
                try:
                    ssid = layer.info.decode('utf-8', errors='ignore')
                except Exception:
                    pass

            if layer.ID == 48:
                wpa_version = "wpa2"
                if b"\x00\x0f\xac\x08" in layer.info:
                    wpa_version = "wpa3"
            elif layer.ID == 221:
                if layer.info.startswith(b"\x00\x50\xf2\x01"):
                    wpa_version = "wpa1"

            layer = layer.payload.getlayer(Dot11Elt)
            
        networks[bssid]["wpa"] = wpa_version
        networks[bssid]["rssi"] = rssi
        networks[bssid]["channel"] = current_channel
        if ssid: 
            networks[bssid]["ssid"] = ssid
        
        loop.call_soon_threadsafe(queue.put_nowait, networks[bssid].copy())

    elif packet[Dot11].type == 2:
        packet_size = len(packet)  
        networks[bssid]["data_bytes"] += packet_size
        networks[bssid]["channel"] = current_channel  
        
        loop.call_soon_threadsafe(queue.put_nowait, networks[bssid].copy())


def wifi_packets_clear():
    networks.clear()
