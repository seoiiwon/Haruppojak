from Server.config.database import SessionLocal
from Server.crud.MainCrud import create_todo, update_todo, delete_todo, check_todo
from Server.schemas.TodoListSchema import TodoCreate, TodoUpdate, TodoCheck
from datetime import datetime

db = SessionLocal()

#  todo_create = TodoCreate(
#     todowrite = "테스트",
#     tododate = datetime.now()
# )

# todo_update = TodoUpdate(
#     id=3,
#     todowrite="안녕하세요로 수정",
#     tododate=datetime.now(),
#     todocheck=True
# )

todo_check = TodoCheck(
    id=4,
    todocheck=True
)
# create_todo(db=db, todo=todo_create)
# update_todo(db=db, todo_id=todo_update.id, todo_update=todo_update)
# delete_todo(db=db, todo_id=3)
check_todo(db=db, todo_id=4, todo_check=todo_check)
