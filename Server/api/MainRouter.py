from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import get_db

from models import TodoListModel
from schemas import TodoListSchema
from crud import MainCrud
import os

router = APIRouter()

template_dir = os.path.join(os.path.dirname(
    __file__), "../../Web/templates/AuthPage")
templates = Jinja2Templates(directory=template_dir)


@router.get("/todo/all", response_class=HTMLResponse)  # todo 리스트 보기
async def read_todos(request: Request, db: Session = Depends(get_db)):
    todos = get_todos(db)
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})


# todo 만들기
@router.post("/todo/create", response_model=TodoListSchema.TodoCreate)
async def create_new_todo(
    todo: TodoListSchema.TodoCreate, db: Session = Depends(get_db)
):
    return create_todo(db=db, todo=todo)


# todo 수정하기
@router.put("/todo/update/{todo_id}", response_model=TodoListSchema.TodoUpdate)
async def update_new_todo(
    todo_id: int, todo: TodoListSchema.TodoUpdate, db: Session = Depends(get_db)
):
    return update_todo(db=db, todo_id=todo_id, todo_update=todo)


# todo 삭제하기
@router.delete("/todo/delete/{todo_id}", response_model=TodoListSchema.TodoList)
async def delete_existing_todo(
    todo_id: int, db: Session = Depends(get_db)
):
    return delete_todo(db=db, todo_id=todo_id)


@router.check("/todo/check/{todo_id}", response_model=TodoListSchema.TodoCheck)
async def check_existing_todo(
    todo_id: int, todo: TodoListSchema.TodoCheck, db: Session = Depends(get_db)
):
    return check_todo(db=db, todo_id=todo_id, todo_check=todo)
Main_router = router
