from tortoise.models import Model
from tortoise import fields


class Code(Model):
    key = fields.CharField(255)
    time_create = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField('models.User', on_delete="CASCADE")

    class Meta:
        table = 'codes'
