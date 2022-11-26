from sqlalchemy.ext.asyncio import AsyncSession

from api.request.calculations import RequestCalculationCreate
from db.models.calculations.input_data import DBCalculationProcessInputData, DBCalculationProcessInputDataFactory
from db.repositories.calculation import CalculationRepository


class CalculationManager:
    @classmethod
    async def create_new_calculation(
            cls,
            session: AsyncSession,
            request_model: RequestCalculationCreate
    ) -> DBCalculationProcessInputData:
        """
        Adds input data for calculation to an improvised queue.
        """

        data: DBCalculationProcessInputData = DBCalculationProcessInputDataFactory.get_from_request_calculation_create(
            request_calculation_create=request_model
        )
        await CalculationRepository(session).add_model(data)
        return data
