from Server.config.database import SessionLocal
from Server.models import TodoListModel
from datetime import datetime

db = SessionLocal()

newtodo = TodoListModel.TodoList(
    date=datetime.now(),
    todo="으어어죽여줘",
    check=True,
    user_id=2,
)

db.add(newtodo)
db.commit()
