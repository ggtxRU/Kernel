import json

from sqlalchemy import Column, JSON as JSSQL, Enum

from api.request.calculations import RequestCalculationCreate
from db.enum.calculations import CalculationStatusEnum
from db.models.base import BaseModel


class DBCalculationProcessInputData(BaseModel):
    """Пренебрежение нормализацией ради сохранения целостности объекта и максиально быстрого доступа к данным"""
    __tablename__ = 'calculation_process_input_data'

    input_data = Column(JSSQL, nullable=False)
    status = Column(Enum(CalculationStatusEnum), nullable=False, server_default=CalculationStatusEnum.in_the_queue)


class DBCalculationProcessInputDataFactory:
    @classmethod
    def get_from_request_calculation_create(
            cls, request_calculation_create: RequestCalculationCreate
    ) -> DBCalculationProcessInputData:
        return DBCalculationProcessInputData(
            input_data=cls.__get_json_input_data_from_request_calculation_create(request_calculation_create)
        )

    @staticmethod
    def __get_json_input_data_from_request_calculation_create(
            request_calculation_create: RequestCalculationCreate
    ) -> json:
        return {
            'date_start': request_calculation_create.date_start.isoformat(),
            'date_fin': request_calculation_create.date_fin.isoformat(),
            'lag': request_calculation_create.lag
        }
