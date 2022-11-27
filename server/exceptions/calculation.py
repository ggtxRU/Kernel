from server.exceptions.base import BaseServerException


class CalculationNotFoundException(BaseServerException):
    status_code = 400
    code = 10
    message = 'Расчет с id %d не найден'