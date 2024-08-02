from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from datetime import datetime
from Server.models import TodoListModel
from Server.schemas import TodoListSchema


def get_todos(db: Session):  # 투두리스트 조회
    return db.query(TodoListModel.TodoList).all()


def create_todo(db: Session, todo: TodoListSchema.TodoCreate):  # 투두리스트 작성
    db_todo = TodoListModel.TodoList(todo=todo.todowrite,
                                     date=datetime.now())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo_update: TodoListSchema.TodoUpdate):  # 투두리스트 수정
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id).first()
    if db_todo:
        db_todo.date = todo_update.tododate
        db_todo.todo = todo_update.todowrite
        db_todo.check = todo_update.todocheck
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):  # 투두리스트 삭제
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo


def check_todo(db: Session, todo_id: int, todo_check: TodoListSchema.TodoCheck):  # 투두리스트 완료 기능
    db_todo = db.query(TodoListModel.TodoList).filter(
        TodoListModel.TodoList.id == todo_id).first()
    if db_todo:
        db_todo.check = todo_check.todocheck
        db.commit()
        db.refresh(db_todo)
    return db_todo

# 추천 todo리스트


def get_recommended_todo(db: Session, age_group: str):
    result = db.query(
        TodoListModel.TodoList.todo,
        func.count(TodoListModel.TodoList.todo).label('todo_count')
    ).filter(
        TodoListModel.TodoList.age_group == age_group
    ).group_by(
        TodoListModel.TodoList.todo
    ).order_by(
        desc('todo_count')
    ).limit(3).all()

    return result
