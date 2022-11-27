from typing import Optional

from fastapi import Query
from pydantic import Field
from pydantic.datetime_parse import datetime

from api.response.base import ResponseBase
from db.enum.calculations import CalculationStatusEnum
from db.models.calculations.calculation import DBCalculation


class ResponseCalculationSimple(ResponseBase):
    name: str = Field(...)
    status: CalculationStatusEnum = Field(...)
    calculation_start_date: Optional[datetime] = Field(None)


class ResponseCalculationWithCompleteResult(ResponseCalculationSimple):
    calculation_result_date: datetime = Field(...)
    liquid: int = Field(...)
    oil: int = Field(...)
    water: int = Field(...)
    wct: int = Field(...)
    name: Optional[str] = Field(None)
    time_spent: Optional[float] = Field(None)


class ResponseCalculationFactorySimple:
    @staticmethod
    def get_from_calculation_data(calculation_data: DBCalculation) -> ResponseCalculationSimple:
        return ResponseCalculationSimple(
            name=calculation_data.get_name,
            calculation_start_date=calculation_data.calculation_start_date,
            status=calculation_data.status
        )

    @classmethod
    def get_many_from_calculation_data(cls, calculation_data: list[DBCalculation]) -> list[ResponseCalculationSimple]:
        return [cls.get_from_calculation_data(calculation_data=calculation_data_) for calculation_data_ in calculation_data]


class ResponseCalculationFactoryWithCompleteResult:
    @staticmethod
    def get_from_calculation_data(calculation_data: DBCalculation, q: Query) -> ResponseCalculationWithCompleteResult:
        return ResponseCalculationWithCompleteResult(
            calculation_start_date=calculation_data.calculation_start_date,
            status=calculation_data.status,
            calculation_result_date=calculation_data.complete_result.calculation_result_date,
            liquid=calculation_data.complete_result.liquid,
            oil=calculation_data.complete_result.oil,
            water=calculation_data.complete_result.water,
            wct=calculation_data.complete_result.wct,
            time_spent=calculation_data.complete_result.time_spent if 'time-spent' in q else None,
            name=calculation_data.get_name if 'name' in q else None,

        )


class ResponseCalculationCreate(ResponseBase):
    id: int = Field(...)


class ResponseCalculationCreateFactory:
    @staticmethod
    def factory_method(data_for_calculation: DBCalculation) -> ResponseCalculationCreate:
        return ResponseCalculationCreate(
            id=data_for_calculation.id
        )
