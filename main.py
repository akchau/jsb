import sys

from logger import logger
from bot.jbot import start_bot


command_dict = {
    "go": "Запуск бота"
}


if __name__ == "__main__":
    console_arguments = sys.argv
    command = "python " + " ".join(console_arguments)
    if sys.argv[0] == "c:\\dev\\j_bot\\main.py":
        logger.debug("Запуск приложения в DEBUG режиме.")
        start_bot()
    elif len(sys.argv) == 1:
        available_command = ""
        for current_command, command_description in command_dict.items():
            available_command = f"{available_command}\npython main.py {current_command} - {command_description}"
        logger.debug(f"Задайте аргументы для запуска: {command}")
        logger.debug(f"Возможные команды:\n{available_command}\n")
    elif sys.argv[1] == "go":
        logger.info("Запуск приложения в БАЗОВОМ работы.")
        start_bot()
    else:
        logger.debug(f"Получена неизвестная команда {command}")