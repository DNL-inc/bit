from sqlalchemy import sql
from utils.db_api import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    tele_id = db.Column(db.Integer(), unique=True)
    username = db.Column(db.String(), unique=True, nullable=True)
    firstname = db.Column(db.String(), nullable=True)
    lastname = db.Column(db.String(), nullable=True)
    lang = db.Column(db.String(), nullable=True)

    query: sql.Select

    async def select_all_users(self):
        users = await User().query.gino.all()
        return users

    async def select_user_by_tele_id(self, tele_id: int):
        user = await User().query.where(self.tele_id == tele_id).gino.first()
        return user if user else False
