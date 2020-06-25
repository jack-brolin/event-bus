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


class UserPermission(Base):
    __tablename__ = "user_permission"

    username = Column(String(300), primary_key=True, nullable=False)
    permission = Column(String(300))

    def __init__(self, username, permission):
        self.username = username
        self.permission = permission

    @classmethod
    def find_by_username(cls, username):
        return session.query(cls).filter_by(username=username).first()

    def save_to_db(self):
        session.add(self)
        session.commit()
