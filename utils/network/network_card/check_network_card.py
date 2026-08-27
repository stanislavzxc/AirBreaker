from errors import NetworkCardNotFoundError
from state import app_state


def check_network_card() -> str: 
    if not app_state.current_card:
        raise NetworkCardNotFoundError()
    return app_state.current_card
