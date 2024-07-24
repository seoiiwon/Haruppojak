from sqlalchemy.orm import Session
from datetime import datetime
from api.models import *
from api.schema import *

def loadTodoList(db : Session):
    todoList = db.query(TodoList).all()
    db.query()
    return todoList

def creatediary(db: Session, diary: CreateDiarySchema):
    diary = UserDiary(content = diary.content,
                      date = datetime.now())
    db.add(diary)


def get_todos(db: Session):
    return db.query(TodoList).all()


def create_todo(db: Session, todo: TodoCreate):
    db_todo = TodoList(todo=todo.todowrite,
                       date=datetime.now())
    db.add(db_todo)
    db.commit()
