from typing import Optional

from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload

from db.enum.calculations import CalculationStatusEnum
from db.enum.direction import DirectionEnum
from db.models.calculations.calculation import DBCalculation
from db.repositories.base import BaseRepository


class CalculationRepository(BaseRepository):
    async def get_from_top_of_the_queue(self, limit: int = 3) -> list[DBCalculation]:
        query = select(
            DBCalculation
        ).where(
            DBCalculation.status == CalculationStatusEnum.in_the_queue
        ).order_by(
            DBCalculation.id
        ).limit(limit)
        return await self.all_ones(query)

    async def get_last_calculation_launches(self, limit: int, offset: int, direction: DirectionEnum) -> list[DBCalculation]:
        query = select(
            DBCalculation
        ).limit(limit).offset(offset)

        if direction == DirectionEnum.direct:
            query = query.order_by(
                desc(DBCalculation.calculation_start_date)
            )
        else:
            query = query.order_by(DBCalculation.id)

        return await self.all_ones(query)

    async def get_by_id_with_complete_result(self, id_: int) -> Optional[DBCalculation]:
        query = select(DBCalculation).where(DBCalculation.id == id_
                                            ).options(joinedload(DBCalculation.complete_result))

        return await self.one_or_none_val(query)
