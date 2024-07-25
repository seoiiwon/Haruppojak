from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.config.database import get_db

from Server.models.TodoListModel import *
from Server.schemas.TodoListSchema import *
from Server.crud.MainCrud import *
import os

router = APIRouter()

template_dir = os.path.join(os.path.dirname(
    __file__), "../../Web/templates/AuthPage")
templates = Jinja2Templates(directory=template_dir)

# todo 리스트 보기


@router.get("/todo/all", response_class=HTMLResponse)
async def read_todos(request: Request, db: Session = Depends(get_db)):
    todos = get_todos(db)
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

# todo 리스트 만들기


@router.post("/todo/create", response_model=TodoListSchema.TodoCreate)
async def create_todo(
    todo: TodoListSchema.TodoCreate, db: Session = Depends(get_db)
):
    return create_todo(db=db, todo=todo)


Main_router = router
