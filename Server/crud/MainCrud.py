from collections import defaultdict
from typing import Optional
from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from Server.models import TodoListModel, UserInfo,UserDiary
from Server.schemas import TodoListSchema
import openai
import os
from typing import List
from dotenv import load_dotenv
from dateutil import parser
import re

import re


# 투두리스트 조회
def get_todos(db: Session, user_id: int):
    today = datetime.now().date()  # 오늘 날짜
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    todos = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.user_id == user_id,
        TodoListModel.TodoList.date >= start_of_day,
        TodoListModel.TodoList.date <= end_of_day
    ).all()

    return todos


def get_todos_by_date(db: Session, user_id: int, target_date: date):
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date, datetime.max.time())

    todos = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.user_id == user_id,
        TodoListModel.TodoList.date >= start_of_day,
        TodoListModel.TodoList.date <= end_of_day
    ).all()
    return todos


# 투두리스트 작성

def create_todo(db: Session, todo: TodoListSchema.TodoCreate, user_id: int):
    db_todo = TodoListModel.TodoList(todo=todo.todowrite,
                                     date=todo.tododate, user_id=user_id)  # 수정된 부분
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# intro todolist 작성
def create_intro_todos(db: Session, todo_request: TodoListSchema.TodoCreateRequest, user_id: int):
    for todo in todo_request.todos:
        db_todo = TodoListModel.TodoList(
            todo=todo.todowrite,
            date=datetime.now(),
            user_id=user_id,
            check=False
        )
        db.add(db_todo)
    db.commit()





# 투두리스트 수정
def update_todo(db: Session, todo_id: int, todo_update: TodoListSchema.TodoUpdate, user_id: int):
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id, TodoListModel.TodoList.user_id == user_id).first()
    if db_todo:
        # db_todo.date = datetime.now()
        db_todo.todo = todo_update.todowrite
        # db_todo.check = todo_update.todocheck
        db.commit()
        db.refresh(db_todo)
    return db_todo


# 투두리스트 삭제
def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id, TodoListModel.TodoList.user_id == user_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo


# 투두리스트 완료 기능
def check_todo(db: Session, todo_id: int, todo_check: TodoListSchema.TodoCheck, user_id: int):
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id, TodoListModel.TodoList.user_id == user_id).first()
    if db_todo:
        db_todo.check = todo_check.todocheck
        db.commit()
        db.refresh(db_todo)
    return db_todo


# 나이 계산 함수
def get_user_age(birth_date: int) -> int:
    birth_date_str = str(birth_date)
    birth_year = int(birth_date_str[:4])
    birth_month = int(birth_date_str[4:6])
    birth_day = int(birth_date_str[6:8])

    today = datetime.today()
    age = today.year - birth_year - \
        ((today.month, today.day) < (birth_month, birth_day))
    return age

# 연령대 구분 함수
def get_user_age_group(user_id: int, db: Session):
    user = db.query(UserInfo).filter(UserInfo.id == user_id).first()
    return get_user_age(user.userBirth) // 10

# 연령대 별 투두 함수


def get_age_group_todo_data(user_age_group: int, db: Session):
    ageGroup = db.query(UserInfo).filter(
        get_user_age_group(UserInfo.id, db) == user_age_group).all()
    userList = [user.id for user in ageGroup]
    todoListAll = []
    for user in userList:
        user_todo = db.query(TodoListModel.TodoList).filter(
            TodoListModel.TodoList.user_id == user).all()
        for todo in user_todo:
            todoListAll.append(todo.todo)
    return todoListAll

# 투두 추천 리스트 코드
def recommend_todo_list(todolist: list, current_user_id: int, db: Session):
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY
    model = "gpt-4o"

    query = "todolist라는 리스트 전체를 분석해서 비슷한 유형들은 하나로 통일하고 가장 빈도수가 많은 값, 또는 자주 언급되는 todolist 중 너가 생각하기에 " + \
        str(get_user_age_group(current_user_id, db)) + \
        "0대가 하면 좋을 생산적인일 5개 리스트로 반환해줘. 리스트 자료형으로 인덱싱 가능하게 반환해줘 반환 값은 다른 값이 없는 []으로 반환부탁해"
    todolist_str = ", ".join(todolist)

    messages = [{
        "role": "system",
        "content": todolist_str
    }, {
        "role": "user",
        "content": query
    }]
    completion = openai.chat.completions.create(model=model, messages=messages)
    text = completion.choices[0].message.content
    matches = re.findall(r'"(.*?)"', text)
    return matches
    # for match in matches:
    #     items = [item.strip().strip("'") for item in match.split(',')]
    #     print(items)
    #     return items
<<<<<<< HEAD
    
# def checkdiary(db: Session, userid: int):
#     # startdate = datetime(year, month, 1)
#     # enddate = (startdate.replace(day=28) + timedelta(days=4)).replace(day=1)  # 다음 달 1일
    
#     return db.query(UserDiary).filter(
#         UserDiary.Diaryuserid == userid,
#     ).order_by(UserDiary.Date).all()
def checkdiary(db: Session, userid: int):
    return db.query(UserDiary).filter(UserDiary.Diaryuserid == userid).order_by(UserDiary.Date).all()
=======
    
def checkdiary(db: Session, userid: int):
    # startdate = datetime(year, month, 1)
    # enddate = (startdate.replace(day=28) + timedelta(days=4)).replace(day=1)  # 다음 달 1일
    
    return db.query(UserDiary).filter(
        UserDiary.Diaryuserid == userid).order_by(UserDiary.Date).all()
>>>>>>> chaehyun2
