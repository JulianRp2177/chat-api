import pytest
from datetime import datetime
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

BASE_URL = "/api/messages"
client = TestClient(app)

AUTH_HEADER = {"X-API-Key": f"{settings.API_KEY}"}


class TestSearchMessages:
    message = {
        "message_id": "msg1",
        "session_id": "session1",
        "content": "hola mundo",
        "timestamp": "2025-07-29T23:41:26.373Z",
        "sender": "user",
        "metadata": {
            "word_count": 2,
            "character_count": 10,
            "processed_at": datetime.utcnow().isoformat()
        }
    }

    @pytest.mark.asyncio
    @patch("app.api.endpoints.message.message_repository.search_messages", new_callable=AsyncMock)
    async def test_search_messages_success(self, mock_search_messages):
        mock_search_messages.return_value = [self.message]

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f"{BASE_URL}/search",
                params={"query": "hola"},
                headers=AUTH_HEADER
            )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert isinstance(data["data"], list)
        assert "metadata" in data["data"][0]

    @pytest.mark.asyncio
    @patch("app.api.endpoints.message.message_repository.search_messages", new_callable=AsyncMock)
    async def test_search_messages_empty(self, mock_search_messages):
        mock_search_messages.return_value = []

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f"{BASE_URL}/search",
                params={"query": "inexistente"},
                headers=AUTH_HEADER
            )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"] == []

    @pytest.mark.asyncio
    @patch("app.api.endpoints.message.message_repository.search_messages", new_callable=AsyncMock)
    async def test_search_messages_internal_error(self, mock_search_messages):
        mock_search_messages.side_effect = Exception("DB Error")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f"{BASE_URL}/search",
                params={"query": "hola"},
                headers=AUTH_HEADER
            )

        assert response.status_code == 500


class TestGetMessages:
    message = {
        "message_id": "msg1",
        "session_id": "session1",
        "content": "hola mundo",
        "timestamp": "2025-07-29T23:41:26.373Z",
        "sender": "user",
        "metadata": {
            "word_count": 2,
            "character_count": 10,
            "processed_at": datetime.utcnow().isoformat()
        }
    }

    @pytest.mark.asyncio
    @patch("app.api.endpoints.message.message_repository.get_messages", new_callable=AsyncMock)
    async def test_get_messages_success(self, mock_get_messages):
        mock_get_messages.return_value = [self.message]

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"{BASE_URL}/session/session1", headers=AUTH_HEADER)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert isinstance(data["data"], list)
        assert "metadata" in data["data"][0]

    @pytest.mark.asyncio
    @patch("app.api.endpoints.message.message_repository.get_messages", new_callable=AsyncMock)
    async def test_get_messages_empty(self, mock_get_messages):
        mock_get_messages.return_value = []

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"{BASE_URL}/session/session1", headers=AUTH_HEADER)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"] == []

    @pytest.mark.asyncio
    @patch("app.api.endpoints.message.message_repository.get_messages", new_callable=AsyncMock)
    async def test_get_messages_internal_error(self, mock_get_messages):
        mock_get_messages.side_effect = Exception("DB Error")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"{BASE_URL}/session/session1", headers=AUTH_HEADER)

        assert response.status_code == 500


class TestReceiveMessage:
    payload = {
        "message_id": "msg1",
        "session_id": "session1",
        "content": "hola mundo",
        "timestamp": "2025-07-29T23:41:26.373Z",
        "sender": "user"
    }

    metadata = {
        "word_count": 2,
        "character_count": 10,
        "processed_at": datetime.utcnow().isoformat()
    }

    message_out = {
        **payload,
        "metadata": metadata
    }

    @pytest.mark.asyncio
    @patch("app.api.endpoints.message.message_repository.process_and_store_message", new_callable=AsyncMock)
    async def test_receive_message_success(self, mock_process_and_store):
        mock_process_and_store.return_value = self.message_out

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(BASE_URL, json=self.payload, headers=AUTH_HEADER)

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert "metadata" in data["data"]

    @pytest.mark.asyncio
    @patch("app.api.endpoints.message.message_repository.process_and_store_message", new_callable=AsyncMock)
    async def test_receive_message_bad_request(self, mock_process_and_store):
        mock_process_and_store.side_effect = ValueError("Invalid content")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(BASE_URL, json=self.payload, headers=AUTH_HEADER)

        assert response.status_code == 400

    @pytest.mark.asyncio
    @patch("app.api.endpoints.message.message_repository.process_and_store_message", new_callable=AsyncMock)
    async def test_receive_message_internal_error(self, mock_process_and_store):
        mock_process_and_store.side_effect = Exception("DB Error")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(BASE_URL, json=self.payload, headers=AUTH_HEADER)

        assert response.status_code == 500
