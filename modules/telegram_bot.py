from configuration import Config
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from services.telegram_services import TelegramBotHandlerService


class TelegramBot:

    @staticmethod
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hi man')

    @staticmethod
    async def set_scope_command(update: Update, context):
        await TelegramBotHandlerService(update, context).set_scope()

    @staticmethod
    async def set_prompt_command(update, context):
        await TelegramBotHandlerService(update, context).set_prompt()

    @staticmethod
    async def get_settings_command(update, context):
        await TelegramBotHandlerService(update, context).get_settings()

    @staticmethod
    async def help(update, context):
        await TelegramBotHandlerService(update, context).help()

    @staticmethod
    async def handle_message(update: Update, context):
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
        app.add_handler(CommandHandler('get_settings', TelegramBot.get_settings_command))
        app.add_handler(CommandHandler('help', TelegramBot.help))
        app.add_handler(MessageHandler(filters.ALL, TelegramBot.handle_message))
        app.add_error_handler(TelegramBot.error)
        print('polling...')
        app.run_polling(poll_interval=3)
