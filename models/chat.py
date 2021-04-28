from tortoise.models import Model
from tortoise import fields


class Chat(Model):
    id = fields.BigIntField(pk=True)
    title = fields.CharField(255)
    creator = fields.ForeignKeyField('models.User', on_delete="CASCADE")
    group = fields.ForeignKeyField('models.Group', on_delete="SET NULL", null=True)
    notification = fields.BooleanField(default=False)
    notification_time = fields.IntField(default=0)
    tele_id = fields.IntField(unique=True)
    lang = fields.CharField(2, null=True, default='ua')

    class Meta:
        table = 'chats'

    async def select_chats_by_creator(self, creator_id: int):
        chats = await Chat.filter(creator=creator_id).all()
        return chats if chats else False
