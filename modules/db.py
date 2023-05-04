from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configuration import Config

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)

    def __init__(self, _id, username, first_name, last_name):
        self.id = _id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'({self.id} {self.username})'


class Chat(Base):
    __tablename__ = 'chats'

    id = Column("id", Integer, primary_key=True)

    def __init__(self, _id):
        self.id = _id

    def __repr__(self):
        return f'({self.id})'

class Message(Base):
    __tablename__ = 'messages'

    id = Column("id", Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column('text', String)

    def __init__(self, _id, chat_id, user_id, text):
        self.id = _id
        self.chat_id = chat_id
        self.user_id = user_id
        self.text = text

    def __repr__(self):
        return f'({self.id} {self.chat_id} {self.user_id})'


engine = create_engine(Config.DB_CONNECT_PATH, echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
# user = User(1, 'test', 'test', 'test')
# session.add(user)
# session.commit()
# chat = Chat(5)
# session.add(chat)
# session.add(Message(1, chat.id, user.id, 'some text'))
# session.commit()

