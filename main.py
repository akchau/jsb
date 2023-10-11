import sys

from logger import logger
from bot.jbot import start_bot
from test import start_tests


START_COMMAND_DICT = {
    "go": ("Запуск бота", start_bot),
    "test": ("Запуск тестов", start_tests)
}

HELP_ARGUMENTS = ["-h", "--h", "-help", "--help"]


def print_help():
    available_command = ""
    for current_command, command_description in START_COMMAND_DICT.items():
        available_command = f"{available_command}\npython main.py {current_command} - {command_description[0]}"
    logger.debug(f"Возможные команды:\n{available_command}\n")


if __name__ == "__main__":
    console_arguments = sys.argv
    command = "python " + " ".join(console_arguments)
    if console_arguments[0] == "c:\\dev\\j_bot\\main.py":
        logger.debug("Запуск приложения в DEBUG режиме.")
        start_bot()
    elif len(console_arguments) == 1:
            print_help()
    elif len(console_arguments) == 2:
        flag = console_arguments[1]
        if flag in START_COMMAND_DICT.keys():
            logger.debug(f"Получена команда {command}.")
            logger.info(START_COMMAND_DICT[console_arguments[1]][0])
            START_COMMAND_DICT[console_arguments[1]][1]()
        elif flag in HELP_ARGUMENTS:
            print_help()
        else:
            logger.debug(f"Аргумент комманды {flag} неизвестен")
            print_help()
    else:
        logger.debug(f"Неизвестная команда: {command}")
        print_help()