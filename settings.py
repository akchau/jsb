import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = True

REQUESTS_IN_DAY = 400
PAGINATION = 120

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("YANDEX_API_KEY")

JELEZNODOROJNAYA = {
    "code": "s9601675",
}
NIJEGORODSKAYA = {
    "code": "s9601835",
}
STATIONS = [(JELEZNODOROJNAYA, NIJEGORODSKAYA)]

