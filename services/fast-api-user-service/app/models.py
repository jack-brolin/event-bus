import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = 'postgresql://{username}:{password}@{host}:{port}/{db_name}'.format(
    username=os.getenv("PG_USERNAME"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    db_name=os.getenv("PG_DB_NAME")
)
engine = create_engine(url)
Session = sessionmaker(bind=engine)
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
