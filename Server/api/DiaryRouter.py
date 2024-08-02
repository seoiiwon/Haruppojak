from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.crud.DiaryCrud import *
from Server.schemas.DiarySchema import *
from Server.config.database import get_db
import os

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()

template_diary = os.path.join(os.path.dirname(__file__), "../../Web/templates/DiaryPage")
template_auth = os.path.join(os.path.dirname(__file__), "../../Web/templates/AuthPage")
templates_diary = Jinja2Templates(directory=template_diary)
templates_auth = Jinja2Templates(directory=template_auth)

@router.get("/diary", response_class=HTMLResponse) # 초기 다이어리 페이지
async def getIntroPage(request : Request):
    token = request.cookies.get("access_token")
    if token:
        return templates_diary.TemplateResponse(name="access.html", request=request)
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)

@router.get("/diary/write", response_class=HTMLResponse) # 다이어리 작성 페이지
async def writediaryhtml(request : Request):
    token = request.cookies.get("access_token")
    if token:
        return templates_diary.TemplateResponse(name="writeDiary.html", request=request)
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)

@router.post("/diary/write", status_code=status.HTTP_204_NO_CONTENT) # 다이어리 작성
async def writediarys(diaryreply : CreateDiarySchema, db : Session=Depends(get_db)):
    reply = Diaryreply(diaryreply)
    CreateDiary(db=db, diaryreply=diaryreply,reply=reply)

@router.get("/diary/calendar", response_class=HTMLResponse) # 다이어리 캘린더
async def diaryclosehtml(request : Request):
    token = request.cookies.get("access_token")
    if token:
        return templates_diary.TemplateResponse(name="diaryCalendar.html", request=request)
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)

@router.get("/diary/close", response_class=HTMLResponse) # 앱 종료
async def diaryclosehtml(request : Request):
    token = request.cookies.get("access_token")
    if token:
        return templates_diary.TemplateResponse(name="closeApp.html", request=request)
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)
    

# @router.get("/diary/reply", response_class=HTMLResponse) # 다이어리 답장 페이지
# async def diaryreplyhtml(request : Request):
#     token = request.cookies.get("access_token")
#     if token:
#         return templates_diary.TemplateResponse(name="reply.html", request=request)
#     else:
#         return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)
    
# @router.get("/diary/reply", status_code=status.HTTP_204_NO_CONTENT) # 다이어리 답장
# async def diary_reply(diaryreply: CreateDiarySchema, request: Request):
#     return templates_diary.TemplateResponse(name="reply.html", context={"request": request, "content": diaryreply.content, "reply": diaryreply.response})

@router.get("/diary/reply", status_code=status.HTTP_204_NO_CONTENT)
async def diary_reply(diaryreply : CreateDiarySchema, request: Request ):
    reply = Diaryreply(diaryreply)
    return templates_diary.TemplateResponse(name="reply.html",context={"request": request, "content": diaryreply.content, "reply": diaryreply.response})
    
# @router.get("diary/detail/{id}", response_class=HTMLResponse) # 일기 다시보기
# async def diarydetailhtml(request:Request,id:int,db:Session=Depends(get_db)):
#     diary=getdiarydetail(db,id=id)

DiaryRouter = router