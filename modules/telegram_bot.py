from configuration import Config
from modules.db import Chat
from modules.db import Message
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from modules.db import User
from services.chatgpt import ChatGPTGenerateResponseService
from services.db import DatabaseServices
from services.telegram_services import TelegramBotHandlerService


class TelegramBot:

    @staticmethod
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await update.message.reply_text('Hi man')
        except Exception as ex:
            await update.get_bot().sendMessage(chat_id=update.message.chat.id, text=str(ex))

    @staticmethod
    async def set_scope_command(update: Update, context):
        await TelegramBotHandlerService(update, context).set_scope()

    @staticmethod
    async def set_prompt_command(update, context):
        await TelegramBotHandlerService(update, context).set_prompt()

    @staticmethod
    async def handle_message(update: Update, context):
        DatabaseServices().add_message(update.message)
        await TelegramBotHandlerService(update, context).handle()

    @staticmethod
    async def error(update, context):
        print(f'Update {update} caused error {context.error}')

    @staticmethod
    def start():
        print('starting')
        app = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler('start', TelegramBot.start_command))
        app.add_handler(CommandHandler('set_scope', TelegramBot.set_scope_command))
        app.add_handler(CommandHandler('set_prompt', TelegramBot.set_prompt_command))
        app.add_handler(MessageHandler(filters.ALL, TelegramBot.handle_message))
        app.add_error_handler(TelegramBot.error)
        print('polling...')
        app.run_polling(poll_interval=3)
