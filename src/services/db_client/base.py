from typing import Type, TypeVar, Generic

from pydantic import BaseModel


CollectionModel = TypeVar("CollectionModel")


#TODO то надо включать в стандартный пакет
class BaseDbCollection(Generic[CollectionModel]):

    def __init__(self, transport, collection_model: Type[CollectionModel], collection_name: str):
        self._collection_model = collection_model
        self._collection_name = collection_name
        self._transport = transport
