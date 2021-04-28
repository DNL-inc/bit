from datetime import datetime

from tortoise.models import Model
from tortoise import fields



class PostponeMessage(Model):
    id = fields.IntField(pk=True)
    creator = fields.ForeignKeyField('models.Admin', on_delete="CASCADE")
    text = fields.TextField()
    sending_time = fields.DatetimeField()

    class Meta:
        table='messages'

    async def select_messages_by_creator(self, creator_id: int):
        messages = await PostponeMessage.filter(creator=creator_id).all()
        return messages if messages else False

    async def delete_message(self, msg_id: int):
        message = await PostponeMessage.filter(id=msg_id).first()
        if message: await message.delete()

    async def create_message(self, sending_time: datetime, text: str, creator):
        await PostponeMessage.create(sending_time=sending_time, text=text, creator=creator)
