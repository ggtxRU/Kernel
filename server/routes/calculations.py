from fastapi import APIRouter

from api.response.calculations import ResponseCalculation, ResponseCalculationTiny

calculations_router = APIRouter(
    prefix='/calculations',
    tags=['Calculations']
)


@calculations_router.get(
    '/last',
    description=
    """
    Getting a list of recent calculation runs. 
    Specify the number of calculations required by the \limit\ parameter.
    Default: 10
    """,
    response_model=ResponseCalculation
)
async def get_last_calculations():
    pass


@calculations_router.post(
    '/create',
    description=
    """
    Create calculation.
    """,
    response_model=ResponseCalculationTiny
)
async def create_calculation():
    pass