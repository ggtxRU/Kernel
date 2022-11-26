class BaseServerException(Exception):
    status_code: int = ...
    code: int = ...
    message: str = ...

    @classmethod
    def raise_with_value(cls, value: int):
        exc = cls()
        exc.message = exc.message % value
        raise exc


class ServerInternalException(BaseServerException):
    status_code = 500
    code = 1
    message = 'Неизвестная ошибка сервера'


class UnprocessableException(BaseServerException):
    status_code = 422
    code = 2
    message = 'Неправильный формат входных данных'


class NotFoundException(BaseServerException):
    status_code = 404
    code = 3
    message = 'Объект не найден'
