from collections import defaultdict
from typing import Optional
from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from Server.models import TodoListModel, UserInfo
from Server.schemas import TodoListSchema
import openai
import os
from dotenv import load_dotenv


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
                                     date=todo.tododate, user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# intro 투두리스트 작성
def create_intro_todos(db: Session, todo_request: TodoListSchema.TodoCreateRequest):
    db_todos = []
    for todo in todo_request.todos:
        db_todo = TodoListModel.TodoList(
            todo=todo.todowrite,
            date=todo.tododate,
            user_id=todo.user_id
        )
        db_todos.append(db_todo)
        db.add(db_todo)

    db.commit()
    for db_todo in db_todos:
        db.refresh(db_todo)

    return db_todos


# 투두리스트 수정
def update_todo(db: Session, todo_id: int, todo_update: TodoListSchema.TodoUpdate, user_id: int):
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id, TodoListModel.TodoList.user_id == user_id).first()
    if db_todo:
        db_todo.date = todo_update.tododate
        db_todo.todo = todo_update.todowrite
        db_todo.check = todo_update.todocheck
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
def get_user_age_group(user_id : int, db : Session):
    user = db.query(UserInfo).filter(UserInfo.id == user_id).first()
    return get_user_age(user.userBirth) // 10

# 연령대 별 투두 함수
def get_age_group_todo_data(user_age_group : int, db : Session):
    ageGroup = db.query(UserInfo).filter(get_user_age_group(UserInfo.id, db) == user_age_group).all()
    userList = [user.id for user in ageGroup]
    todoListAll = []
    for user in userList:
        user_todo = db.query(TodoListModel.TodoList).filter(TodoListModel.TodoList.user_id == user).all()
        for todo in user_todo:
            todoListAll.append(todo.todo)
    return todoListAll

# 투두 추천 리스트 코드
def recommend_todo_list(todolist : list, current_user_id : int, db : Session):
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY
    model = "gpt-4o"

    query = "todolist라는 리스트 전체를 분석해서 비슷한 유형들은 하나로 통일하고 가장 빈도수가 많은 값, 또는 자주 언급되는 todolist 중 너가 생각하기에 " + str(get_user_age_group(current_user_id, db)) +"0대가 하면 좋을 생산적인일 5개 리스트로 반환해줘. 리스트 자료형으로만 반환해줘"
    todolist_str = ", ".join(todolist)

    messages = [{
        "role" : "system",
        "content" : todolist_str
    }, {
        "role" : "user",
        "content" : query
    }]
    completion = openai.chat.completions.create(model=model, messages=messages)
    print(completion.choices[0].message.content)



# DB에서 연령대 유저 가져오기.
def get_recommended_todo_by_age_group(db: Session, age_group: str):
    users = db.query(UserInfo).all()

    age_group_todos = defaultdict(list)  # 연령대별로 딕셔너리 생성

    # 각 유저의 연령대와 참여한 todo를 계산
    for user in users:
        user_age_group = get_user_age_group(user)
        if user_age_group == age_group:
            todo_items = db.query(TodoListModel.TodoList).filter_by(
                user_id=user.id).all()
            for todo_item in todo_items:
                age_group_todos[age_group].append(todo_item.todo)

    todo_texts = age_group_todos[age_group]
    classifications = classify_todo(todo_texts)

    classification_count = defaultdict(int)
    for classification in classifications:
        classification_count[classification] += 1

    sorted_classifications = sorted(
        classification_count.items(), key=lambda x: x[1], reverse=True)
    top_3_classifications = sorted_classifications[:3]

    return top_3_classifications


# 이게 필요한가??
def print_recommendations(db: Session):
    age_groups = ["10대", "20대", "30대", "40대", "50대 이상"]
    for age_group in age_groups:
        recommendations = get_recommended_todo_by_age_group(db, age_group)
        print(f"{age_group}: {recommendations}")
