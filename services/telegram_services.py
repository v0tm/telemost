import random

from modules.db import Chat
from modules.db import User
from services.chatgpt import ChatGPTGenerateResponseService
from telegram import Update

from services.db import DatabaseServices


class TelegramBotHandlerService:

    def __init__(self, update: Update, context):
        self.update = update
        self.bot = self.update.get_bot()
        self.context = context
        self.chat = self.update.message.chat
        self.message = self.update.message
        self.message_type = self.update.message.chat.type
        self.text = self.update.message.text

    async def handle(self):
        try:
            chance = random.random()
            mentioned = True if self.bot.name in self.text or 'хоуми' in self.text.lower() else False
            if self.message.reply_to_message and self.message.reply_to_message.from_user.id == self.bot.id:
                mentioned = True
            if self.message_type == 'group' and chance > 0.3 and not mentioned:
                return
            await self.chat.send_chat_action("typing")
            print(f'{self.update.message.chat.id} in {self.message_type}: {self.text}')
            text = ChatGPTGenerateResponseService(self.bot, self.chat.id).generate_response_with_narrative()
            response = await self.update.get_bot().sendMessage(chat_id=self.chat.id, text=text)
            DatabaseServices().add_message(response)
        except Exception as ex:
            await self.bot.sendMessage(chat_id=self.chat.id, text=str(ex))

    async def set_scope(self):
        chat_id = Chat.get_or_create(id=self.message.chat.id)
        user = User.get_or_create(id=self.message.from_user.id)
        try:
            if len(self.context.args) != 1:
                request = f'Кратно объясни, что {user.username} использовал команду неверно. Правильный формат: ' \
                          f'/set_scope [название темы]'
            else:
                chat = Chat.get_or_create(id=chat_id)
                chat.update(scope=self.context.args[0])
                request = f'Кратно сообщи, что {user.username} успешно переключил тему чата на {self.context.args[0]} и ' \
                          f'как тебе от этого кайфово'
            response = ChatGPTGenerateResponseService(self.bot, chat_id).generate_response(request)
        except Exception as ex:
            response = str(ex)
        await self.bot.sendMessage(chat_id=chat_id, text=response)

    async def set_prompt(self):
        try:
            new_prompt = None
            if len(self.context.args) > 1 or self.context.args[0] != 'default':
                new_prompt = ' '.join(self.context.args)
            chat = Chat.get_or_create(id=self.message.chat.id)
            chat.update(prompt=new_prompt)
            request = f'Поприветствуй всех в своём фирменном стиле'
            response = ChatGPTGenerateResponseService(self.bot, chat.id).generate_response(request)
            await self.bot.sendMessage(chat_id=self.message.chat.id, text=response)
        except Exception as ex:
            await self.bot.sendMessage(chat_id=self.chat.id, text=str(ex))
