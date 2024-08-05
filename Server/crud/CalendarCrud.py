from sqlalchemy.orm import Session
from datetime import datetime, timezone
from Server.models import ChallengeModel, UserChallenge, TodoListModel
from Server.schemas import AuthSchema
from fastapi import HTTPException, UploadFile
import shutil
from pathlib import Path
import os
from typing import List

# 뽀짝한 날 = 투두를 작성한 날
def ppojakDay(currentUser : AuthSchema.UserInfoSchema, month : int, todo : TodoListModel.TodoList ,db : Session):
    
    date = str(todo.date)[5:7]
    userMonthTodo = db.query(TodoListModel.TodoList).filter(currentUser.id == todo.user_id, month == date).all()
    ppojak_day = 0
    for day in (1, 32):
        for todolist in userMonthTodo:
            if int(str(todolist.date)[5:7]) == day:
                ppojak_day += 1
                break 
    return ppojak_day

        

# 뽀짝퍼센트 = 투두 체크 비율

# 완벽 뽀짝한 날 = 투두를 모두 달성한 날 