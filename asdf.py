from Server.config.database import SessionLocal
from Server.models import TodoListModel
from datetime import datetime

db = SessionLocal()

newtodo = TodoListModel.TodoList(
    date=datetime.now(),
    todo="배고프기",
    check=False,
    user_id=1,
)

db.add(newtodo)
db.commit()
