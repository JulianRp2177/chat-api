from tortoise import fields
from tortoise.models import Model
from app.schemas.enums import SenderEnum


class Message(Model):
    message_id = fields.CharField(max_length=100, pk=True)
    session_id = fields.CharField(max_length=100)
    content = fields.TextField()
    timestamp = fields.DatetimeField()
    sender = fields.CharEnumField(enum_type=SenderEnum)
    word_count = fields.IntField(null=True)
    character_count = fields.IntField(null=True)
    processed_at = fields.DatetimeField(null=True)

    class Meta:
        table = "messages"
        app_label = "models"
