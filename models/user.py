from tortoise import fields
from tortoise.models import Model

from models.subgroup import Subgroup


class User(Model):
    id = fields.IntField(pk=True)
    tele_id = fields.IntField(unique=True)
    username = fields.CharField(255, unique=True, null=True)
    firstname = fields.CharField(255, null=True)
    lastname = fields.CharField(255, null=True)
    lang = fields.CharField(2, null=True)
    group = fields.ForeignKeyField(
        'models.Group', on_delete='SET NULL', null=True, related_name='users')
    subgroups = fields.ManyToManyField('models.Subgroup')
    welcome_message_id = fields.IntField()

    class Meta:
        table = 'users'

    async def select_all_users(self):
        users = await User.all()
        return users

    async def select_user_by_tele_id(self, tele_id: int):
        user = await User.filter(tele_id=tele_id).first()
        return user if user else False

    async def create_user(self, tele_id: int, welcome_message_id, username=None, firstname=None, lastname=None):
        user = await User().select_user_by_tele_id(tele_id)
        if not user:
            user = await User.create(
                tele_id=tele_id,
                username=username,
                firstname=firstname,
                lastname=lastname,
                welcome_message_id=welcome_message_id
            )
            return user if user else False
        else:
            return False

    async def select_user_subgroups(self, user):
        subgroups = await user.subgroups.all()
        return subgroups if subgroups else False

    async def update_user(self, tele_id: int, username=None, firstname=None, lastname=None, lang=None, group=None):
        user = await User().select_user_by_tele_id(tele_id)
        if user:
            if username:
                user.username = username
            if firstname:
                user.firstname = firstname
            if lastname:
                user.lastname = lastname
            if lang:
                user.lang = lang
            if group:
                user.group_id = group
            await user.save()
        else:
            return False

    async def delete_user(self, tele_id):
        user = await User().select_user_by_tele_id(tele_id)
        if user:
            await user.delete()
        else:
            return False

    async def add_or_clear_subgroup(self, subgroup_id, user):
        association = await user.subgroups.filter(id=subgroup_id).first()
        if association:
            await user.subgroups.remove(association)
        else:
            subgroup = await Subgroup().select_subgroup_by_id(subgroup_id)
            if subgroup:
                await user.subgroups.add(subgroup)

    async def set_language(self, tele_id, lang):
        user = await User().select_user_by_tele_id(tele_id)
        await user.update(lang=lang).apply()
