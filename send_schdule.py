import logging


logger = logging.getLogger(__name__)


class ScheduleSender:

    def __init__(self, input_params: dict) -> None:
        self._input_params: dict = input_params

    def _request_schedule(self) -> dict:
        data = {}
        return data

    def _clean_schedule(self, data: dict) -> dict:
        return data

    def _validate_schedule(self, data) -> dict:
        return data

    def _constructor(self, data: dict) -> str:
        schedule_message = f"Ваше расписание:\n\n{data}"
        return schedule_message

    def _construct_schedule(self) -> str:
        schedule = self._request_schedule()
        clean_schedule = self._clean_schedule(data=schedule)
        valide_scheule = self._validate_schedule(data=clean_schedule)
        message = self._constructor(data=valide_scheule)
        return message

    def get_shedule(self) -> str:
        logger.error(f'Получен запрос на загрузку расписания с {self._input_params}')
        return self._construct_schedule()


if __name__ == "__main__":
    sender = ScheduleSender({}).get_shedule()
    print(sender)
