from dataclasses import dataclass
from typing import Any

from src.domain.utils.api_view import ApiView
from src.services import ScheduleEntity


class DataHandler:

    @dataclass
    class InputParsedData:
        user: str
        data: str

    __input_parsed_data = InputParsedData

    async def __parse_data(self, update) -> dict | None:
        query = update.callback_query
        data = query.data
        if len(data.split("/")) > 2:
            res = data.split("/")[1:]
        elif len(data.split("/")) == 2:
            res = data.split("/")[1]
        else:
            return None
        return self.__get_dict_from_list(res)

    def __get_dict_from_list(self, params: list[str]) -> dict:
        res = {}
        for param in params:
            splitted_param_string = param.split(":")
            res[splitted_param_string[0]] = splitted_param_string[1]
        return res

    @staticmethod
    async def create_data(**kwargs) -> str:
        return "/" + "/".join([f"{key}:{param}" for key, param in kwargs.items()])

    async def get_context(self, update) -> InputParsedData:
        user = update.message.from_user if update.message else update.callback_query.from_user
        data: Any = await self.__parse_data(update)
        return self.__input_parsed_data(user=user, data=data)


class BaseApp:

    def __init__(self, view: ApiView, entity: ScheduleEntity):
        self._api_view = view
        self._entity = entity
        self._context_creator = DataHandler()


async def app_handler(func):

    """
    Декоратор обработает ошибки при работе с api
    Глобальная ошибка которую выбрасывает транспорт -> Внутренняя ошибка.
    Ошибка при парсинге модели ответа -> Внутренняя ошибка.
    :param func:
    :return:
    """
    async def wrapper(update):
        route_handler = DataHandler()
        context = await route_handler.get_context(update)
        return func(context.user, context.data)
    return wrapper