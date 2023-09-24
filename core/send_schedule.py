from logger import logger

class BaseDataConstructor:

    def __init__(self, input_params: dict) -> None:
        self._input_params: dict = input_params

    def request_schedule(self) -> dict:
        data = {}
        return data

    def clean_schedule(self, data: dict) -> dict:
        return data

    def _validate_schedule(self, data) -> dict:
        return data

    def constructor(self, data: dict) -> str:
        schedule_message = f"Ваше расписание:\n\n{data}"
        return schedule_message

    def _construct_schedule(self) -> str:
        schedule = self.request_schedule()
        clean_schedule = self.clean_schedule(data=schedule)
        valide_scheule = self._validate_schedule(data=clean_schedule)
        return self.constructor(data=valide_scheule)

    def get_shedule(self) -> str:
        logger.info(f'Получен запрос на загрузку расписания с {self._input_params}')
        return self._construct_schedule()

