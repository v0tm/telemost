from configuration import Config
from modules.models import Chat
from modules.models import Message
from modules.models import User
from modules.database import session
import openai
from sqlalchemy.orm import joinedload

openai.api_key = Config.CHATGPT_TOKEN
openai.api_base = Config.CHATGPT_API_BASE
default_prompt = """Help me to write dialogues with telegram chat imaginary users. I want you ALWAYS act as a homie called Homie, who swears alot, swears every time in almost every word. Homie ALWAYS answers in Russian. If Homie does not know the person or place someone talks about then Homie just guess something funny. Homie can sometimes mangle others names. Homie is a gangster. You must generate answers only from Homie's name. You mustn't generate answers for any other person. Generate response with valid markdownV2 style for telegram. By default you should answer only to the previous message, not the whole chat. And by default try to generate answer no more than 20-30 words (if the previous user explicitly not asking to write the big text). Always start your messages with this - Homie: """
default_message = {
    "role": "system", "content": default_prompt
}


class ChatGPTGenerateResponseService:

    def __init__(self, bot, chat_id):
        self.bot = bot
        self.data = [default_message]
        self.chat = Chat.get_or_create(id=chat_id)
        if self.chat.prompt is not None:
            self.data = [{"role": "system", "content": self.chat.prompt}]

    def generate_response_with_narrative(self):
        messages = session.query(Message).\
            join(User, Message.user_id == User.id).\
            filter(Message.chat_id == self.chat.id, Message.scope == self.chat.scope).\
            options(joinedload(Message.user)).\
            order_by(Message.id.desc()).\
            all()

        for message in messages:
            role = 'assistant' if message.user_id == self.bot.id else 'user'
            username = message.user.first_name or message.user.username
            text = f'{username}: {message.text}'
            if sum([len(m['content']) for m in self.data]) + len(text) > Config.CHATGPT_SYMBOLS_THRESHOLD:
                break
            else:
                self.data.insert(1, {"role": role, "content": text})
        # print(f'{self.data}')
        return self._request_response(self.data)

    def generate_response(self, task):
        self.data.append({"role": 'user', "content": f'{task}'})
        return self._request_response(self.data)

    def _request_response(self, data):
        try:
            chat = openai.ChatCompletion.create(model=Config.CHATGPT_MODEL, messages=data, n=1)
            if chat.choices[0].finish_reason != 'stop':
                raise Exception("This model's maximum context length is full")
            reply = chat.choices[0].message.content
            data.append({"role": "assistant", "content": reply})
            if reply.startswith('Хоуми: ') or reply.startswith('Homie: ') or reply.startswith('homieish_bot: '):
                reply = reply.replace('Хоуми: ', '', 1).replace('Homie: ', '', 1).replace('homieish_bot: ', '', 1)
            return reply
        except Exception as ex:
            if str(ex).startswith("This model's maximum context length is"):
                data[1:3] = []
                return self._request_response(data)
            print(f'ERROR! MESSAGES COUNT: {len(data)}; CHARACTERS: {len("".join(data))}')
            return str(ex)
