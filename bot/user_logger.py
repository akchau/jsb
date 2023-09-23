from telegram import Update
from logger import logger

async def get_request_user(update):
    
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username

    return {
        "username": username,
        "str": f"[{first_name} {last_name}]({username})"
    }

async def log_user(update: Update):
    request_user = await get_request_user(update=update)
    logger.info(f'Получен запрос от {request_user["str"]}')


def log_user_decorator(func):
    async def wrapper(*args, **kwargs):
        update, context = args
        await log_user(update)
        return await func(*args, **kwargs)
    return wrapper
