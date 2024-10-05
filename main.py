import sys

from src import start_bot


class CommandError(Exception):
    pass


REGISTERED_COMMANDS = {
    "go": start_bot
}


def main():
    args = sys.argv
    args_len = len(args)

    if args_len == 1:
        raise CommandError(
            f"Вы должны указать аргументы при обращении к файлу {__name__}. "
            f"Возможные аргументы: {list(REGISTERED_COMMANDS.keys())}"
        )
    elif args_len >= 2:
        command = args[1]
        func = REGISTERED_COMMANDS.get(command, None)

        if func is None:
            raise CommandError(
                f"Данной команды не существует. "
                f"Возможные команды: {list(REGISTERED_COMMANDS.keys())}"
            )
        func()


if __name__ == "__main__":
    main()
