import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = True

BOT_TOKEN = os.getenv("BOT_TOKEN")
TEST_CHAT_ID = os.getenv("TEST_CHAT_ID")
TEST_MESSAGE = os.getenv("TEST_MESSAGE")