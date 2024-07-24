from pydantic import BaseModel, field_validator
import datetime
from typing import Optional


class TodoCreate(BaseModel):
    todowrite: str
    tododate: datetime.datetime


class TodoUpdate(BaseModel):
    id: int
    todowrite: str
    tododate: datetime.datetime
    todocheck: bool


class TodoCheck(BaseModel):
    todocheck: bool
