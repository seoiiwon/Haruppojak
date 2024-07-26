from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.crud.DiaryCrud import *
from Server.schemas.DiarySchema import *
from Server.config.database import get_db
import os

router = APIRouter()

template_dir = os.path.join(os.path.dirname(__file__), "../../Web/templates/DiaryPage")
templates = Jinja2Templates(directory=template_dir)


@router.get("/diary/write", response_class=HTMLResponse)
async def getSignInPage(request : Request):
    return templates.TemplateResponse("writeDiary.html", {"request" : request})

@router.post("/diary/write", status_code=status.HTTP_204_NO_CONTENT)
async def creatediarys(creatediarys : CreateDiarySchema, db : Session=Depends(get_db)):
    return CreateDiary(db=db, diary=creatediarys)

DiaryRouter = router