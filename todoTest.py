from typing import List
from Server.config.database import SessionLocal
from Server.crud.MainCrud import create_todo, update_todo, delete_todo, check_todo, create_intro_todos
from Server.models import TodoListModel
from Server.schemas.TodoListSchema import TodoCreate, TodoCreateRequest, TodoUpdate, TodoCheck
from datetime import datetime

db = SessionLocal()
특정_날짜 = datetime(2024, 8, 1)

todo_create = TodoCreate(
    user_id=3,
    todowrite="8월 1일 데이터 입니다",
    tododate=특정_날짜,
    todocheck=False
)

# todo_create1 = TodoCreate(
#     user_id=3,
#     todowrite="이게",
#     tododate=datetime.now(),
#     todocheck=False
# )

# todo_create2 = TodoCreate(
#     user_id=3,
#     todowrite="되네",
#     tododate=datetime.now(),
#     todocheck=False
# )

# todo_create3 = TodoCreate(
#     user_id=3,
#     todowrite="뭐지",
#     tododate=datetime.now(),
#     todocheck=False
# )

# todo_update = TodoUpdate(
#     id=3,
#     user_id=1,
#     todowrite="안녕하세요로 수정",
#     tododate=datetime.now(),
#     todocheck=True
# )

# todo_delete = delete_todo

# todo_check = TodoCheck(
#     id=4,
#     todocheck=True
# )


# intro 부분 투두리스트
# todo_intro_create = TodoCreateRequest(
#     todos=[todo_create1, todo_create2, todo_create3]
# )


create_todo(db=db, todo=todo_create, user_id=todo_create.user_id)
# update_todo(db=db, todo_id=todo_update.id, user_id=todo_update.user_id,
#             todo_update=todo_update)
# delete_todo(db=db, todo_id=5, user_id=3)
# check_todo(db=db, todo_id=4, todo_check=todo_check)
# create_intro_todos(db=db, todo_request=todo_intro_create)
