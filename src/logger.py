import logging

from src.settings import settings

logger = logging.getLogger()

if settings.DEBUG:
    level = logging.DEBUG
else:
    level = logging.ERROR
logger.setLevel(level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
debug_handler = logging.FileHandler('debug.log')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)
error_handler = logging.FileHandler('error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(debug_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)


def setup_logging():
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('pymongo').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    pass