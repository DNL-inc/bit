from sqlalchemy import create_engine, Table, Integer, String, Column, ForeignKey, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import exists
from menu import get_main_menu
from datetime import time
from config import config


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

    def __init__(self, tele_id=None, username=None, firstname=None, lastname=None, group=None, is_admin=None):
        self.tele_id = tele_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.group = group
        self.is_admin = is_admin

    def __repr__(self):
        return "<User('%s')>" % (self.tele_id)

    def to_dict(self):
        return dict({
            'tele_id': self.tele_id,
            'username': self.username,
            'firstname': self.lastname,
            'is_admin': self.is_admin,
            'group': self.group,
        })


class Admin(Base):

    __tablename__ = "admins"
    id = Column('id', Integer, primary_key=True)
    tele_id = Column('tele_id', Integer, unique=True)
    group = Column('group', ForeignKey('groups.id'))
    is_supreme = Column('is_supreme', Boolean)

    def __init__(self, tele_id=None, username=None, firstname=None, lastname=None, group=None):
        self.tele_id = tele_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.group = group

    def __repr(self):
        return "<Admin('%s')" % (self.tele_id)

    def to_dict(self):
        return dict({
            'tele_id': self.tele_id,
            'is_supreme': self.is_supreme,
            'group': self.group,
        })



class Group(Base):

    __tablename__ = "groups"
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, unique=True)
    course = Column('course', Integer)
    students = relationship("User")
    faculty = Column('faculty', ForeignKey('faculties.id'))

    def __init__(self, title=None, faculty=None, course=None):
        self.title = title
        self.faculty = faculty
        self.course = course

    def __repr(self):
        return "<Group('%s')" % (self.id)

    def to_dict(self):
        return dict({
            'title': self.title,
            'course': self.course,
            'faculty': self.faculty,
        })


class Faculty(Base):
    __tablename__ = 'faculties'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, unique=True)
    groups = relationship('Group')

    def __init__(self, title=None):
        self.title = title
    
    def __repr(self):
        return "<Faculty('%s')" % (self.id)

    def to_dict(self):
        return dict({
            'title': self.title,
        })

class Event(Base):
    __tablename__ = 'events'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    group = Column('group', ForeignKey('groups.id'))
    day = Column('day', String)
    time_start = Column('time_start', Time)

    def __init__(self, title=None, group=None, day=None, time_start=None):
        self.title = title
        self.group = group
        self.day = day
        self.time_start = time_start

    def __repr(self):
        return "<Event('%s')" % (self.id)

    def to_dict(self):
        return dict({
            'id': self.id,
            'title': self.title,
            'group': self.day,
            'time_start': self.time_start,
            'day': self.day,
        })

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

def get_user(message):
    tele_id = message.from_user.id
    if session.query(exists().where(User.tele_id == tele_id)).scalar():
        return session.query(User).filter(User.tele_id == tele_id).first()

def get_fac(id):
    fac = session.query(Faculty).filter(Faculty.id == id).first()
    return fac.title

def register_fac(message):
    title = message.text

    fac = Faculty(title)
    if session.query(exists().where(Faculty.title == title)).scalar():
        return False
    session.add(fac)
    session.commit()
    return True

def delete_fac(message):
    id = message.data.split('-')[-1]
    print(id)

    fac = session.query(Faculty).filter(Faculty.id == id).first()
    session.delete(fac)
    session.commit()

def edit_fac(message, id):
    title = message.text

    fac = session.query(Faculty).filter(Faculty.id == id).first()
    if session.query(exists().where(Faculty.title == title)).scalar():
        return False
    fac.title = title
    session.commit()
    return True


def register_group(title, faculty, course):
    group = Group(title, faculty, course)
    if session.query(exists().where(Group.title == title)).scalar():
        return False
    session.add(group)
    session.commit()
    return True

def delete_group(message):
    id = message.data.split('-')[-1]
    group = session.query(Group).filter(Group.id == id).first()

    session.delete(group)
    session.commit()

def edit_group(title, id):
    #title = message.text

    group = session.query(Group).filter(Group.id == id).first()
    if session.query(exists().where(Group.title == title)).scalar():
        return False
    group.title = title
    session.commit()
    return True

def get_group(id):
    group = session.query(Group).filter(Group.id == id).first()
    return group.title

def save_group_user(message, group):
    user = session.query(User).filter(
        User.tele_id == message.from_user.id).first()
    if user.group == int(group):
        user.group = None
    else: user.group = group
    session.commit()

def register_event(message, title, time_start, day):
    time_start = list(map(int, time_start.split(':')))
    group = session.query(User).filter(User.tele_id == message.from_user.id).first().group

    event = Event(title, group, day, time(time_start[0], time_start[1]))
    session.add(event)
    session.commit()
    return True

def delete_event(message, event):
    event = session.query(Event).filter(Event.id == event.id).first()
    if not event:
        return False
    session.delete(event)
    session.commit()
    return True

def edit_event(message, changes):
    event = session.query(Event).filter(Event.id == changes['id']).first()
    if not event:
        return False

    if changes.get('time_start'):
        time_start = list(map(int, changes.get('time_start').split(':')))
        if time_start != time(time_start[0], time_start[1]):
            event.time_start = time(time_start[0], time_start[1])
    if changes.get('title') and changes.get('title') != event.title:
        event.title = changes.get('title')
    session.commit()
    return True
    

if __name__ == "__main__":
    Base.metadata.create_all(engine)
