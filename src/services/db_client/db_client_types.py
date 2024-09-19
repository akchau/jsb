# TODO Эту модель включить в стандартный пакет и обрабатывать. Пока не тестируем
import re

from pydantic import BaseModel, validator


class DbClientAuthModel(BaseModel):
    db_name: str
    db_user: str
    db_host: str
    db_password: str
    db_port: int

    @validator('db_name')
    def check_url(cls, v):
        if not re.match(r'^(mongodb|mongodb\+srv)', v):
            raise ValueError('Имя БД должно быть mongodb или mongodb+srv')
        return v
