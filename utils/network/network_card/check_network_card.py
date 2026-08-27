from state import app_state
from errors import NetworkCardNotFoundError

def check_network_card() -> str: 
    if not app_state.current_card:
        raise NetworkCardNotFoundError()
    return app_state.current_card