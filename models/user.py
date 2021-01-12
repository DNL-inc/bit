from sqlalchemy import sql
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from utils.db_api import db
from models.subgroup import AssociationSubgroup

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    tele_id = db.Column(db.Integer(), unique=True)
    username = db.Column(db.String(), unique=True, nullable=True)
    firstname = db.Column(db.String(), nullable=True)
    lastname = db.Column(db.String(), nullable=True)
    lang = db.Column(db.String(), nullable=True)
    group = db.Column(db.Integer(), db.ForeignKey('groups.id', ondelete='SET NULL'), nullable=True)
    subgroups = relationship('AssocationSubgroup')

    query: sql.Select

    async def select_all_users(self):
        users = await User.query.gino.all()
        return users

    async def select_user_by_tele_id(self, tele_id: int):
        user = await User.query.where(User.tele_id == tele_id).gino.first()
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
        else: return False

    async def select_user_subgroups(self, user):
        subgroups = await AssociationSubgroup.query.where(AssociationSubgroup.user_id == user.id).gino.all()
        return subgroups if subgroups else False
    
    async def update_user(self, tele_id: int, username=None, firstname=None, lastname=None, lang=None, group=None):
        user = await User().select_user_by_tele_id(tele_id)
        if user:
            await user.update(
                username=username,
                firstname=firstname,
                lastname=lastname,
                lang=lang,
                group=int(group)
            ).apply()
        else: return False

    async def delete_user(self, tele_id):
        user = await User().select_user_by_tele_id(tele_id)
        if user: await user.delete()
        else: return False