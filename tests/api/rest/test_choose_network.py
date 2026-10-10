import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from models import WifiNetworkModel
from routers import current_network_router
from state import app_state

app = FastAPI()
app.include_router(current_network_router)

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_state():
    app_state.current_network = WifiNetworkModel(
        wpa="none",
        ssid="none",
        bssid="00:00:00:00:00:00",
        rssi=0,
        channel=1,
        data_bytes=0,
        clients_mac=[]
    )

def test_set_network():
    network = {
        "wpa": 'str',
        "ssid": 'str',
        "bssid": 'str',
        "rssi":  1,
        "channel": 1,
        "data_bytes": 0, 
        "clients_mac": ['asd','asd'] 
    }
    response = client.post('/network/current', json=network)

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert app_state.current_network.wpa == 'str' 
