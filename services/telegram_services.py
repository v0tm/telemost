import random

from configuration import Config
from modules.constants import Scopes
from modules.models import Chat
from modules.models import User
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
        """
        Service for handling incoming messages.
        """
        try:
            print(f'[{self.message.id}][{self.message_type}] {self.message.from_user.username}: {self.message.text} [topic {self.message.message_thread_id}]')
            DatabaseServices().add_message(self.message)
            chance = random.random()
            mentioned = True if self.bot.name in self.text or 'хоуми' in self.text.lower() else False
            if self.message.reply_to_message and self.message.reply_to_message.from_user.id == self.bot.id:
                mentioned = True
            if 'group' in str(self.message_type) and chance > 0.05 and not mentioned:
                return
            await self.chat.send_chat_action("typing")
            topic = self.message.message_thread_id if self.message.is_topic_message else None
            text = ChatGPTGenerateResponseService(self.bot, self.chat.id).generate_response_with_narrative(topic)
            try:
                response = await self.update.get_bot().sendMessage(chat_id=self.chat.id, text=text, message_thread_id=topic,
                                                                   parse_mode='markdownV2')
            except Exception as e:
                response = await self.update.get_bot().sendMessage(chat_id=self.chat.id, text=text, message_thread_id=topic)
            print(f'[{self.message_type}] {self.bot.username}: {response.text} [to {self.message.from_user.username}]')
            DatabaseServices().add_message(response)
        except Exception as ex:
            print(ex)
            #await self.bot.sendMessage(chat_id=self.chat.id, text=str(ex))

    async def set_scope(self):
        chat = Chat.get_or_create(id=self.message.chat.id, name=self.message.chat.title)
        user = User.get_or_create(id=self.message.from_user.id)
        try:
            if len(self.context.args) != 1:
                request = f'{user.username} использовал команду неверно. Сгенерируй ответ который об этом сообщит ' \
                          f'пользователю. Правильный формат: /set_scope [название_темы] (тема без пробелов)'
            else:
                chat.update(scope=self.context.args[0])
                request = f'{user.username} успешно переключил тему чата на {self.context.args[0]}. Сгенерируй ответ ' \
                          f'который об этом сообщит пользователю и как тебе от этого кайфово'
            response = ChatGPTGenerateResponseService(self.bot, chat.id).generate_response(request)
        except Exception as ex:
            response = str(ex)
        await self.bot.sendMessage(chat_id=chat.id, text=response)

    async def set_prompt(self):
        try:
            new_prompt = None
            if len(self.context.args) > 1 and self.context.args[0] != 'default':
                new_prompt = ' '.join(self.context.args)
            chat = Chat.get_or_create(id=self.message.chat.id, name=self.message.chat.title)
            chat.update(prompt=new_prompt)
            request = f'Поприветствуй всех в своём фирменном стиле'
            response = ChatGPTGenerateResponseService(self.bot, chat.id).generate_response(request)
            await self.bot.sendMessage(chat_id=self.message.chat.id, text=response)
        except Exception as ex:
            await self.bot.sendMessage(chat_id=self.chat.id, text=str(ex))

    async def get_settings(self):
        DatabaseServices().add_message(self.message, scope=Scopes.COMMAND_USED)
        chat = Chat.get_or_create(id=self.message.chat.id, name=self.message.chat.title)
        prompt = chat.prompt or Config.DEFAULT_CHATGPT_PROMPT
        text = Config.HTML_TEMPLATE_SETTINGS_COMMAND.format(scope=chat.scope, prompt=prompt)
        await self.bot.sendMessage(chat_id=self.chat.id, text=text, parse_mode='HTML')

    async def help(self):
        await self.chat.send_chat_action("typing")
        DatabaseServices().add_message(self.message, scope=Scopes.COMMAND_USED)
        commands = "/set_scope [scope_name_without_spaces] - Установить тему в чате.\n/set_prompt [prompt text] - Установить промт в рамках чата.\n/get_settings - Посмотреть настройки чата"
        request = f'Есть документация по доступным коммандам (напишу её в конце). Я прошу тебя подготовить сообщение в котором ты своими словаим перефразируешь эту документацию, чтоб я мог скинуть пользователям все доступные команды. Документация: {commands}'
        response = ChatGPTGenerateResponseService(self.bot, self.chat.id).generate_response(request)
        await self.bot.sendMessage(chat_id=self.message.chat.id, text=response)
