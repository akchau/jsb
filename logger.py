import logging
import sys

import settings

logger = logging.getLogger(__name__)

if settings.DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO

logger = logging.getLogger('j_bot')
logger.setLevel(level)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)