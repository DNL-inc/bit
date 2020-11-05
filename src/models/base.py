from sqlalchemy import create_engine, Table, Integer, String, Column, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import exists
from menu import get_main_menu

engine = create_engine("sqlite:///db.sqlite", echo=True, connect_args={'check_same_thread': False})
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
    group = Column('group', ForeignKey('groups.id'))

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
    username = Column('username', String, nullable=True)
    firstname = Column('firstname', String, nullable=True)
    lastname = Column('lastname', String, nullable=True)
    group = Column('group', ForeignKey('groups.id'))
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
    faculty = Column('faculty', ForeignKey('faculties.id'))

    def __init__(self, title, faculty, course):
        self.title = title
        self.faculty = faculty
        self.course = course

class Faculty(Base):
    __tablename__ = 'faculties'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, unique=True)
    groups = relationship('Group')

    def __init__(self, title):
        self.title = title

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


def register_fac(message):
    title = message.text

    fac = Faculty(title)
    if session.query(exists().where(Faculty.title == title)).scalar():
        return False
    session.add(fac)
    session.commit()

def register_group(message, faculty, course):
    title = message.text
    
    group = Group(title, faculty.id, course)
    if session.query(exists().where(Group.title == title)).scalar():
        return False
    session.add(group)
    session.commit()

def save_group_user(message, group):
    user = session.query(User).filter(User.tele_id == message.from_user.id).first()
    user.group = group
    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)

