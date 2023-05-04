import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    CHATGPT_TOKEN = os.environ.get("CHATGPT_TOKEN")
    DB_CONNECT_PATH = os.environ.get("DB_CONNECT_PATH")
    AUTHORIZATION_TOKEN = os.environ.get("AUTHORIZATION_TOKEN")
    DEFAULT_CHATGPT_PROMPT = os.environ.get("DEFAULT_CHATGPT_PROMPT", 'none')
    DEFAULT_CHATGPT_SYSTEM_PROMPT = os.environ.get("DEFAULT_CHATGPT_SYSTEM_PROMPT", 'none')
    TITLE_PROMPT = os.environ.get("TITLE_PROMPT", 'none')
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', 'none')
