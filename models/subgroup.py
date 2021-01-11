from sqlalchemy import sql
from sqlalchemy.orm import relationship
from utils.db_api import db


class Subgroup(db.Model):
    __tablename__ = 'subgroups'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    group_id = db.Column(db.Integer(), db.ForeignKey(
        'groups.id', ondelete="CASCADE"))
    group = relationship("Group")

    async def select_all_subgroups(self):
        subgroups = await Subgroup().query.gino.all()
        return subgroups
