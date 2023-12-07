from api_client.number_request_controller import set_start_value
from core.poller.poller_client import BasePollerWithParams
from .number_request_controller import try_to_reset


class ReseterNimberOfTrying(BasePollerWithParams):
    """
    Поллер сброса оставшихся попыток при смене дня.
    """

    def process_polling(self):
        try_to_reset()


def start_reset_number_of_trying_polling() -> None:
    """
    Метод запускает поллинг
    сброса оставшегося количества попыток.
    """
    ReseterNimberOfTrying(
        poll_interval=60,
        thread_name="reset_number_of_trying_polling",
    ).start_polling()
