from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.crud.DiaryCrud import *
from Server.schemas.DiarySchema import *
from Server.schemas import AuthSchema
from sqlalchemy import desc
from datetime import datetime, timedelta
from Server.config.database import get_db
from Server.crud.TokenForAuth import *
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

# @router.post("/diary/write", status_code=status.HTTP_204_NO_CONTENT) # 다이어리 작성
# async def writediarys(diaryreply : CreateDiarySchema, db : Session=Depends(get_db)):
#     reply = Diaryreply(diaryreply)
#     CreateDiary(db=db, diaryreply=diaryreply,reply=reply)

@router.post("/diary/write", status_code=status.HTTP_201_CREATED) # 다이어리 작성 테스트중
async def writediarys(writediary: CreateDiarySchema, request : Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    user = getCurrentUser(token,db)
    userid = user.id
    writediary.id = userid
    latest_diary = db.query(UserDiary).filter(UserDiary.Diaryuserid == userid).order_by(desc(UserDiary.Date)).first()
    if latest_diary and latest_diary.Date > datetime.now() - timedelta(days=1):
        raise HTTPException(status_code=429, detail="하루에 한 번만 일기를 작성할 수 있습니다.")
    reply = Diaryreply(writediary)
    writediary.response = reply
    CreateDiary(db=db, diary=writediary, reply=reply, diaryuserid=userid) 

# @router.post("/diary/write", status_code=status.HTTP_201_CREATED) # 다이어리 작성 수정 후
# async def writediarys(writediary: CreateDiarySchema, db: Session = Depends(get_db)):
#     reply = Diaryreply(writediary)
#     writediary.response = reply
#     CreateDiary(db=db, writediary=writediary, reply=reply) 

@router.get("/diary/reply", response_class=HTMLResponse)  # 다이어리 답장 보기
async def diary_reply(request: Request, currentUser: AuthSchema.UserInfoSchema = Depends(getCurrentUser), db: Session = Depends(get_db)):
    
    userid = currentUser.id
    
    # 사용자별 최신 일기 조회
    latest_diary = db.query(UserDiary).filter(UserDiary.Diaryuserid == userid).order_by(desc(UserDiary.Date)).first()

    if latest_diary is None:
        # 일기가 없는 경우
        return templates_diary.TemplateResponse(name="reply.html", context={"request": request, "reply": "최근 일기가 없습니다."})
    
    # 일기가 있는 경우
    return templates_diary.TemplateResponse(name="reply.html", context={"request": request, "reply": latest_diary.Response})

# @router.get("/diary/reply", response_class=HTMLResponse) # 다이어리 답장 보기 test
# async def diary_reply(request: Request, currentUser: AuthSchema.UserInfoSchema = Depends(getCurrentUser),db: Session = Depends(get_db)):
#     # token = request.cookies.get("access_token")
#     # user = getCurrentUser(token,db)
#     userid = currentUser.id
#     latest_diary = db.query(UserDiary).filter(UserDiary.Diaryuserid == userid).order_by(desc(UserDiary.Date)).first()
#     # diaryreply = CreateDiarySchema(content=latest_diary.Diarycontent, response=latest_diary.Response, todo=latest_diary.Diarytodo, id=latest_diary.Diaryuserid)
#     return templates_diary.TemplateResponse(name="reply.html",context= {"request": request,"reply": latest_diary.Response})

# @router.get("/diary/reply", status_code=status.HTTP_200_OK) # 다이어리 답장 수정중.
# async def diary_reply(diaryreply : CreateDiarySchema, request: Request ):
#     reply = Diaryreply(diaryreply)
#     return templates_diary.TemplateResponse(name="reply.html",context={"request": request, "content": diaryreply.content, "reply": reply})

@router.get("/diary/calendar", response_class=HTMLResponse) # 다이어리 캘린더
async def diarycalendarhtml(request : Request):
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
    
# @router.get("/diary/reply", status_code=status.HTTP_200_OK) # 다이어리 답장 수정
# async def diary_reply(content: str, response: str, request: Request):
#     diaryreply = {"content": content, "response": response}
#     reply = Diaryreply(diaryreply)  # Diaryreply 함수로 가정
#     return templates_diary.TemplateResponse(name="reply.html", context={"request": request, "content": content, "reply": response})

# @router.get("diary/detail/{id}", response_class=HTMLResponse) # 일기 다시보기
# async def diarydetailhtml(request:Request,id:int,db:Session=Depends(get_db)):
#     diary=getdiarydetail(db,id=id)

# @router.get("diary/responsedetail/{id}", response_class=HTMLResponse) # 답장 다시보기
# async def diarydetailresponse(request:Request, id:int,db:Session=Depends(get_db)):
#     diaryresponse=getdiaryresponsedetail(db,id=id)

DiaryRouter = router

