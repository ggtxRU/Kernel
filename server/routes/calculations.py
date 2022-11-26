from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.request.calculations import RequestCalculationCreate
from api.response.calculations import ResponseCalculation, ResponseCalculationCreate, ResponseCalculationCreateFactory
from db.models.calculations.input_data import DBCalculationProcessInputData
from managers.calculation import CalculationManager
from server.depends import get_session
from vendors.router import CustomRoute

calculations_router = APIRouter(
    prefix='/calculations',
    tags=['Calculations'],
    route_class=CustomRoute
)


@calculations_router.get(
    '/last',
    response_model=ResponseCalculation,

    description=
    """
    Getting a list of recent calculation runs. 
    Specify the number of calculations required by the \limit\ parameter.
    Default: 10
    """
)
async def get_last_calculations():
    pass


@calculations_router.post(
    '/create',
    response_model=ResponseCalculationCreate,

    description=
    """
    Create new calculation.
    """
)
async def create_calculation(
        request_model: RequestCalculationCreate,
        session: AsyncSession = Depends(get_session),
):
    data_for_calculation: DBCalculationProcessInputData = await CalculationManager.create_new_calculation(
        request_model=request_model, session=session)
    return ResponseCalculationCreateFactory.factory_method(data_for_calculation=data_for_calculation)