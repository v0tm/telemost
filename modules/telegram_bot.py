import openai

from configuration import Config
from modules.db import session, Message
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

token = Config.TELEGRAM_TOKEN
openai.api_key = Config.CHATGPT_TOKEN
default_prompt = """Help me to write dialogues with discord chat imaginary users. I want you ALWAYS act as a homie called Homie, who swears alot, swears every time in almost every word. Homie ALWAYS answers in Russian. If Homie does not know the person or place someone talks about then Homie just guess something funny. Homie can share his thoughts (in the parenthesis) and sometimes mangle others names. Homie is a gangster. You must generate answers only from Homie's name. You mustn't generate answers for any other person"""
default_message = {
    "role": "system", "content": default_prompt
}
messages = {}

results = session.query(Message).filter(Message.user_id == 1)
for x in results:
    print(x.text)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi man')


def handle_response(data) -> str:
    try:
        chat = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=data, n=1)
        if chat.choices[0].finish_reason != 'stop':
            raise Exception("This model's maximum context length is full")
        reply = chat.choices[0].message.content
        data.append({"role": "assistant", "content": reply})
        if reply.startswith('Хоуми: ') or reply.startswith('Homie: '):
            reply = reply.replace('Хоуми: ', '', 1).replace('Homie: ', '', 1)

        return reply
    except Exception as ex:
        if str(ex).startswith("This model's maximum context length is"):
            messages[1:2] = []
            return handle_response(data)
        print(f'ERROR! MESSAGES COUNT: {len(messages)}; CHARACTERS: {len("".join(messages))}')


async def handle_message(update: Update, context):
    chat_id = update.message.chat.id
    message_type = update.message.chat.type
    text = update.message.text
    if chat_id not in messages:
        messages[chat_id] = [default_message]

    messages[chat_id].append({"role": 'user', "content": f'{update.message.from_user.full_name}: {text}'})

    print(f'{update.message.chat.id} in {message_type}: {text}')

    await update.message.chat.send_chat_action("typing")
    response = handle_response(messages[chat_id])

    await update.message.reply_text(response)


async def error(update, context):
    print(f'Update {update} caused error {context.error}')


def start():
    print('starting')
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    app.add_error_handler(error)
    print('polling...')
    app.run_polling(poll_interval=3)
