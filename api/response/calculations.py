from pydantic import Field

from api.response.base import ResponseBase
from db.enum.calculations import CalculationStatusEnum


class ResponseCalculation(ResponseBase):
    name: str = Field(...)
    calculation_start_date: str = Field(...)
    status: CalculationStatusEnum = Field(...)


class ResponseCalculationTiny(ResponseBase):
    id: int = Field(...)
