from sqlalchemy.orm import Session
from datetime import datetime
from models import TodoListModel
from schemas import TodoListSchema

def loadTodoList(db : Session):
    todoList = db.query(TodoListModel.TodoList).all()
    db.query()
    return todoList

def get_todos(db: Session):
    return db.query(TodoListModel.TodoList).all()


def create_todo(db: Session, todo: TodoListSchema.TodoCreate):
    db_todo = TodoListModel.TodoList(todo=todo.todowrite,
                       date=datetime.now())
    db.add(db_todo)
    db.commit()