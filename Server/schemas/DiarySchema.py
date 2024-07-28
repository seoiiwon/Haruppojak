from pydantic import BaseModel, field_validator
import datetime
from typing import Optional

class CreateDiarySchema(BaseModel):
    content : str
    response : str
    todo : str

    @field_validator("content")
    def empty_vaildation(cls, valid) :
        if not valid or not valid.strip():
            raise ValueError("일기를 작성해주세요.")
        return valid