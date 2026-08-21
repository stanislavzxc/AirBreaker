from schemas import WifiNetworkModel


class AppState:
    def __init__(self):
        self.current_card: str | None = "wlp3s0" #mock
        self.current_channel: int = 1
        self.current_network : WifiNetworkModel

app_state = AppState()
