import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = True

BOT_TOKEN = os.getenv("BOT_TOKEN")