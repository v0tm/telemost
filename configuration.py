import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    CHATGPT_SYMBOLS_THRESHOLD = os.environ.get("CHATGPT_SYMBOLS_THRESHOLD", 8000)
    CHATGPT_TOKEN = os.environ.get("CHATGPT_TOKEN")
    CHATGPT_BASE = os.environ.get("CHATGPT_BASE", 'https://api.openai.com/v1/')
    CHATGPT_MODEL = os.environ.get("CHATGPT_MODEL", 'gpt-4o')
    DB_CONNECT_PATH = os.environ.get("DB_CONNECT_PATH")
    AUTHORIZATION_TOKEN = os.environ.get("AUTHORIZATION_TOKEN")
    DEFAULT_CHATGPT_PROMPT = os.environ.get("DEFAULT_CHATGPT_PROMPT", 'none')
    DEFAULT_CHATGPT_SYSTEM_PROMPT = os.environ.get("DEFAULT_CHATGPT_SYSTEM_PROMPT", 'none')
    TITLE_PROMPT = os.environ.get("TITLE_PROMPT", 'none')
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', 'none')
    HTML_TEMPLATE_SETTINGS_COMMAND = os.environ.get('HTML_TEMPLATE_SETTINGS_COMMAND', 'none').replace('\\n', '\n')
