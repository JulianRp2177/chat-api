import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.ws.message_ws import router as ws_router


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(ws_router)
    return app


def test_websocket_connection_sync(test_app):
    client = TestClient(test_app)
    session_id = "test123"

    with client.websocket_connect(f"/ws/{session_id}") as websocket:
        message = "test message"
        websocket.send_text(message)
        assert websocket is not None  
