from tortoise import fields
from tortoise.models import Model


class Subgroup(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(255)
    group = fields.ForeignKeyField('models.Group', on_delete="CASCADE")

    async def select_all_subgroups(self):
        subgroups = await Subgroup.all()
        return subgroups

    async def select_subgroup_by_id(self, id: int):
        subgroup = await Subgroup.filter(id=id).first()
        return subgroup if subgroup else False

    async def select_subgroups_in_group(self, group_id: int):
        subgroups = await Subgroup.filter(group_id=group_id).all()
        return subgroups

    async def select_user_subgroups(self, user):
        await user.fetch_related("subgroups")
        subgroups = user.subgroups

        if subgroups:
            return subgroups
        else:
            return False
