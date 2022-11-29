import datetime

from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey

from db.models.base import BaseModel


class DBCalculationResult(BaseModel):
    __tablename__ = 'calculation_result'

    calculation_result_date = Column(DateTime, nullable=False)
    liquid = Column(Integer, nullable=False)
    oil = Column(Integer, nullable=False)
    water = Column(Integer, nullable=False)
    wct = Column(Integer, nullable=False)
    time_spent = Column(Float, nullable=False)

    calculation_id = Column(
        Integer, ForeignKey('calculation.id', ondelete='CASCADE'), nullable=True)


class DBCalculationProcessCompleteFactory:
    @classmethod
    def get_from_data_frame(
            cls,
            calculation_result_date: datetime,
            liquid: int, oil: int, water: int, wct: int,
            time_spent: float,
            calculation_id: int
    ) -> DBCalculationResult:
        return DBCalculationResult(
            calculation_result_date=calculation_result_date,
            liquid=liquid,
            oil=oil,
            water=water,
            wct=wct,
            time_spent=time_spent,
            calculation_id=calculation_id
        )
