from utils.network import DeauthPackets
from scapy.all import *

class Handshake():
    def __init__(self, type):
        self.type = type

    def start_catching(self):
        deauth = DeauthPackets()
        

    