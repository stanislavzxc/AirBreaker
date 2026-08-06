from scapy.layers.dot11 import Dot11

def get_bssid(pkt):
    if not pkt.haslayer(Dot11):
        return None

    FCfield = pkt[Dot11].FCfield
    to_ds = FCfield & 0x1
    from_ds = (FCfield & 0x2) >> 1

    if to_ds == 0 and from_ds == 0:
        return pkt[Dot11].addr3
    elif to_ds == 1 and from_ds == 0:
        return pkt[Dot11].addr1
    elif to_ds == 0 and from_ds == 1:
        return pkt[Dot11].addr2
    elif to_ds == 1 and from_ds == 1:
        return pkt[Dot11].addr3
        
    return pkt[Dot11].addr3  
