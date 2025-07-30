from datetime import datetime, timezone
from app.schemas.message import MessageIn, MessageOut, Metadata
from app.repositories.message_repo import MessageRepository
from app.utils.message_utils import contains_prohibited_words, generate_metadata
from app.api.ws.message_ws import active_connections


class MessageService:
    """
    Service layer to handle business logic for messages:
    - Validates content
    - Extracts metadata
    - Interacts with the repository layer
    """

    def __init__(self, repository: MessageRepository):
        self.repository = repository

    async def process_and_store_message(self, payload: MessageIn) -> MessageOut:
        if contains_prohibited_words(payload.content):
            raise ValueError("Message contains inappropriate language")

        metadata = generate_metadata(payload.content)

        data: dict = payload.model_dump()
        data.update(metadata)

        saved = await self.repository.save_message(data)

        result = MessageOut(
            message_id=saved.message_id,
            session_id=saved.session_id,
            content=saved.content,
            timestamp=saved.timestamp,
            sender=saved.sender,
            metadata=Metadata(**metadata)
        )

        if payload.session_id in active_connections:
            for ws in active_connections[payload.session_id]:
                await ws.send_json({
                    "event": "new_message",
                    "data": result.model_dump()
                })

        return result

    async def get_messages(
        self, session_id: str, limit: int = 10, offset: int = 0, sender: str | None = None
    ) -> list[MessageOut]:
        messages = await self.repository.get_messages_by_session(
            session_id, limit, offset, sender
        )

        result = []
        for msg in messages:
            result.append(
                MessageOut(
                    message_id=msg.message_id,
                    session_id=msg.session_id,
                    content=msg.content,
                    timestamp=msg.timestamp,
                    sender=msg.sender,
                    metadata={
                        "word_count": msg.word_count,
                        "character_count": msg.character_count,
                        "processed_at": msg.processed_at,
                    },
                )
            )
        return result

    async def search_messages(self, query: str, limit: int = 10) -> list[MessageOut]:
        messages = await self.repository.search_messages(query, limit)
        result = []
        for msg in messages:
            result.append(
                MessageOut(
                    message_id=msg.message_id,
                    session_id=msg.session_id,
                    content=msg.content,
                    timestamp=msg.timestamp,
                    sender=msg.sender,
                    metadata={
                        "word_count": msg.word_count,
                        "character_count": msg.character_count,
                        "processed_at": msg.processed_at,
                    },
                )
            )
        return result


message_repository = MessageService(MessageRepository())
