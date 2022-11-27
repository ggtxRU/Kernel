import datetime
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class CalculationParams:
    __slots__ = ('date_start', 'date_fin', 'lag')
    date_start: datetime
    date_fin: datetime
    lag: int
