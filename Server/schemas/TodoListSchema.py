from pydantic import BaseModel
import datetime
from typing import Optional, List


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


class TopTodo(BaseModel):
    todo: str
    todo_count: int
