from collections import defaultdict
from sqlalchemy.orm import Session
from datetime import datetime
from Server.models import TodoListModel, UserInfo
from Server.schemas import TodoListSchema
import openai
import os
from dotenv import load_dotenv


# 투두리스트 조회
def get_todos(db: Session):
    return db.query(TodoListModel.TodoList).all()


# 투두리스트 작성
def create_todo(db: Session, todo: TodoListSchema.TodoCreate):
    db_todo = TodoListModel.TodoList(todo=todo.todowrite,
                                     date=datetime.now())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# 투두리스트 수정
def update_todo(db: Session, todo_id: int, todo_update: TodoListSchema.TodoUpdate):
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id).first()
    if db_todo:
        db_todo.date = todo_update.tododate
        db_todo.todo = todo_update.todowrite
        db_todo.check = todo_update.todocheck
        db.commit()
        db.refresh(db_todo)
    return db_todo


# 투두리스트 삭제
def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo


# 투두리스트 완료 기능
def check_todo(db: Session, todo_id: int, todo_check: TodoListSchema.TodoCheck):
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id).first()
    if db_todo:
        db_todo.check = todo_check.todocheck
        db.commit()
        db.refresh(db_todo)
    return db_todo


# 나이 계산 코드
def get_user_age(birth_date: int) -> int:
    birth_date_str = str(birth_date)
    birth_year = int(birth_date_str[:4])
    birth_month = int(birth_date_str[4:6])
    birth_day = int(birth_date_str[6:8])

    today = datetime.today()
    age = today.year - birth_year - \
        ((today.month, today.day) < (birth_month, birth_day))
    return age


# 연령대 구분 코드
def get_user_age_group(user: UserInfo) -> str:
    age = get_user_age(user.userBirth)
    if 10 <= age < 20:
        return "10대"
    elif 20 <= age < 30:
        return "20대"
    elif 30 <= age < 40:
        return "30대"
    elif 40 <= age < 50:
        return "40대"
    else:
        return "50대 이상"


# OpenAPI ChatGPT 불러오기 코드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"


def classify_todo(todo_items):
    prompt = "다음 todo들을 카테고리별로 분류해줘:\n"
    for item in todo_items:
        prompt += f"- {item}\n"
    prompt += "\n분류된 카테고리:"

    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=150,
        temperature=0.5,
    )

    classifications = response.choices[0].text.strip().split("\n")
    return classifications


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
