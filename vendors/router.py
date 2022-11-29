import traceback
from typing import Callable, Optional

from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from api.response.exceptions.base import ResponseBadRequestException, ResponseForbiddenException, \
    ResponseInternalServerException, ResponseNotFoundException, ResponseUnprocessableException, ResponseTimeoutException
from server.exceptions.base import BaseServerException, ServerInternalException
from vendors.app import Application


class CustomRoute(APIRoute):

    __app: Optional[Application] = None

    @classmethod
    def set_app(cls, app: Application) -> None:
        cls.__app = app

    @classmethod
    def get_app(cls) -> Application:
        if not cls.__app:
            raise ValueError
        return cls.__app

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            session = self.get_app().create_async_session()
            config = self.get_app().config

            request.state.session = session
            request.state.config = config

            try:
                response: Response = await original_route_handler(request)
                await session.commit()

            except BaseServerException as e:
                status_code = e.status_code
                if status_code == 400:
                    class_ = ResponseBadRequestException
                elif status_code == 401:
                    class_ = ResponseForbiddenException
                elif status_code == 404:
                    class_ = ResponseNotFoundException
                elif status_code == 422:
                    class_ = ResponseUnprocessableException
                elif status_code == 504:
                    class_ = ResponseTimeoutException
                else:
                    class_ = ResponseInternalServerException

                response = JSONResponse(
                    status_code=status_code,
                    content=class_(
                        code=e.code,
                        message=e.message
                    ).dict()
                )
            except RequestValidationError:
                await session.rollback()
                raise
            except HTTPException:
                await session.rollback()
                raise
            except BaseException:
                await session.rollback()

                print(traceback.format_exc())

                status_code = 500
                response = JSONResponse(
                    status_code=status_code,
                    content=ResponseInternalServerException(
                        code=ServerInternalException.code,
                        message=ServerInternalException.message
                    ).dict()
                )
            finally:
                await session.close()

            return response

        return custom_route_handler
