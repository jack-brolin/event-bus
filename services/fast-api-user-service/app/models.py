from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection resources
engine = create_engine('postgresql://EventBus:EventBus.123.@postgres:5432/eb_database')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(300))
    password = Column(String(300))
    first_name = Column(String(300))
    last_name = Column(String(300))
    permission = Column(String(300))

    def __init__(self, username, password, first_name, last_name, permission):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.permission = permission

    @classmethod
    def find_by_username(cls, username):
        return session.query(cls).filter_by(username=username).first()

    def save_to_db(self):
        session.add(self)
        session.commit()
