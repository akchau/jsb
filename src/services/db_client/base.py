"""
Модуль базовых классов для работы с MongoDB
"""
from typing import Type, TypeVar, Generic

from mongo_db_client import MongoDbTransport

from src.services.db_client.exc import NotExistException, TransportError, ExistException

CollectionModel = TypeVar("CollectionModel")


#TODO то надо включать в стандартный пакет
class BaseDbCollection(Generic[CollectionModel]):
    """
    Базовый класс коллекций.
    """
    def __init__(self, transport: MongoDbTransport, collection_name: str):
        self._collection_name = collection_name
        self._transport = transport
        self._exist_exception = ExistException
        self._not_exist_exception = NotExistException
        self._transport_error = TransportError
