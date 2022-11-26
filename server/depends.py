from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


def get_session(request: Request) -> AsyncSession:
    return request.state.session
