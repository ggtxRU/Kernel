from pydantic import Field

from api.response.base import ResponseBase
from db.enum.calculations import CalculationStatusEnum
from db.models.calculations.input_data import DBCalculationProcessInputData


class ResponseCalculation(ResponseBase):
    name: str = Field(...)
    calculation_start_date: str = Field(...)
    status: CalculationStatusEnum = Field(...)


class ResponseCalculationCreate(ResponseBase):
    id: int = Field(...)


class ResponseCalculationCreateFactory:
    @staticmethod
    def factory_method(data_for_calculation: DBCalculationProcessInputData):
        return ResponseCalculationCreate(
            id=data_for_calculation.id
        )
