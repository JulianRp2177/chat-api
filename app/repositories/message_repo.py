from app.models.message import Message
from datetime import datetime


class MessageRepository:
    async def save_message(self, data: dict) -> Message:
        try:
            message = await Message.create(**data)
            return message
        except Exception as e:
            raise ValueError(f"Error saving message: {str(e)}")

    async def get_messages_by_session(
        self,
        session_id: str,
        limit: int = 10,
        offset: int = 0,
        sender: str | None = None
    ):
        query = Message.filter(session_id=session_id)
        if sender:
            query = query.filter(sender=sender)
        return await query.offset(offset).limit(limit).all()

    async def search_messages(self, query: str, limit: int = 10) -> list[Message]:
        return await Message.filter(content__icontains=query).limit(limit).all()
