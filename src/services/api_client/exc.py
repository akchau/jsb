"""
Исключения Api-клиента.
"""
class ApiError(Exception):
    """
    Исключение api-клиента
    """
    def __init__(self, message):
        super().__init__(message)
