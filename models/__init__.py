import enum

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


class Role(enum.Enum):
    odinary = 'odinary'
    improved = 'improved'
    supreme = 'supreme'


class Admin(Model):

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', on_delete="CASCADE")
    role = fields.CharEnumField(Role, null=True)
    group = fields.ForeignKeyField(
        'models.Group', on_delete='SET NULL', null=True)
    faculty = fields.ForeignKeyField(
        'models.Faculty', on_delete='SET NULL', null=True)

    async def select_all_admins(self):
        admins = await Admin.all()
        return admins

    async def select_admin_by_user_id(self, user_id: int):
        admin = await Admin.filter(user = user_id).first()
        return admin if admin else False


class Faculty(Model):

    id = fields.IntField(pk=True)
    title = fields.CharField(255)

    class Mеta:
        table = 'faculties'

    async def select_all_faculties(self):
        faculties = await Faculty.all()
        return faculties


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
        subgroups = await Subgroup.filter(group_id = group_id).all()
        return subgroups

    async def select_user_subgroups(self, user):
        subgroups = list()

        if associations:
            for association in associations:
                subgroup = await Subgroup().select_subgroup_by_id(association.subgroup_id)
                if subgroup:
                    subgroups.append(subgroup)
        else:
            return False
        return subgroups


class User(Model):
    id = fields.IntField(pk=True)
    tele_id = fields.IntField(unique=True)
    username = fields.CharField(255, unique=True, null=True)
    firstname = fields.CharField(255, null=True)
    lastname = fields.CharField(255, null=True)
    lang = fields.CharField(255, null=True)
    group = fields.ForeignKeyField(
        'models.Group', on_delete='SET NULL', null=True, related_name='users')
    subgroups = fields.ManyToManyField('models.Subgroup')

    class Meta:
        table = 'users'

    async def select_all_users(self):
        users = await User.all()
        return users

    async def select_user_by_tele_id(self, tele_id: int):
        user = await User.filter(tele_id=tele_id).first()
        return user if user else False

    async def create_user(self, tele_id: int, username=None, firstname=None, lastname=None):
        user = await User().select_user_by_tele_id(tele_id)
        if not user:
            user = await User.create(
                tele_id=tele_id,
                username=username,
                firstname=firstname,
                lastname=lastname,
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

