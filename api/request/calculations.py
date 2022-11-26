import datetime

from pydantic import Field

from api.request.base import RequestBase


class RequestCalculationCreate(RequestBase):
    date_start: datetime.date = Field(...)
    date_fin: datetime.date = Field(...)
    lag: int = Field(...)
