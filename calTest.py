from sqlalchemy.orm import Session
from datetime import datetime, timezone
from Server.models import ChallengeModel, UserChallenge, TodoListModel
from Server.config.database import SessionLocal
from Server.schemas import AuthSchema
from fastapi import HTTPException, UploadFile
from datetime import datetime, timedelta
from collections import defaultdict

# 뽀짝한 날 = 투두를 작성한 날

def getMonthTodo(currentUser : int, month : int, db : Session):
    year = datetime.now().year
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)

    # 해당 월의 투두 리스트 가져오기
    user_todo_1month = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.user_id == currentUser,
        TodoListModel.TodoList.date >= start_date,
        TodoListModel.TodoList.date <= end_date).all()
    
    return user_todo_1month

def ppojakDay(currentUser: int, month: int, db: Session):
    current_year = datetime.now().year
    user_todos = db.query(TodoListModel.TodoList).filter(TodoListModel.TodoList.user_id == currentUser).all()
    unique_days = set()

    for todo in user_todos:
        if todo.date.year == current_year and todo.date.month == month:
            unique_days.add(todo.date.day)
    
    ppojak_day = len(unique_days)

    return ppojak_day
        

# 뽀짝퍼센트 = 투두 체크 비율
def ppojakPercent(currentUser: int, month: int, db: Session):
    user_todo_1month = getMonthTodo(currentUser, month, db)
    count = 0
    for todo in user_todo_1month:
        if todo.check == 1:
            count += 1
    return int(count / len(db.query(TodoListModel.TodoList).filter(TodoListModel.TodoList.user_id == currentUser_id).all()))


# 완벽 뽀짝한 날 = 투두를 모두 달성한 날 
def ppojakcomplete(currentUser: int, month: int, db: Session):
    user_todo_1month = getMonthTodo(currentUser, month, db)
    todos_by_day = defaultdict(list)
    for todo in user_todo_1month:
        todos_by_day[todo.date.date()].append(todo)

    # 모든 투두리스트가 달성된 날 계산
    complete_days_count = 0
    for date, todos in todos_by_day.items():
        if all(todo.check for todo in todos):
            complete_days_count += 1

    return complete_days_count


db = SessionLocal()
month = 8
currentUser_id = 2

print(ppojakDay(currentUser_id, month, db))
print(ppojakPercent(currentUser_id, month, db))
print(ppojakcomplete(currentUser_id, month, db))
