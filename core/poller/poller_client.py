import logging
import time

from .thread_manager import start_new_daemon_thread
from . import event_manager, poller_exceptions

logger = logging.getLogger(__name__)


class BasePoller:

    manual_break = True

    def __init__(
            self,
            poll_interval: int,
            thread_name: str = "",
            max_attempts: int = None,
            event_manager: event_manager.EventManager = None,
            one_stream: bool = False
         ):
        self.poll_interval = poll_interval
        self.thread_name = thread_name
        self.max_attempts = max_attempts
        self.one_stream = one_stream
        if event_manager is not None:
            self.event_manager = event_manager()
        else:
            self.event_manager = None
        self.counter = 0

    def _is_have_time(self) -> bool:
        return (
            (
                self.max_attempts is not None and
                self.counter < self.max_attempts
            ) or
            self.max_attempts is None
        )

    def _is_time_end(self) -> bool:
        return (
            self.max_attempts is not None and
            self.counter >= self.max_attempts
        )

    def _is_not_out_stop(self) -> bool:
        return (
            (
                self.event_manager is not None and
                not self.event_manager.event_is_set()
            ) or
            self.event_manager is None
        )

    def _full_polling_flag(self):
        return (
            # Кастомная функция
            self.should_continue_polling() and
            # Если заданно максимальное количество попыток
            # И они еще остались
            self._is_have_time() and
            # Если задан event_manager и не задан флаг
            self._is_not_out_stop() and
            # Если ручной останов не переведен в True
            self.manual_break
        )

    def _poll(self):
        """
        Цикл поллинга
        """
        logger.info(f'Поллинг {self.thread_name} запущен')
        while self._full_polling_flag():
            # Выполнение поллинга
            self.process_polling()
            # Пауза
            time.sleep(self.poll_interval)
            # Счетчик
            self.counter += 1
        logger.info(f'Поллинг {self.thread_name} остановлен')
        if self._is_time_end():
            raise poller_exceptions.TimeOutException(name=self.thread_name)
        else:
            self.finaly_action()

    def start_polling(self):
        """
        Функция которая запускает поллинг в отдельнои треде.
        """
        if self.one_stream is True:
            self._poll()
        else:
            thread = start_new_daemon_thread(
                target_func=self._poll,
                func_args=(),
                sufix=self.thread_name
            )
        return thread

    def process_polling(self):
        """
        Регулярное действие выполняемое во время поллинга.
        """
        pass

    def should_continue_polling(self) -> bool:
        """
        Функция управления условием новой итерации полинга.

        Returns:
            bool: True если продолжать итерации.
        """
        return True

    def finaly_action(self):
        pass


class BasePollerWithParams(BasePoller):
    def __init__(
            self, poll_interval: int,
            thread_name: str = "",
            request_params: dict = {},
            max_attempts: int = None,
            event_manager=None,
            one_stream: bool = False
         ):
        super().__init__(
            poll_interval=poll_interval,
            thread_name=thread_name,
            max_attempts=max_attempts,
            event_manager=event_manager,
            one_stream=one_stream
        )
        self.request_params = request_params
