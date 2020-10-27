from sqlalchemy import create_engine, Table, Integer, String, Column, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

    def __init__(self, tele_id, username=None, firstname=None, lastname=None, group=None, is_admin=None):
        self.tele_id = tele_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.group = group
        self.is_admin = is_admin

    def __repr__(self):
        return "<User('%s')>" % (self.username)


def register_user(message):
    username = message.from_user.username
    tele_id = message.from_user.id
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    is_admin = None

    # check if user is in admin list

    user = User(tele_id, username, firstname, lastname, is_admin=is_admin)
    if session.query(User).filter(User.tele_id == tele_id).first():
        return
    session.add(user)
    session.commit()

if __name__ == "__main__":
    Base.metadata.create_all(engine)

