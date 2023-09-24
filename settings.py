import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = True

BOT_TOKEN = os.getenv("BOT_TOKEN")
REQUESTS_IN_DAY = 400
API_KEY = os.getenv("YANDEX_API_KEY")
API_DOMAIN = os.getenv("API_DOMAIN")
PAGINATION = 70