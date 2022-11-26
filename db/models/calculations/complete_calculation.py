import datetime

from sqlalchemy import Column, DateTime, Text, Integer, Float

from db.models.base import BaseModel


class DBCalculationProcessComplete(BaseModel):
    __tablename__ = 'calculation_process_complete'

    name = Column(Text, nullable=True)
    calculation_start_date = Column(DateTime, nullable=False)
    calculation_result_date = Column(DateTime, nullable=False)
    liquid = Column(Integer, nullable=False)
    oil = Column(Integer, nullable=False)
    water = Column(Integer, nullable=False)
    wct = Column(Integer, nullable=False)
    time_spent = Column(Float, nullable=False)

    @property
    def get_name(self) -> str:
        if not self.name:
            return 'Сalculation %id' % self.id
        else:
            return self.name


class DBCalculationProcessCompleteFactory:
    @classmethod
    def get_from_kernel_calculate(
            cls,
            calculation_start_date: datetime,
            calculation_result_date: datetime,
            liquid: int, oil: int, water: int, wct: int,
            time_spent: float
    ) -> DBCalculationProcessComplete:
        return DBCalculationProcessComplete(
            calculation_start_date=calculation_start_date,
            calculation_result_date=calculation_result_date,
            liquid=liquid,
            oil=oil,
            water=water,
            wct=wct,
            time_spent=time_spent
        )
