import logging
import threading

from ..unique_id_generator import unique_thread_name

logger = logging.getLogger(__name__)


def start_new_daemon_thread(target_func,
                            func_args=(), sufix_thread_name: str = "") -> None:
    thread_name: str = unique_thread_name(f"_{sufix_thread_name}")
    logger.debug(f'Создание нового треда с названием {thread_name}')
    thread = threading.Thread(
        target=target_func,
        args=func_args,
        daemon=True,
        name=thread_name
    )
    thread.start()
    return thread
