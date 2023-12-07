from datetime import datetime
from core.base_manager.base_manager import BaseTypeManager
from core.json_manager.json_manager import JsonFileManager
from logger import logger
from .limmiter_exceptions import NotSuccsessRefreshNumberOfTrying


class NumberLimmiterWithJsonMemory(BaseTypeManager):
    """
    Класс-ограничитель. Используется для счета запросов в день.
    Работает на json-файле. Не удаляет файл после завершения работы.
    """

    VERDICTS: dict = {
        "succsess": (True, "РАЗРЕШЕНИЕ ВЫДАНО."),
        "zero_trying": (
            False, ("РАЗРЕШЕНИЕ НЕ ВЫДАНО. "
                    "ПРЕВЫШЕНО КОЛИЧЕСТВО ДОПУСТИМЫХ ПОПЫТОК!")
        )
    }
    value_key = "value_key"
    last_update_key = "last_update"
    TIME_FORMAT_STRING = "%Y-%m-%d %H:%M"

    def __init__(self, memory_path: str, full_number: int):
        """

        Args:

            - memory_path (str): Путь файла для запоминания.

            - full_number (int): Максимальное количество попыток в сутки.
        """
        self.memory: JsonFileManager = JsonFileManager(
                path=memory_path,
                destroy=False,
                create=True,
        )
        self.full_number: int = self.validate_positive_int(full_number)
        if self.memory.get_data() == "":
            self.memory.write_data(
                {
                    self.value_key: self.full_number,
                    self.last_update_key: datetime.now().strftime(
                        self.TIME_FORMAT_STRING
                    )
                }
            )

    def get_last_update_time(self) -> str:
        """
        Получение времени последнего обновления.

        Returns:
            str: Время последнего обновления.
        """
        memory_data: dict = self.memory.get_data()
        return self.parse(memory_data, [(self.last_update_key, dict)])

    def is_update_today(self) -> bool:
        """
        Было ли обновлено сегодня?.

        Returns:
            bool: Вердикт
        """
        last_update_time: datetime = datetime.strptime(
            self.get_last_update_time(),
            self.TIME_FORMAT_STRING
        )
        return last_update_time.date() == datetime.now().date()

    def get_memory_value(self) -> int:
        """
        Метод получения текущего значения.

        Returns:

            - int: Текущее значение.
        """
        memory_data = self.memory.get_data()
        return self.validate_positive_int(self.parse(memory_data, [(self.value_key, dict)]))

    def write_new_number_of_trying(self, new_value: int, reset = False) -> None:
        """
        Метод записи нового значения.

        Args:

            - new_value (int): Ноыое значение.

        Raises:
            - NotSuccsessRefreshNumberOfTrying: Если значение не было запсиано.
        """
        # Проверяем, чтобы значение было не более максимального
        if self.validate_positive_int(new_value) > self.full_number:
            new_value = self.full_number
        # Записываем значения
        memory_data = self.memory.get_data()
        memory_data[self.value_key] = new_value
        if reset:
            memory_data[self.last_update_key] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.memory.write_data(data=memory_data)
        # Проверяем
        if new_value != self.get_memory_value():
            raise NotSuccsessRefreshNumberOfTrying
        return new_value

    def use_trying(self) -> tuple:
        """
        Обновление количества попыток.
        """
        current_value: int = self.get_memory_value()
        if current_value > 0:
            new_value: int = current_value - 1
            verdict: tuple = self.VERDICTS["succsess"]
            self.write_new_number_of_trying(new_value=new_value)
        else:
            verdict: tuple = self.VERDICTS["zero_trying"]
        logger.info(f"РАЗРЕШЕНИЕ НА ЗАПРОС: {verdict[1]}")
        return verdict[0]

    def set_actual_number_of_trying(self, new_value: int = None) -> None:
        """
        Функция для задания нового значения количества попыток.
        Если вызывается без аргументов то обновляется
        до максимального значения.

        Args:
            new_value (int, optional): Новое значение.
        """
        # Если требуется сбросить до максимального значения.
        if new_value is None:
            new_value = self.write_new_number_of_trying(
                new_value=self.full_number,
                reset=True
            )
            logger.info(f"ЗНАЧЕНИЕ ОБНОВЛЕНО: {new_value}")
        # Если требуется задать стартовое значениее.
        else:
            new_value = self.write_new_number_of_trying(new_value=new_value, reset=True)
            logger.info(f"ЗАДАНО КОЛИЧЕСТВА ОСТАВШИХСЯ ПОПЫТОК: {new_value}")
