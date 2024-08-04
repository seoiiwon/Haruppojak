from Server.config.database import SessionLocal
from Server.models import TodoListModel, UserModel
from datetime import datetime
from sqlalchemy.orm import Session
import openai
import os
from dotenv import load_dotenv

db = SessionLocal()

def get_user_age(birth_date: int) -> int:
    birth_date_str = str(birth_date)
    birth_year = int(birth_date_str[:4])
    birth_month = int(birth_date_str[4:6])
    birth_day = int(birth_date_str[6:8])

    today = datetime.today()
    age = today.year - birth_year - \
        ((today.month, today.day) < (birth_month, birth_day))
    return age

def get_user_age_group(user_id : int, db : Session):
    user = db.query(UserModel.UserInfo).filter(UserModel.UserInfo.id == user_id).first()
    return get_user_age(user.userBirth) // 10

def get_age_group_todo_data(user_age_group : int, db : Session):
    ageGroup = db.query(UserModel.UserInfo).filter(get_user_age_group(UserModel.UserInfo.id, db) == user_age_group).all()
    userList = [user.id for user in ageGroup]
    todoListAll = []
    for user in userList:
        user_todo = db.query(TodoListModel.TodoList).filter(TodoListModel.TodoList.user_id == user).all()
        for todo in user_todo:
            todoListAll.append(todo.todo)
    return todoListAll


def helpAI(todolist : list, current_user_id : int):
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

current_user_id = 3
helpAI(get_age_group_todo_data(get_user_age_group(current_user_id, db), db), current_user_id)