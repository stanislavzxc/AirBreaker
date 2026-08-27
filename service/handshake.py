from models.enums import DeauthType
from utils.network import DeauthPackets


class Handshake():
    def __init__(self, device, attack_type):
        self.device = self.device
        self.attack_type = attack_type,

    async def start_catching(self):
        deauth = DeauthPackets()
        match self.attack_type:
            case DeauthType.ALL:
                await deauth.kill_all_users()
            case DeauthType.MANY:
                await deauth.kill_many_users()
            case DeauthType.ONE:
                await deauth.kill_one_user() 
        

    
