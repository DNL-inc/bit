from tortoise import fields
from tortoise.models import Model


class Notification(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', on_delete="CASCADE")
    event = fields.ForeignKeyField('models.Event', on_delete="CASCADE")
