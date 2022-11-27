import json

from sqlalchemy import Column, JSON as JSSQL, Enum, Text, DateTime
from sqlalchemy.orm import relationship

from api.request.calculations import RequestCalculationCreate
from db.enum.calculations import CalculationStatusEnum
from db.models.base import BaseModel


class DBCalculation(BaseModel):
    """Пренебрежение нормализацией ради сохранения целостности объекта и максиально быстрого доступа к данным"""
    __tablename__ = 'calculation'

    name = Column(Text, nullable=True)
    input_data = Column(JSSQL, nullable=False)
    status = Column(Enum(CalculationStatusEnum), nullable=False, server_default=CalculationStatusEnum.in_the_queue)

    calculation_start_date = Column(DateTime, nullable=True)
    complete_result = relationship('DBCalculationResult', uselist=False, lazy='raise')

    @property
    def get_name(self) -> str:
        if not self.name:
            return 'Сalculation %d' % self.id
        else:
            return self.name


class DBCalculationProcessInputDataFactory:
    @classmethod
    def get_from_request_calculation_create(
            cls, request_calculation_create: RequestCalculationCreate
    ) -> DBCalculation:
        return DBCalculation(
            name=request_calculation_create.name,
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
