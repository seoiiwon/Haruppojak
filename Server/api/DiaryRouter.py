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


@router.get("/diary", response_class=HTMLResponse)
async def writediaryhtml(request : Request):
    return templates.TemplateResponse("access.html", {"request" : request})

@router.get("/diary/write", response_class=HTMLResponse)
async def writediaryhtml(request : Request):
    return templates.TemplateResponse("writeDiary.html", {"request" : request})

@router.post("/diary/write", status_code=status.HTTP_204_NO_CONTENT)
async def writediarys(writediarys : CreateDiarySchema, db : Session=Depends(get_db)):
    CreateDiary(db=db, diary=writediarys)

@router.get("/diary/reply", response_class=HTMLResponse)
async def diaryreplyhtml(request : Request):
    return templates.TemplateResponse("reply.html", {"request" : request})

# @router.get("diary/detail/{id}", response_class=HTMLResponse)
# async def diarydetailhtml(request:Request,id:int,db:Session=Depends(get_db)):
#     diary=getdiarydetail(db,id=id)

DiaryRouter = router