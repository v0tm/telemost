from modules.database import session
from modules.models import Chat, Message, User
from telegram import Message as TelegramMessage
from sqlalchemy.exc import IntegrityError, PendingRollbackError


class DatabaseServices:

    def add_message(self, message: TelegramMessage, scope=None) -> None:
        """
        Save the message in the database.

        :param message: The message to save.
        :param scope: Custom scope (for example for storing command logs).
        :return: None
        """
        try:
            topic = message.message_thread_id if message.is_topic_message else None
            u = message.from_user
            chat = Chat.get_or_create(id=message.chat.id, name=message.chat.title)
            user = User.get_or_create(id=u.id, username=u.username, first_name=u.first_name, last_name=u.last_name)
            Message.create(message_id=message.id, chat_id=chat.id, user_id=user.id, text=message.text,
                           scope=scope or chat.scope, topic=topic)
        except (IntegrityError, PendingRollbackError) as ex:
            error_message = ex.args[0] if len(ex.args) > 0 else ex.__class__.__name__
            print(f'ERROR WITH SAVING THE MESSAGE, ROLLING BACK... ({error_message})')
            session.rollback()
