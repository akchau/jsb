from mongo_db_client import MongoDbTransport
from pydantic import ValidationError

from src.services.db_client.db_client_types import DbClientAuthModel
from src.services.db_client.exc import AuthError


#TODO то надо включать в стандартный пакет
class BaseDbCollection:

    def __init__(self, db_name: str, db_host: str, dp_port: int, db_user: str, db_password: str,
                 _transport_class=MongoDbTransport):
        try:
            clean_data = DbClientAuthModel(
                db_name=db_name,
                db_host=db_host,
                db_port=dp_port,
                db_user=db_user,
                db_password=db_password
            )
        except ValidationError:
            raise AuthError("Невалидные данные для подключения к бд")
        self._transport = _transport_class(**clean_data.dict())
