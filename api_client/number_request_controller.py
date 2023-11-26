import os
from core.int_manager.int_manager import validate_int
from core.json_manager.json_manager import JsonFileManager
from logger import logger
import settings

from .api_client_exceptoins import (
    IsNotIntException,
    NotSuccsessRefreshNumberOfTrying
)

MEMORY_PATH = os.path.join(
    settings.DATA_FOLDER,
    "number_trying_day.json"
)


VERDICTS = {
    "succsess": (True, "РАЗРЕШЕНИЕ ВЫДАНО."),
    "zero_trying": (
        False, "РАЗРЕШЕНИЕ НЕ ВЫДАНО. ПРЕВЫШЕНО КОЛИЧЕСТВО ДОПУСТИМЫХ ПОПЫТОК!"
    ),
    "refresh": (False, "ЗНАЧЕНИЕ ОСТ. ПОПЫТОК ОБНОВЛЕНО.")
}


class NumberRequestControler(JsonFileManager):

    LOST_TRYING_KEY = "lost_number_of_trying"
    START_DICT = {LOST_TRYING_KEY: settings.REQUESTS_IN_DAY}

    def __init__(self, path: str, max_requests: int):
        super().__init__(
            path=path,
            destroy=False,
            create=True
        )
        self.REQUESTS_IN_DAY = max_requests

    def _configuration_dict(self, value: int) -> dict:
        return {
            self.LOST_TRYING_KEY: value
        }

    def _get_number_of_trying(self) -> int:
        return int(self.get_value(
            parse_keys=(
                (self.LOST_TRYING_KEY, int),
            )
        ))

    def _write_new_number_of_trying(self, new_value: int):
        self.write(
            data=self._configuration_dict(
                value=new_value,
            )
        )
        if new_value != self._get_number_of_trying():
            raise NotSuccsessRefreshNumberOfTrying

    def _refresh_number_of_trying(
            self,
            manual_value: int | None = None
         ) -> int:
        if manual_value is None:
            current_value: int = validate_int(self._get_number_of_trying())
            if current_value > 0:
                new_value = current_value - 1
                verdict = VERDICTS["succsess"]
            else:
                new_value = current_value
                verdict = VERDICTS["zero_trying"]
        else:
            manual_value = validate_int(data=manual_value)
            verdict = VERDICTS["refresh"]
            new_value = manual_value
        self._write_new_number_of_trying(new_value=new_value)
        return verdict

    def get_request_permission(self) -> bool:
        """
        Метод выдает разрешение, если остались попытки.

        Returns:
            bool: Разрешение.
        """
        verdict = self._refresh_number_of_trying()
        logger.info(f"РАЗРЕШЕНИЕ НА ЗАПРОС: {verdict[1]}")
        return verdict[0]

    def reset_number_of_trying(self) -> None:
        self._refresh_number_of_trying(
            manual_value=settings.REQUESTS_IN_DAY
        )
        logger.info("СБРОС КОЛИЧЕСТВА ОСТАВШИХСЯ ПОПЫТОК. "
                    f"ОСТАЛОСЬ ПОПЫТОК {settings.REQUESTS_IN_DAY}")

    def set_actual_number_of_trying(self, new_value: int) -> None:
        self._refresh_number_of_trying(
            manual_value=new_value
        )
        logger.info(f"ЗАДАНО КОЛИЧЕСТВА ОСТАВШИХСЯ ПОПЫТОК. {new_value}")


def api_request_permission(func):
    """
    Декоратор который будет выдавать разрешение на запрос,
    если количество попыток больше нуля.
    """
    def wrapper(*args, **kwargs):
        if NumberRequestControler(
            max_requests=settings.REQUESTS_IN_DAY,
        ).get_request_permission():
            return func(*args, **kwargs)
        return None
    return wrapper


def set_start_value(new_value: int) -> None:
    """
    Задание актуального значения оставшихся попыток перед
    запуском бота.

    Args:
        new_value (int): Актуальное значение
    """
    NumberRequestControler(
        max_requests=settings.REQUESTS_IN_DAY,
    ).set_actual_number_of_trying(new_value=new_value)


def reset_lost_trying() -> None:
    """
    Сброс текущего значения до максимального.
    """
    NumberRequestControler(
        max_requests=settings.REQUESTS_IN_DAY
    ).reset_number_of_trying()
