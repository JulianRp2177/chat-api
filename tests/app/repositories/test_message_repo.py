import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.repositories.message_repo import MessageRepository

pytestmark = pytest.mark.asyncio

class TestMessageRepository:

    @patch("app.repositories.message_repo.Message", autospec=True)
    async def test_save_message_success(self, mock_message_class):
        repo = MessageRepository()
        fake_data = {"message_id": "msg1", "content": "hello world"}

        mock_instance = MagicMock()
        mock_message_class.create = AsyncMock(return_value=mock_instance)

        result = await repo.save_message(fake_data)

        mock_message_class.create.assert_awaited_once_with(**fake_data)
        assert result == mock_instance

    @patch("app.repositories.message_repo.Message", autospec=True)
    async def test_save_message_exception(self, mock_message_class):
        repo = MessageRepository()
        fake_data = {"message_id": "msg1", "content": "hello world"}

        mock_message_class.create = AsyncMock(side_effect=Exception("DB error"))

        with pytest.raises(Exception, match="DB error"):
            await repo.save_message(fake_data)

    @patch("app.repositories.message_repo.Message", autospec=True)
    async def test_get_messages_by_session_without_sender(self, mock_message_class):
        repo = MessageRepository()

        mock_query = MagicMock()
        mock_message_class.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all = AsyncMock(return_value=["msg1", "msg2"])

        result = await repo.get_messages_by_session("session1", limit=5, offset=0)

        mock_message_class.filter.assert_called_once_with(session_id="session1")
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(5)
        mock_query.all.assert_awaited_once()
        assert result == ["msg1", "msg2"]

    @patch("app.repositories.message_repo.Message", autospec=True)
    async def test_get_messages_by_session_with_sender(self, mock_message_class):
        repo = MessageRepository()

        mock_query = MagicMock()
        mock_message_class.filter.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all = AsyncMock(return_value=["msg_user"])

        result = await repo.get_messages_by_session("session1", sender="user")

        mock_message_class.filter.assert_called_once_with(session_id="session1")
        mock_query.filter.assert_called_once_with(sender="user")
        mock_query.all.assert_awaited_once()
        assert result == ["msg_user"]

    @patch("app.repositories.message_repo.Message", autospec=True)
    async def test_search_messages_success(self, mock_message_class):
        #Given
        repo = MessageRepository()

        mock_query = MagicMock()
        mock_message_class.filter.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all = AsyncMock(return_value=["found1", "found2"])

        #When
        mock_message_class.filter.return_value.limit.return_value.all = AsyncMock(return_value=["found1", "found2"])

        result = await repo.search_messages("hola", limit=5)

        #Then
        mock_message_class.filter.assert_called_once_with(content__icontains="hola")
        mock_message_class.filter.return_value.limit.assert_called_once_with(5)
        mock_message_class.filter.return_value.limit.return_value.all.assert_awaited_once()
        assert result == ["found1", "found2"]