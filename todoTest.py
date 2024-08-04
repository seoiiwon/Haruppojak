from typing import List
from Server.config.database import SessionLocal
from Server.crud.MainCrud import create_todo, update_todo, delete_todo, check_todo, create_intro_todos
from Server.models import TodoListModel
from Server.schemas.TodoListSchema import TodoCreate, TodoCreateRequest, TodoUpdate, TodoCheck
from datetime import datetime

db = SessionLocal()

todo_create1 = TodoCreate(
    user_id=1,
    todowrite="테스트 1",
    tododate=datetime.now(),
    todocheck=False
)

todo_create2 = TodoCreate(
    user_id=1,
    todowrite="테스트 2",
    tododate=datetime.now(),
    todocheck=False
)

todo_create3 = TodoCreate(
    user_id=1,
    todowrite="테스트 3",
    tododate=datetime.now(),
    todocheck=False
)

# todo_update = TodoUpdate(
#     id=3,
#     user_id=1,
#     todowrite="안녕하세요로 수정",
#     tododate=datetime.now(),
#     todocheck=True
# )

# todo_check = TodoCheck(
#     id=4,
#     todocheck=True
# )

todo_intro_create = TodoCreateRequest(
    todos=[todo_create1, todo_create2, todo_create3]
)


# create_todo(db=db, todo=todo_create, user_id=todo_create.user_id)
# update_todo(db=db, todo_id=todo_update.id, user_id=todo_update.user_id,
#             todo_update=todo_update)
# delete_todo(db=db, todo_id=3)
# check_todo(db=db, todo_id=4, todo_check=todo_check)
create_intro_todos(db=db, todo_request=todo_intro_create)
