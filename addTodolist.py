from Server.config.database import SessionLocal
from Server.models import TodoListModel
from datetime import datetime

db = SessionLocal()

newtodo = TodoListModel.TodoList(
    date = datetime.now(),
    todo = "밥 먹기",
    check = False,
    user_id = 1,    
)

db.add(newtodo)
db.commit()