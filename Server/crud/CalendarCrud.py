from sqlalchemy.orm import Session
from datetime import datetime, timezone
from Server.models import ChallengeModel, UserChallenge, TodoListModel
from Server.config.database import SessionLocal
from Server.schemas import AuthSchema
from fastapi import HTTPException, UploadFile
import shutil
from pathlib import Path
import os
from typing import List

# 뽀짝한 날 = 투두를 작성한 날

# def ppojakDay(currentUser: AuthSchema.UserInfoSchema.id, month: int, db: Session):
#     current_year = datetime.now().year
#     user_todos = db.query(TodoListModel.TodoList).filter(TodoListModel.TodoList.user_id == currentUser).all()
#     unique_days = set()

#     for todo in user_todos:
#         todo_date = datetime.strptime(todo.date, '%Y-%m-%d %H:%M:%S.%f')
#         if todo_date.year == current_year and todo_date.month == month:
#             unique_days.add(todo_date.day)
    
#     ppojak_day = len(unique_days)

#     return ppojak_day

# db = SessionLocal()
# month = 8
# currentUser_id = 2

# ppojakDay(currentUser_id, month, db)
        

# 뽀짝퍼센트 = 투두 체크 비율

# 완벽 뽀짝한 날 = 투두를 모두 달성한 날 