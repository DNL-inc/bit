import enum

from sqlalchemy import sql
from sqlalchemy.orm import relationship
from utils.db_api import db
from models.user import User


class Role(enum.Enum):
    odinary = 'odinary'
    improved = 'improved'
    supreme = 'supreme'


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer(), primary_key=True)
    user = relationship("User")
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role = db.Column(db.Enum(Role), nullable=True)
    group = db.Column(db.Integer(), db.ForeignKey(
        'groups.id', ondelete='SET NULL'), nullable=True)
    faculty = db.Column(db.Integer(), db.ForeignKey(
        'faculties.id', ondelete='SET NULL'), nullable=True)

    async def select_all_admins(self):
        admins = await self.query.gino.all()
        return admins

    async def select_admin_by_tele_id(self, tele_id: int):
        user = await User().select_user_by_tele_id(tele_id)
        if user:
            admin = await Admin.query.where(self.user_id == user.id).gino.first()
            return admin if admin else False