from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

from app.schemas.enums import SenderEnum


class MessageIn(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: SenderEnum


class Metadata(BaseModel):
    word_count: int
    character_count: int
    processed_at: datetime


class MessageOut(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: Literal["user", "system"]
    metadata: Metadata


class MessageResponse(BaseModel):
    status: Literal["success"]
    data: MessageOut

class MessageListResponse(BaseModel):
    status: Literal["success"]
    data: list[MessageOut]



class ErrorResponse(BaseModel):
    status: Literal["error"]
    error: dict
