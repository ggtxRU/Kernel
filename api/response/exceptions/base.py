from pydantic import BaseModel, Field


class ResponseBaseException(BaseModel):
    code: int = Field(...)
    message: str = Field(...)


class ResponseInternalServerException(ResponseBaseException):
    pass


class ResponseBadRequestException(ResponseBaseException):
    pass


class ResponseForbiddenException(ResponseBaseException):
    pass


class ResponseNotFoundException(ResponseBaseException):
    pass


class ResponseUnprocessableException(ResponseBaseException):
    pass


class ResponseTimeoutException(ResponseBaseException):
    pass
