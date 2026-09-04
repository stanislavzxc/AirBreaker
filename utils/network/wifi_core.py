import asyncio
from typing import Dict

from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt
from scapy.layers.eap import EAPOL

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
        loop.call_soon_threadsafe(queue.put_nowait, {"type": "network_update", "data": networks[bssid].copy()})

    # 3. Beacon
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
        
        loop.call_soon_threadsafe(queue.put_nowait, {"type": "network_update", "data": networks[bssid].copy()})

    # 4.Data)
    elif packet[Dot11].type == 2:
        packet_size = len(packet)  
        networks[bssid]["data_bytes"] += packet_size
        networks[bssid]["channel"] = current_channel  
        
        loop.call_soon_threadsafe(queue.put_nowait, {"type": "network_update", "data": networks[bssid].copy()})

    # (EAPOL)
    if packet.haslayer(EAPOL):
        eapol = packet[EAPOL]

        # (EAPOL-Key)
        if eapol.type == 3:
            wpa_key = eapol.payload
            try:
                key_info = wpa_key.key_info
                key_data = wpa_key.key_data
            except AttributeError:
                return

            is_pairwise = bool(key_info & 0x0080)
            is_ack = bool(key_info & 0x0100)

            if is_pairwise:
                if is_ack:
                    loop.call_soon_threadsafe(
                        queue.put_nowait, 
                        {"type": "handshake", "step": "M1", "bssid": bssid, "client_mac": client_mac or addr1, "packet": packet}
                    )
                else:
                    loop.call_soon_threadsafe(
                        queue.put_nowait, 
                        {"type": "handshake", "step": "M2", "bssid": bssid, "client_mac": client_mac or addr2, "packet": packet}
                    )

                #pmkid logic
                target_client = client_mac or addr1
                if key_data and len(key_data) > 3:
                    pmkid = extract_pmkid_from_key_data(key_data)
                    if pmkid:
                        loop.call_soon_threadsafe(
                            queue.put_nowait,
                            {
                                "type": "pmkid",
                                "bssid": bssid,
                                "client_mac": target_client,
                                "pmkid": pmkid.hex(),
                                "packet": packet
                            }
                        )

def extract_pmkid_from_key_data(key_data: bytes) -> bytes | None:
    try:
        index = 0
        while index < len(key_data):
            if key_data[index] == 0x30:
                length = key_data[index + 1]
                rsn_ie = key_data[index : index + 2 + length]
                
                pos = 2 + 2 # ID + Len + Version
                pos += 4     # Group Suite
                
                if pos + 2 > len(rsn_ie): return None
                pairwise_count = int.from_bytes(rsn_ie[pos:pos+2], byteorder='little')
                pos += 2 + (pairwise_count * 4)
                
                if pos + 2 > len(rsn_ie): return None
                akm_count = int.from_bytes(rsn_ie[pos:pos+2], byteorder='little')
                pos += 2 + (akm_count * 4)
                
                pos += 2 
                
                if pos + 2 <= len(rsn_ie):
                    pmkid_count = int.from_bytes(rsn_ie[pos:pos+2], byteorder='little')
                    if pmkid_count > 0 and pos + 2 + (pmkid_count * 16) <= len(rsn_ie):
                        return rsn_ie[pos + 2 : pos + 2 + 16]
            
            if index + 1 < len(key_data):
                index += 2 + key_data[index + 1]
            else:
                break
    except Exception:
        pass
    return None
def wifi_packets_clear():
    networks.clear()
