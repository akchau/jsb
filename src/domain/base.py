from src.domain.utils.api_view import ApiView
from src.services import ScheduleEntity


class BaseApp:

    def __init__(self, view: ApiView, entity: ScheduleEntity):
        self._api_view = view
        self._entity = entity

