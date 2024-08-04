from pydantic import BaseModel
import datetime
from typing import Optional, List


class TodoCreate(BaseModel):
    user_id: int
    todowrite: str
    tododate: datetime.datetime
    todocheck: Optional[bool] = False


class TodoCreateRequest(BaseModel):
    todos: List[TodoCreate]


class TodoUpdate(BaseModel):
    id: int
    user_id: int
    todowrite: str
    tododate: datetime.datetime
    todocheck: bool


class TodoCheck(BaseModel):
    id: int
    user_id: int
    todocheck: bool


class TopTodoRecommendations(BaseModel):
    recommendations: List[str]
