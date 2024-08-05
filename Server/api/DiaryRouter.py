from fastapi import APIRouter, Depends, Query, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.crud.DiaryCrud import *
from Server.crud.MainCrud import *
from Server.schemas.DiarySchema import *
from Server.schemas import AuthSchema
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from Server.config.database import get_db
from Server.crud.TokenForAuth import *
from utils import diary_to_dict  # utils.py에서 변환 함수 가져오기
import os

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()

template_diary = os.path.join(os.path.dirname(__file__), "../../Web/templates/DiaryPage")
template_auth = os.path.join(os.path.dirname(__file__), "../../Web/templates/AuthPage")
templates_diary = Jinja2Templates(directory=template_diary)
templates_auth = Jinja2Templates(directory=template_auth)

@router.get("/diary", response_class=HTMLResponse)  # 초기 다이어리 페이지
async def getIntroPage(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return templates_diary.TemplateResponse(name="access.html", request=request)
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)

@router.get("/diary/write", response_class=HTMLResponse)  # 다이어리 작성 페이지
async def writediaryhtml(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token:
        # currentUser = getCurrentUser(token, db)
        # userid = currentUser.id
        # target_date = datetime.strptime(date, '%Y-%m-%d').date()
        # target_date_str = target_date.strftime('%Y-%m-%d')
        # usertodo = db.query(TodoList).filter(TodoList.user_id == userid, TodoList.date.like(f'{target_date_str}%')).first()
        return templates_diary.TemplateResponse("writeDiary.html", { "request": request})
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)

@router.post("/diary/write", status_code=status.HTTP_201_CREATED)  # 다이어리 작성
async def writediarys(writediary: CreateDiarySchema, currentUser: AuthSchema.UserInfoSchema = Depends(getCurrentUser), db: Session = Depends(get_db)):
    userid = currentUser.id
    writediary.id = userid
    latest_diary = db.query(UserDiary).filter(UserDiary.Diaryuserid == userid).order_by(desc(UserDiary.Date)).first()
    if latest_diary and latest_diary.Date >= datetime.now() - timedelta(days=1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="뽀짝일기는 하루에 한 번만 작성할 수 있습니다. 내일 또 만나요 !")
    reply = Diaryreply(writediary)
    writediary.response = reply
    CreateDiary(db=db, diary=writediary, reply=reply, diaryuserid=userid)

@router.get("/diary/reply", response_class=HTMLResponse)  # 다이어리 답장 페이지
async def diary_reply(request: Request, currentUser: AuthSchema.UserInfoSchema = Depends(getCurrentUser), db: Session = Depends(get_db)):
    userid = currentUser.id
    latest_diary = db.query(UserDiary).filter(
        UserDiary.Diaryuserid == userid).order_by(desc(UserDiary.Date)).first()
    if latest_diary is None:
        return templates_diary.TemplateResponse(name="reply.html", context={"request": request, "reply": "최근 일기가 없습니다."})
    return templates_diary.TemplateResponse(name="reply.html", context={"request": request, "reply": latest_diary.Response})

@router.get("/diary/calendar", response_class=HTMLResponse)
async def diary_calendar_html(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token:
        currentUser = getCurrentUser(token, db)
        userid = currentUser.id
        diaries = checkdiary(db, userid)
        diaries = [diary_to_dict(diary) for diary in diaries]  # UserDiary 객체를 사전으로 변환
        return templates_diary.TemplateResponse("diaryCalendar.html", {"request": request, "diaries": diaries})
        if not diaries:
            raise HTTPException(status_code=404, detail="해당 날짜의 뽀짝일기를 찾을 수 없습니다.")
        
        # Convert diaries to a dictionary for easy lookup
        diary_dict = {diary.Date.strftime("%Y-%m-%d"): {"content": diary.Diarycontent} for diary in diaries}

        return templates_diary.TemplateResponse("diaryCalendar.html", {
            "request": request,
            "diaries": diary_dict
        })
    else:
        return templates_auth.TemplateResponse("HaruPpojakSignIn.html", {"request": request})

@router.get("/diary/calendar/{date}", response_class=HTMLResponse)
async def get_diary_by_date(request: Request, date: str, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token:
        currentUser = getCurrentUser(token, db)
        userid = currentUser.id
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
        target_date_str = target_date.strftime('%Y-%m-%d')

        diary = db.query(UserDiary).filter(UserDiary.Diaryuserid == userid,UserDiary.Date.like(f'{target_date_str}%')).first()

        if not diary:
            raise HTTPException(status_code=404, detail="해당 날짜의 뽀짝일기를 찾을 수 없습니다.")

        return templates_diary.TemplateResponse("calendarInnerDiary.html", { "request": request,"diary": diary, "diary_date":target_date_str})
    else:
        return templates_auth.TemplateResponse("HaruPpojakSignIn.html", {"request": request})

@router.get("/diary/close", response_class=HTMLResponse)  # 앱 종료
async def diaryclosehtml(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return templates_diary.TemplateResponse(name="closeApp.html", request=request)
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)

DiaryRouter = router