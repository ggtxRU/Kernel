from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.calculations import RequestCalculationCreate
from api.response.calculations import ResponseCalculationSimple, ResponseCalculationCreate, \
    ResponseCalculationCreateFactory, \
    ResponseCalculationFactorySimple, ResponseCalculationFactoryWithCompleteResult, \
    ResponseCalculationWithCompleteResult
from db.enum.calculations import CalculationStatusEnum
from db.models.calculations.calculation import DBCalculation
from managers.calculation import CalculationManager
from server.depends import get_session, PagesPaginationParamsWithDirection
from vendors.router import CustomRoute

calculations_router = APIRouter(
    prefix='/calculations',
    tags=['Calculations'],
    route_class=CustomRoute
)


@calculations_router.get(
    '/last',
    response_model=list[ResponseCalculationSimple],
    description="""
    Getting a list of recent calculation runs.
    Specify the number of calculations required by the \limit\ parameter.
    Default: 10
    """
)
async def get_last_calculations(
        session: AsyncSession = Depends(get_session),
        pagination_params: PagesPaginationParamsWithDirection = Depends(),
):
    calculation_data: list[DBCalculation] = await CalculationManager.get_last_calculation_launches(
        limit=pagination_params.limit,
        offset=pagination_params.offset,
        session=session,
        direction=pagination_params.direction
    )
    return ResponseCalculationFactorySimple.get_many_from_calculation_data(calculation_data)


@calculations_router.get(
    '/{calculation_id}',
    response_model=Optional[ResponseCalculationWithCompleteResult],
    description="""
    Get a specific calculation by ID
    """
)
async def get_calculation_by_id(
        calculation_id: int,
        session: AsyncSession = Depends(get_session),
        q: Optional[list[str]] = Query(
            default=[],
            alias='fields',
            description="""
            Valid values: name, time-spent
            """,
            example='name'

        )
):
    calculation: Optional[DBCalculation] = await CalculationManager.get_by_id(session=session, id=calculation_id)
    return ResponseCalculationFactoryWithCompleteResult.get_from_calculation_data(
        calculation_data=calculation, q=q) if calculation.status == CalculationStatusEnum.complete else None


@calculations_router.post(
    '/create',
    response_model=ResponseCalculationCreate,
    description="""
    Create new calculation.
    """
)
async def create_calculation(
        request_model: RequestCalculationCreate,
        session: AsyncSession = Depends(get_session),
):
    data_for_calculation: DBCalculation = await CalculationManager.create_new_calculation(
        request_model=request_model, session=session)
    return ResponseCalculationCreateFactory.factory_method(data_for_calculation=data_for_calculation)
