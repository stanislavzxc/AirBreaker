class AppState:
    def __init__(self):
        self.current_card: str | None = None
        self.current_channel: int

app_state = AppState()
