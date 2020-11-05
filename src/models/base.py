from sqlalchemy import create_engine, Table, Integer, String, Column, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import exists

engine = create_engine("sqlite:///db.sqlite", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):

    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    tele_id = Column('tele_id', Integer, unique=True)
    username = Column('username', String, unique=True, nullable=True)
    firstname = Column('firstname', String, nullable=True)
    lastname = Column('lastname', String, nullable=True)
    is_admin = Column('is_admin', Boolean, nullable=True)
    has_group = Column('has_group', ForeignKey('groups.id'))

    def __init__(self, tele_id, username=None, firstname=None, lastname=None, group=None, is_admin=None):
        self.tele_id = tele_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.group = group
        self.is_admin = is_admin

    def __repr__(self):
        return "<User('%s')>" % (self.username)

class Admin(Base):

    __tablename__ = "admins"
    id = Column('id', Integer, primary_key=True)
    tele_id = Column('tele_id', Integer, unique=True)
    username = Column('username', String, unique=True, nullable=True)
    firstname = Column('firstname', String, nullable=True)
    lastname = Column('lastname', String, nullable=True)
    has_group = Column('has_group', ForeignKey('groups.id'))
    is_supreme = Column('is_supreme', Boolean)

    def __init__(self, tele_id, username=None, firstname=None, lastname=None, group=None):
        self.tele_id = tele_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.group = group


class Group(Base):

    __tablename__ = "groups"
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, unique=True)
    course = Column('course', Integer)
    students = relationship("User")
    faculty = Column('faculty', String, nullable=True)

def is_admin_bool(message):
    if session.query(exists().where(Admin.tele_id == message.from_user.id)).scalar():
        return True
    else:
        return False

def register_user(message):
    username = message.from_user.username
    tele_id = message.from_user.id
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    is_admin = is_admin_bool(message)

    user = User(tele_id, username, firstname, lastname, is_admin=is_admin)
    if session.query(exists().where(User.tele_id == tele_id)).scalar():
        user = session.query(User).filter(User.tele_id == tele_id).first()
        if is_admin:
            user.is_admin = True
            session.commit()
        return

    session.add(user)
    session.commit()



if __name__ == "__main__":
    Base.metadata.create_all(engine)

