from sqlalchemy import sql
from sqlalchemy.orm import relationship
from utils.db_api import db


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    course = db.Column(db.Integer())
    faculty_id = db.Column(db.Integer, db.ForeignKey(
        'faculties.id', ondelete='CASCADE'))
    faculty = relationship("Faculty")
    subgroups = relationship("Subgroup", back_populates="subgroup")

    query: sql.Select

    async def select_all_groups(self):
        groups = await self.query.gino.all()
        return groups
