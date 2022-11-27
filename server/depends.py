from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from db.enum.direction import DirectionEnum


def get_session(request: Request) -> AsyncSession:
    return request.state.session


class PagesPaginationParamsWithDirection:

    def __init__(
            self,
            limit: int = Query(10, ge=0, le=1_000),
            offset: int = Query(0, ge=0, alias='skip'),
            direction: DirectionEnum = Query(DirectionEnum.direct)
    ) -> None:
        self.limit = limit
        self.offset = offset
        self.direction = direction
