import asyncio
import json
import time
from datetime import datetime
from typing import Optional

from pandas import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.calculations import RequestCalculationCreate
from calculation.kernel import CalculationKernel
from db.custom.calculation_params import CalculationParams
from db.enum.calculations import CalculationStatusEnum
from db.enum.direction import DirectionEnum
from db.models.calculations.calculation_result import DBCalculationProcessCompleteFactory, \
    DBCalculationResult
from db.models.calculations.calculation import DBCalculation, DBCalculationProcessInputDataFactory
from db.repositories.calculation import CalculationRepository
from entities.kernel import KERNEL
from server.exceptions.calculation import CalculationNotFoundException


class CalculationManager:
    @classmethod
    async def create_new_calculation(
            cls,
            session: AsyncSession,
            request_model: RequestCalculationCreate
    ) -> DBCalculation:
        """
        Adds input data for calculation to an improvised queue.
        """

        data: DBCalculation = DBCalculationProcessInputDataFactory.get_from_request_calculation_create(
            request_calculation_create=request_model
        )
        await CalculationRepository(session).add_model(data)
        return data

    @staticmethod
    async def get_last_calculation_launches(
            session: AsyncSession,
            limit: int, offset: int, direction: DirectionEnum
    ) -> list[DBCalculation]:
        return await CalculationRepository(session).get_last_calculation_launches(
            limit=limit, offset=offset, direction=direction)

    @staticmethod
    async def get_by_id(
            session: AsyncSession,
            id: int
    ) -> Optional[DBCalculation]:
        calculation: Optional[DBCalculation] = await CalculationRepository(
            session).get_by_id_with_complete_result(id_=id)
        if not calculation:
            raise CalculationNotFoundException.raise_with_value(id)
        return calculation

    @classmethod
    async def calculation_process_prepare_and_do(
            cls,
            session: AsyncSession,
    ) -> None:
        """Get 3 input parameters for calculation process from the top of the improvised queue."""
        calculations_in_queue: list[DBCalculation] = await CalculationRepository(
            session).get_from_top_of_the_queue()

        """
        It makes no sense to continue the continuous work of the worker 
            if the queue with the parameters waiting for the queue is empty
        """
        if len(calculations_in_queue) >= 1:

            for calculation in calculations_in_queue:
                calculation_params_: CalculationParams = await cls.__get_data_for_calculation_from_json(
                    json_params=calculation.input_data)

                """
                :param start_time_calculation_process: Time-tracking for calculation process
                """
                start_time_calculation_process = time.monotonic()

                await cls.__change_status_to_in_progress(calculation=calculation, session=session)
                result_data_frame: DataFrame = await cls.__do_calculation_and_return_result_data_frame(
                    calculation_params=calculation_params_)

                time_spent_on_calculation = time.monotonic() - start_time_calculation_process

                await cls.__add_calculation_result_in_db(
                    session=session,
                    data_frame=result_data_frame,
                    time_spent_on_calculation=time_spent_on_calculation,
                    calculation_id=calculation.id
                )
                await cls.__change_status_to_complete(calculation=calculation, session=session)
        else:
            time.sleep(5)

    @classmethod
    async def __get_data_for_calculation_from_json(
            cls, json_params: json
    ) -> CalculationParams:
        """
        :param json_params: 'date_start': 'YYYY-MM-DD', 'date_fin': 'YYYY-MM-DD', 'lag': int
        :return:
        """
        return CalculationParams(
            date_start=datetime.fromisoformat(json_params['date_start']),
            date_fin=datetime.fromisoformat(json_params['date_fin']),
            lag=json_params['lag']
        )

    @staticmethod
    async def __change_status_to_in_progress(
            calculation: DBCalculation, session: AsyncSession
    ) -> None:
        calculation.status = CalculationStatusEnum.in_progress
        calculation.calculation_start_date = datetime.now()

        await session.flush()
        await session.commit()

    @staticmethod
    async def __change_status_to_complete(
            calculation: DBCalculation, session: AsyncSession
    ) -> None:
        calculation.status = CalculationStatusEnum.complete
        await session.flush()
        await session.commit()

    @staticmethod
    async def __do_calculation_and_return_result_data_frame(
            calculation_params: CalculationParams) -> DataFrame:
        return KERNEL.main(
            date_start=calculation_params.date_start,
            date_fin=calculation_params.date_fin,
            lag=calculation_params.lag
        )

    @staticmethod
    async def __add_calculation_result_in_db(
            data_frame: DataFrame, time_spent_on_calculation: float,
            calculation_id: int, session: AsyncSession
    ) -> None:
        complete_calculation_data = DBCalculationProcessCompleteFactory.get_from_data_frame(
            calculation_result_date=data_frame['date'][0],
            liquid=data_frame['liquid'][0],
            oil=data_frame['oil'][0],
            water=data_frame['water'][0],
            wct=data_frame['wct'][0],
            time_spent=time_spent_on_calculation,
            calculation_id=calculation_id
        )
        await CalculationRepository(session).add_model(complete_calculation_data)
