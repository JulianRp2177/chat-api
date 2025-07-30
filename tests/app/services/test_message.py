import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from app.services.message import MessageService
from app.schemas.message import MessageIn, MessageOut, Metadata


@pytest.fixture
def fake_repository():
    return AsyncMock()


@pytest.fixture
def service(fake_repository):
    return MessageService(fake_repository)


@pytest.fixture
def example_payload():
    return MessageIn(
        message_id="msg1",
        session_id="abc123",
        content="hello world",
        sender="user",  
        timestamp=datetime.now()
    )


@pytest.mark.asyncio
async def test_process_and_store_message_success(service, example_payload):
    # Given
    fake_saved = MagicMock()
    fake_saved.message_id = "msg123"
    fake_saved.session_id = "abc123"
    fake_saved.content = "hello world"
    fake_saved.timestamp = datetime.now()
    fake_saved.sender = "user"
    fake_saved.word_count = 2
    fake_saved.character_count = 10
    fake_saved.processed_at = datetime.now()

    service.repository.save_message.return_value = fake_saved

    # When
    with patch("app.services.message.active_connections", {}):
       
        result = await service.process_and_store_message(example_payload)

    # Then
    assert isinstance(result, MessageOut)
    assert result.message_id == "msg123"
    assert result.session_id == example_payload.session_id
    assert result.content == example_payload.content
    assert result.sender == example_payload.sender
    assert isinstance(result.metadata, Metadata)
    assert result.metadata.word_count == 2
    assert result.metadata.character_count == 11


@pytest.mark.asyncio
async def test_process_and_store_message_with_prohibited_words(service, example_payload):
    # Given
    example_payload.content = "forbidden_word"
    # When and Then
    with patch("app.services.message.contains_prohibited_words", return_value=True):
        with pytest.raises(ValueError, match="Message contains inappropriate language"):
            await service.process_and_store_message(example_payload)


@pytest.mark.asyncio
async def test_get_messages(service):
    # Given
    fake_msg = MagicMock()
    fake_msg.message_id = "msg1"
    fake_msg.session_id = "abc123"
    fake_msg.content = "Hola de nuevo"
    fake_msg.timestamp = datetime.now()
    fake_msg.sender = "user"
    fake_msg.word_count = 3
    fake_msg.character_count = 13
    fake_msg.processed_at = datetime.now()

    service.repository.get_messages_by_session.return_value = [fake_msg]

    # When
    result = await service.get_messages(session_id="abc123")

    # Then
    assert len(result) == 1
    assert isinstance(result[0], MessageOut)
    assert result[0].session_id == "abc123"
    assert result[0].metadata.word_count == 3


@pytest.mark.asyncio
async def test_search_messages(service):
    # Given
    fake_msg = MagicMock()
    fake_msg.message_id = "msg1"
    fake_msg.session_id = "abc123"
    fake_msg.content = "Buscando esto"
    fake_msg.timestamp = datetime.now()
    fake_msg.sender = "user"  
    fake_msg.word_count = 2
    fake_msg.character_count = 14
    fake_msg.processed_at = datetime.now()

    service.repository.search_messages.return_value = [fake_msg]

    # When
    result = await service.search_messages(query="esto")

    # Then
    assert len(result) == 1
    assert isinstance(result[0], MessageOut)
    assert result[0].sender == "user"
    assert result[0].metadata.word_count == 2
    assert result[0].metadata.character_count == 14