from sqlalchemy import Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    nickname = Column(String, nullable=False)

class ChatRoom(Base):
    __tablename__ = 'chatrooms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    owner_id = Column(Integer)
