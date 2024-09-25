"""
Обработка данных пользователя в сообщениях бота.
"""
from telegram import Update
from logger import logger


async def get_request_user(update):
    """
    Получение пользователя при запросе бота.
    :param update: Объект обновления бота.
    :return:
    """
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username

    return {
        "username": username,
        "str": f"[{first_name} {last_name}]({username})"
    }


async def log_user(update: Update):
    """
    Логирование пользователя.
    :param update: Объект обновления бота.
    :return:
    """
    request_user = await get_request_user(update=update)
    logger.info('Получен запрос от %s', request_user["str"])


def log_user_decorator(func):
    """
    Декоратор для логирования запросов пользователей
    """
    async def wrapper(*args, **kwargs):
        update, _ = args
        await log_user(update)
        return await func(*args, **kwargs)
    return wrapper
