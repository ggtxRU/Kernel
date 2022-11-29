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
from db.models.calculations.calculation import DBCalculation, DBCalculationProcessInputDataFactory
from db.models.calculations.calculation_result import DBCalculationProcessCompleteFactory
from db.repositories.calculation import CalculationRepository
from server.exceptions.calculation import CalculationNotFoundException

KERNEL = CalculationKernel()


class CalculationManager:
    @classmethod
    async def create_new_calculation(
            cls,
            session: AsyncSession,
            request_model: RequestCalculationCreate
    ) -> DBCalculation:
        """
        Добавляем в импровизированную FIFO очередь новый набор входных данных для выполнения расчета.
        """

        new_calculation: DBCalculation = DBCalculationProcessInputDataFactory.get_from_request_calculation_create(
            request_calculation_create=request_model
        )
        await CalculationRepository(session).add_model(new_calculation)
        return new_calculation

    @staticmethod
    async def get_last_calculation_launches(
            session: AsyncSession,
            limit: int, offset: int, direction: DirectionEnum
    ) -> list[DBCalculation]:
        """
        Получение списка последних N запусков расчетов.

        :param limit: регулировка параметра N.
        """
        return await CalculationRepository(session).get_last_calculation_launches(
            limit=limit, offset=offset, direction=direction)

    @staticmethod
    async def get_by_id(
            session: AsyncSession,
            id: int
    ) -> Optional[DBCalculation]:
        """
        Получение одного конкретного расчета по id.

        :param id: id расчета.
        """
        calculation: Optional[DBCalculation] = await CalculationRepository(
            session).get_by_id_with_complete_result(id_=id)

        if not calculation:
            """
            В случае, если расчета с указанным id не существует.
            """
            raise CalculationNotFoundException.raise_with_value(id)
        return calculation

    @classmethod
    async def calculation_process_prepare_and_do(
            cls,
            session: AsyncSession,
    ) -> None:
        """
        Получаем 3 набора входных данных для выполнения расчета генерации промысловых показателей
         нефтянной скважины для каждого набора.
        """
        calculations_in_queue: list[DBCalculation] = await CalculationRepository(
            session).get_from_top_of_the_queue()

        """
        Если очередь с параметрами, ожидающими выполнения, не пуста - заходим в цикл.
        Иначе - нет смысла продолжать непрерывную работу воркера.
        """
        if len(calculations_in_queue) >= 1:

            for calculation in calculations_in_queue:
                """Подготовка данных для отправки в CalculationKernel."""
                calculation_params_: CalculationParams = await cls.__get_data_for_calculation_from_json(
                    json_params=calculation.input_data)

                start_time_calculation_process = time.monotonic()

                """Меняем статус расчета -> /В процессе выполнения/."""
                await cls.__change_calculation_status_to_in_progress(calculation=calculation, session=session)

                """Запуска процесса выполнения расчета."""
                result_data_frame: DataFrame = await cls.__do_calculation_and_return_result_data_frame(
                    calculation_params=calculation_params_)

                """
                :param time_spent_on_calculation: Время затраченное на выполнение расчета.
                """
                time_spent_on_calculation = time.monotonic() - start_time_calculation_process

                """Сохраняем полученный результат в БД."""
                await cls.__add_calculation_result_in_db(
                    session=session,
                    data_frame=result_data_frame,
                    time_spent_on_calculation=time_spent_on_calculation,
                    calculation_id=calculation.id
                )

                """Меняем статус расчета -> /Завершен/."""
                await cls.__change_calculation_status_to_complete(calculation=calculation, session=session)
        else:
            time.sleep(2.5)

    @classmethod
    async def __get_data_for_calculation_from_json(
            cls, json_params: json
    ) -> CalculationParams:
        """
        :param json_params: {'date_start': 'YYYY-MM-DD', 'date_fin': 'YYYY-MM-DD', 'lag': int}
        """
        return CalculationParams(
            date_start=datetime.fromisoformat(json_params['date_start']),
            date_fin=datetime.fromisoformat(json_params['date_fin']),
            lag=json_params['lag']
        )

    @staticmethod
    async def __change_calculation_status_to_in_progress(
            calculation: DBCalculation, session: AsyncSession
    ) -> None:
        calculation.status = CalculationStatusEnum.in_progress
        calculation.calculation_start_date = datetime.now()
        await session.flush()
        await session.commit()

    @staticmethod
    async def __change_calculation_status_to_complete(
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
