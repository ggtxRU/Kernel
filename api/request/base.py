from pydantic import BaseModel


class RequestBase(BaseModel):
    class Config:
        use_enum_values = True
