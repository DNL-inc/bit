from tortoise.models import Model
from tortoise import fields


class Group(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(255)
    course = fields.IntField()
    faculty = fields.ForeignKeyField('models.Faculty', on_delete="CASCADE")

    class Meta:
        table = 'groups'

    async def select_all_groups(self):
        groups = await Group.all()
        return groups

    async def select_groups_by_filters(self, args: dict):
        groups = await Group.filter(**args).all()
        return groups if groups else False
