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

# Создайте обработчик для записи логов в файл
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
# Создайте форматирование для логов
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# Добавьте обработчик к логгеру
logger.addHandler(stream_handler)