from modules.db import Chat
from modules.db import Message
from modules.db import User
from modules import session
from sqlalchemy.orm.attributes import flag_modified


class DatabaseServices:

    def add_message(self, message):
        u = message.from_user
        chat = Chat.get_or_create(id=message.chat.id) #self.get_or_create(Chat, id=message.chat.id)
        user = User.get_or_create(id=u.id, username=u.username, first_name=u.first_name, last_name=u.last_name) #self.get_or_create(User, **telegram_user_data)
        Message.create(id=message.id, chat_id=chat.id, user_id=user.id, text=message.text, scope=chat.scope)
