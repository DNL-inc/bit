from tortoise.models import Model
from tortoise import fields

class Chat(Model):
    id = fields.IntField(pk=True)
    creator = fields.ForeignKeyField('models.User', on_delete="CASCADE")
    group = fields.ForeignKeyField('models.Group', on_delete="CASCADE")
    tele_id = fields.IntField(unique=True)

    class Meta:
        table = 'chats'

    async def select_chats_by_creator(self, creator_id: int):
        chats = await Chat.filter(creator=creator_id).all()
        return chats if chats else False
