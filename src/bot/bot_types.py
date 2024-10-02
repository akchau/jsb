"""
Модели и типы бота.
"""
from enum import Enum


class StationActions(str, Enum):
    """
    Действия со станцией.
    """
    MOVE = "MOVE"
    DELETE = "DELETE"
    REGISTER = "REGISTER"
