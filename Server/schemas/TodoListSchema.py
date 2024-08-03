from pydantic import BaseModel
import datetime
from typing import Optional, List


class TodoCreate(BaseModel):
    todowrite: str
    tododate: datetime.datetime
    todocheck: bool

class TodoCreateRequest(BaseModel):
    todos: List[TodoCreate]

class TodoUpdate(BaseModel):
    id: int
    todowrite: str
    tododate: datetime.datetime
    todocheck: bool

class TodoCheck(BaseModel):
    todocheck: bool
