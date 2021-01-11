from sqlalchemy import sql
from sqlalchemy.orm import relationship
from utils.db_api import db


class Faculty(db.Model):
    __tablename__ = 'faculties'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    groups = relationship("Group", back_populates="group")

    query: sql.Select

    async def select_all_faculties(self):
        faculties = await Faculty().query.gino.all()
        return faculties
