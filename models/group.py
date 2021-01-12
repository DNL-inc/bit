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
        groups = await Group.query.gino.all()
        return groups

    async def select_groups_by_filters(self, args: dict):
        filters = self.__get_filters_by_args(args)
        for filter in filters:
            groups = await Group.query.where(filter).gino.all()
        return groups if groups else False

    def __get_filters_by_args(self, args: dict):
        filters = []
        for key, value in args.items():
            filters.append(getattr(Group, key) == int(value))
        return filters

    