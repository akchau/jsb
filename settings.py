import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = True

REQUESTS_IN_DAY = 400
PAGINATION = 120

API_DOMAIN = os.getenv("API_DOMAIN")
API_PORT = os.getenv("API_PORT")
API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATA_FOLDER = "data/system/shedule_cache"

JELEZNODOROJNAYA = {
    "code": "s9601675",
}
NIJEGORODSKAYA = {
    "code": "s9601835",
}
STATIONS = [(JELEZNODOROJNAYA, NIJEGORODSKAYA)]
