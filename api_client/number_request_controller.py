import os
import uuid
from core.json_manager.json_manager import JsonFileManager
from core.limmiter.limmiter import NumberLimmiterWithJsonMemory
import settings

# -------- Путь к файлу -----------------
MEMORY_PATH: str = os.path.join(
    settings.DATA_FOLDER,
    "number_trying_day.json"
)
# ------------ Ключ ---------------------
MEMORY_KEY: str = "lost_number_of_trying"
# ---------------------------------------


class NumberRequestControler(NumberLimmiterWithJsonMemory):
    pass


def api_request_permission(func):
    """
    Декоратор который будет выдавать разрешение на запрос,
    если количество попыток больше нуля и считать использованные попытки.
    """
    def wrapper(*args, **kwargs):
        if NumberRequestControler(
            path=MEMORY_PATH,
            max_requests=settings.REQUESTS_IN_DAY,
        ).use_trying():
            return func(*args, **kwargs)
        return None
    return wrapper


def set_start_value() -> None:
    """
    Задание актуального значения оставшихся попыток перед
    запуском бота.

    Args:
        new_value (int): Актуальное значение
    """
    start_value: int = int(input("Введите оставшееся количество попыток: "))
    NumberRequestControler(
        path=MEMORY_PATH,
        full_number=settings.REQUESTS_IN_DAY
    ).set_actual_number_of_trying(new_value=start_value)


def try_to_reset():
    controller: NumberRequestControler = NumberRequestControler(
        path=MEMORY_PATH,
        full_number=settings.REQUESTS_IN_DAY
    )
    if not controller.is_update_today():
        controller.set_actual_number_of_trying()
