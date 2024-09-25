"""
Основной модуль бота.
"""
import logging
from telegram.ext import Application

from src.bot.handlers import main_conv_handler
from src.settings import settings


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start_bot() -> None:
    """Run the bot."""
    application = Application.builder().token(settings.BOT_TOKEN).build()
    application.add_handler(main_conv_handler)
    application.run_polling()


if __name__ == "__main__":
    start_bot()
