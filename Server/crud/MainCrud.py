from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from datetime import datetime
from Server.models import TodoListModel, UserModel
from Server.schemas import TodoListSchema
import openai
import os
from dotenv import load_dotenv


def get_todos(db: Session):  # 투두리스트 조회
    return db.query(TodoListModel.TodoList).all()


def create_todo(db: Session, todo: TodoListSchema.TodoCreate):  # 투두리스트 작성
    db_todo = TodoListModel.TodoList(todo=todo.todowrite,
                                     date=datetime.now())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo_update: TodoListSchema.TodoUpdate):  # 투두리스트 수정
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id).first()
    if db_todo:
        db_todo.date = todo_update.tododate
        db_todo.todo = todo_update.todowrite
        db_todo.check = todo_update.todocheck
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):  # 투두리스트 삭제
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo


def check_todo(db: Session, todo_id: int, todo_check: TodoListSchema.TodoCheck):  # 투두리스트 완료 기능
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id).first()
    if db_todo:
        db_todo.check = todo_check.todocheck
        db.commit()
        db.refresh(db_todo)
    return db_todo

# 추천 todo리스트


def get_recommended_todo(db: Session):
    # 데이터베이스에서 모든 투두 항목을 가져옵니다.
    todo_items = db.query(TodoListModel.TodoList.todo).all()
    todo_texts = [item.todo for item in todo_items]

    # OpenAI API를 사용하여 투두 항목을 분류합니다.
    classifications = classify_todo_items(todo_texts)

    # 분류 결과를 기반으로 상위 3개의 추천 항목을 선택합니다.
    classification_count = {}
    for classification in classifications:
        if classification in classification_count:
            classification_count[classification] += 1
        else:
            classification_count[classification] = 1

    sorted_classifications = sorted(
        classification_count.items(), key=lambda x: x[1], reverse=True)
    top_3_classifications = sorted_classifications[:3]

    return top_3_classifications


# 추천 todo 작성 api 불러오기
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"


def classify_todo_items(todo_items):
    prompt = "다음 투두 리스트 항목을 카테고리별로 분류해줘:\n"
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


def get_age_group(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year - \
        ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 20:
        return '10대'
    elif age < 30:
        return '20대'
    elif age < 40:
        return '30대'
    else:
        return '40대 이상'


def get_recommended_todo_by_age_group(db: Session, age_group: str):
    # 데이터베이스에서 해당 연령대의 모든 투두 항목을 가져옵니다.
    users_in_age_group = db.query(UserModel.UserInfo.id).filter(
        UserModel.UserInfo.age_group == age_group).subquery()
    todo_items = db.query(TodoListModel.TodoList.todo).filter(
        TodoListModel.TodoList.user_id.in_(users_in_age_group)).all()
    todo_texts = [item.todo for item in todo_items]

    # OpenAI API를 사용하여 투두 항목을 분류합니다.
    classifications = classify_todo_items(todo_texts)

    # 분류 결과를 기반으로 상위 3개의 추천 항목을 선택합니다.
    classification_count = {}
    for classification in classifications:
        if classification in classification_count:
            classification_count[classification] += 1
        else:
            classification_count[classification] = 1

    sorted_classifications = sorted(
        classification_count.items(), key=lambda x: x[1], reverse=True)
    top_3_classifications = sorted_classifications[:3]

    return top_3_classifications
