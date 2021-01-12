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
        subgroups = await Subgroup.query.gino.all()
        return subgroups

    async def select_subgroup_by_id(self, id: int):
        subgroup = await Subgroup.get(id)
        return subgroup if subgroup else False

    async def select_subgroups_in_group(self, group_id: int):
        subgroups = await Subgroup.query.where(Subgroup.group_id == group_id).gino.all()
        return subgroups

    async def select_subgroups_from_associations(self, associations):
        subgroups = list()
        if associations:
            for association in associations:
                subgroup = await Subgroup().select_subgroup_by_id(association.subgroup_id)
                if subgroup:
                    subgroups.append(subgroup)
        else: return False
        return subgroups


class AssociationSubgroup(db.Model):
    __tablename__ = 'association_subgroups'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    subgroup_id = db.Column(db.Integer(), db.ForeignKey('subgroups.id', ondelete='CASCADE'), primary_key=True)
    subgroup = relationship("Subgroup")

    async def select_asscociation(self, subgroup_id: int, user_id: int):
        association = await AssociationSubgroup.query.where(AssociationSubgroup.subgroup_id == subgroup_id and AssociationSubgroup.user_id == user_id).gino.first()
        return association if association else False

    async def create_or_delete_association(self, subgroup_id: int, user_id: int):
        association = await AssociationSubgroup().select_asscociation(subgroup_id, user_id)
        if not association:
            association = await AssociationSubgroup.create(user_id=user_id, subgroup_id=subgroup_id)
            return association if association else False
        else:
            await association.delete()
