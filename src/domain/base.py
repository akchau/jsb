from src.domain.utils.api_view import ApiView
from src.services import ScheduleEntity


class BaseApp:

    def __init__(self, view: ApiView, entity: ScheduleEntity):
        self._api_view = view
        self._entity = entity

    @staticmethod
    async def parse_data(update):
        query = update.callback_query
        data = query.data
        if len(data.split("/")) > 2:
            return data.split("/")[1:]
        if len(data.split("/")) == 2:
            return data.split("/")[1]
        if len(data.split("/")) == 1:
            return None

    @staticmethod
    async def create_data(handler, *args):
        return f"{handler}/" + "/".join(args)

