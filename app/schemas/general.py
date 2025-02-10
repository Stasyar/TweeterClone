from pydantic import BaseModel


class BaseSchema(BaseModel):
    pass


class ResponseWithBool(BaseSchema):
    result: bool


class ErrorResponse(BaseSchema):
    result: bool
    error_type: str
    error_message: str
