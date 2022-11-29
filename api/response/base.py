from pydantic import BaseModel


class ResponseBase(BaseModel):
    class Config:
        use_enum_values = True
