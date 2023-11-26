import threading


class EventManager:
    """
    Класс управляет объектами event.
    """
    event_variable = threading.Event()

    def event_is_set(self) -> bool:
        return self.event_variable.is_set()

    def clear_event(self) -> None:
        self.event_variable.clear()

    def set_event(self) -> None:
        self.event_variable.set()
