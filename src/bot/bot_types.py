from enum import Enum


class StationActions(str, Enum):
    MOVE = "MOVE",
    DELETE = "DELETE"
    REGISTER = "REGISTER"
