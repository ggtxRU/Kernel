import datetime
from typing import Optional

from pydantic import Field

from api.request.base import RequestBase


class RequestCalculationCreate(RequestBase):
    name: Optional[str] = Field(None)

    date_start: datetime.date = Field(...)
    date_fin: datetime.date = Field(...)
    lag: int = Field(..., gt=0)
