from typing import Callable

from managers.calculation import CalculationManager
from vendors.services.base import BaseService


class CalculationProcessWorkerService(BaseService):

    @property
    def service_name(self) -> str:
        return 'Calculation Worker'

    @property
    def purpose_func(self) -> Callable:

        return CalculationManager.calculation_process_prepare_and_do

    @property
    def time_sleep(self) -> float:
        return 0.1
