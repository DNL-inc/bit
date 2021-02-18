import enum

from tortoise import fields
from tortoise.models import Model

from models.user import User


class Role(enum.Enum):
    ordinary = 'ordinary'
    improved = 'improved'
    supreme = 'supreme'


class Admin(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', on_delete="CASCADE")
    role = fields.CharEnumField(Role, null=True)
    group = fields.ForeignKeyField(
        'models.Group', on_delete='SET NULL', null=True)
    faculty = fields.ForeignKeyField(
        "models.Faculty", on_delete='SET NULL', null=True)

    async def select_all_admins(self):
        admins = await Admin.all()
        return admins

    async def select_admin_by_user_id(self, user_id: int):
        admin = await Admin.filter(user=user_id).first()
        return admin if admin else False

    async def select_admin_by_tele_id(self, tele_id: int):
        user = await User().select_user_by_tele_id(tele_id)
        if user:
            admin = await Admin().select_admin_by_user_id(user.id)
            return admin if admin else False

    async def is_admin_exists(self, user_id: int):
        return Admin.filter(user=user_id).exists()

    async def has_access(self, operation: str, admin):
        if admin.role.name == 'ordinary' and operation in ['msg-sender', 'edit-subjects', 'edit-events',
                                                           'edit-subgroups']:
            return True
        elif admin.role.name == 'improved' and operation in ['msg-sender', 'edit-admins', 'edit-groups']:
            return True
        elif admin.role.name == 'supreme' and operation in ['msg-sender', 'edit-admins', 'edit-faculties',
                                                            'edit-groups']:
            return True
        return False
