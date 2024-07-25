from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# from config.database import get_db
import os

router = APIRouter()

template_dir = os.path.join(os.path.dirname(__file__), "../../Web/templates/AuthPage")
templates = Jinja2Templates(directory=template_dir)

router = APIRouter(prefix="/api")

# @router.get("diary/write", response_class=HTMLResponse)
# async def diarywritehtml(request : Request):
#     return HTMLResponse(name="diary.html",request = request)

# @router.post("/diary/write", status_code=status.HTTP_204_NO_CONTENT)
# async def creatediarys(creatediarys : schemas.CreateDiarySchema, db : Session=Depends(get_db)):
#     crud.CreateDiary(db=db, diary=creatediarys)

DiaryRouter = router