from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from api import crud, schema, models
from config.database import get_db

router = APIRouter(prefix="/api")

# @router.get("/post/create", response_class=HTMLResponse)
# async def post_create_html(request : Request):
#     return templates.TemplateResponse(name="post_create.html", request=request)
# 요런 느낌

@router.get("/todo/all", response_class=JSONResponse)
async def readTodoListJson(request: Request, db: Session = Depends(get_db)):
    todoList = crud.loadTodoList(db)
    return JSONResponse(content=todoList)