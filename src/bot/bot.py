import logging

from telegram.error import NetworkError

from src.bot.handlers import main_conv_handler
from src.init_app import get_app_data

logger = logging.getLogger(__name__)


def start_bot() -> None:
    """Run the bot."""
    try:
        application = get_app_data().application_builder.build()
        application.add_handler(main_conv_handler)
        application.run_polling()
    except NetworkError:
        logger.error("Не удалось запустить бот. Недоступна сеть!")