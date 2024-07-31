# from config.database import SessionLocal, engine
# from models.TodoListModel import Base, TodoList
# from crud.MainCrud import get_todos, create_todo, update_todo, delete_todo, check_todo
# from schemas.TodoListSchema import TodoCreate, TodoUpdate, TodoCheck
# from datetime import datetime

from Server.config.database import SessionLocal
from Server.crud.MainCrud import create_todo
from Server.schemas.TodoListSchema import TodoCreate
from datetime import datetime

db = SessionLocal()

todo_create = TodoCreate(
    todowrite="테스트 다시",
    tododate=datetime.now()
)

create_todo(db=db, todo=todo_create)




# try:
#     # Create a new todo item
#     todo_create = TodoCreate(
#         todowrite="테스트 할 일",
#         tododate=datetime.now()
#     )
#     new_todo = create_todo(db=db, todo=todo_create)
#     print(f"Created Todo: {new_todo}")

#     # Retrieve all todos
#     todos = get_todos(db=db)
#     print(f"Retrieved Todos: {todos}")

#     # Update the created todo item
#     todo_update = TodoUpdate(
#         id=new_todo.id,
#         todowrite="수정된 테스트 할 일",
#         tododate=datetime.now(),
#         todocheck=False
#     )
#     updated_todo = update_todo(
#         db=db, todo_id=new_todo.id, todo_update=todo_update)
#     print(f"Updated Todo: {updated_todo}")

#     # Check the todo item
#     todo_check = TodoCheck(todocheck=True)
#     checked_todo = check_todo(
#         db=db, todo_id=new_todo.id, todo_check=todo_check)
#     print(f"Checked Todo: {checked_todo}")

#     # Delete the todo item
#     deleted_todo = delete_todo(db=db, todo_id=new_todo.id)
#     print(f"Deleted Todo: {deleted_todo}")

# except Exception as e:
#     db.rollback()
#     print(f"Error: {e}")

# finally:
#     db.close()
