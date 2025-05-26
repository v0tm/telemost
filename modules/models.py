from sqlalchemy import ForeignKey, Column, String, Integer
from sqlalchemy.orm import relationship

from utils.mixins import BaseDBOperationsMixin
from modules.database import Base


class User(BaseDBOperationsMixin, Base):
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)

    def __init__(self, id, username, first_name, last_name):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class Chat(BaseDBOperationsMixin, Base):
    __tablename__ = 'chats'

    id = Column("id", Integer, primary_key=True)
    name = Column('name', String, nullable=True, default=None)
    prompt = Column('prompt', String, nullable=True, default=None)
    scope = Column('scope', String, nullable=False, default='default')

    def __init__(self, id, name=None):
        self.id = id
        self.name = name


class Message(BaseDBOperationsMixin, Base):
    __tablename__ = 'messages'

    id = Column("id", Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column('text', String)
    scope = Column('scope', String)
    topic = Column('topic', Integer)

    user = relationship("User", backref="messages")

    def __init__(self, id, chat_id, user_id, text, scope=None, topic=None):
        self.id = id
        self.chat_id = chat_id
        self.user_id = user_id
        self.text = text
        self.scope = scope
        self.topic = topic

