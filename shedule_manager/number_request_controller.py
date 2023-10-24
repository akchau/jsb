from core.json_manager.json_manager import BaseJsonController
from logger import logger
import settings

LOST_TRYING_KEY = "lost_number_of_trying"
LOST_TRYING_FILE = "data/system/shedule_cache/number_trying_day.json"

class NumberRequestControler(BaseJsonController):

    REQUESTS_IN_DAY = settings.REQUESTS_IN_DAY

    def _get_number_of_trying(self):
        return self._get_json_record(
            filepath=LOST_TRYING_FILE,
            key=LOST_TRYING_KEY
        )

    def _refresh_number_of_trying(self, current_value):
        current_value -= 1
        self._write_json_record(
            filepath=LOST_TRYING_FILE,
            key=LOST_TRYING_KEY,
            value=current_value
        )

    def get_request_permission(self):
        lost_requests = self._get_number_of_trying()
        if lost_requests > 0:
            self._refresh_number_of_trying(lost_requests)
            verdict = (True, f"ВЫДАНО. ОСТАНОЛОСЬ ЗАПРОСОВ: {lost_requests}")
        else:
            verdict = (False, "НЕ ВЫДАНО. ПРЕВЫШЕНО КОЛИЧЕСТВО ДОПУСТИМЫХ ПОПЫТОК!!!")
        logger.info(f"РАЗРЕШЕНИЕ НА ЗАПРОС: {verdict[1]}")
        return verdict[0]


def reset_number_of_trying():
    MAX_ATTEMPTS = settings.REQUESTS_IN_DAY
    NumberRequestControler()._write_json_record(
        filepath=LOST_TRYING_FILE,
        key=LOST_TRYING_KEY,
        value=MAX_ATTEMPTS
    )
    logger.info(f"СБРОС КОЛИЧЕСТВА ОСТАВШИХСЯ ПОПЫТОК. ОСТАЛОСЬ ПОПЫТОК {MAX_ATTEMPTS}")


def api_request_permission(func):
    def wrapper(*args, **kwargs):
        permission = NumberRequestControler().get_request_permission()
        if permission:
            return func(*args, **kwargs)
        return None
    return wrapper