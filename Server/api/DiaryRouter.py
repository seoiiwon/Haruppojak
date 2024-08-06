from fastapi import APIRouter, Depends, Query, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.crud.DiaryCrud import *
from Server.crud.MainCrud import *
# from Server.crud.CalendarCrud import ppojakDay
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
template_calendar = os.path.join(os.path.dirname(__file__), "../../Web/templates/CalendarPage")

templates_diary = Jinja2Templates(directory=template_diary)
templates_auth = Jinja2Templates(directory=template_auth)
templates_calendar = Jinja2Templates(directory=template_calendar)

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
        currentUser = getCurrentUser(token, db)
        userid = currentUser.id
        target_date = datetime.now().strftime('%Y-%m-%d')
        usertodoall=db.query(TodoList).filter(TodoList.user_id == userid,TodoList.date.like(f'{target_date}%')).all()
        if not usertodoall:
            return templates_diary.TemplateResponse(name="writeDiary.html", context={"request": request, "usertodo":usertodoall})
        return templates_diary.TemplateResponse(name="writeDiary.html", context={"request": request})
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)

@router.post("/diary/write", status_code=status.HTTP_201_CREATED)  # 다이어리 작성
async def writediarys(writediary: CreateDiarySchema, currentUser: AuthSchema.UserInfoSchema = Depends(getCurrentUser), db: Session = Depends(get_db)):
    userid = currentUser.id
    writediary.id = userid
    target_date = datetime.now().strftime('%Y-%m-%d')
    latest_diary = db.query(UserDiary).filter(UserDiary.Diaryuserid == userid,UserDiary.Date.like(f'{target_date}%')).first()
    if latest_diary:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="뽀짝일기는 하루에 한 번만 작성할 수 있습니다. 내일 또 만나요 !")
    reply = Diaryreply(writediary)
    writediary.response = reply
    CreateDiary(db=db, diary=writediary, reply=reply, diaryuserid=userid)

@router.get("/diary/reply", response_class=HTMLResponse)  # 다이어리 답장 페이지
async def diary_reply(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token:
        currentUser = getCurrentUser(token, db)
        userid = currentUser.id
        latest_diary = db.query(UserDiary).filter(UserDiary.Diaryuserid == userid).order_by(desc(UserDiary.Date)).first()
        if latest_diary is None:
            return templates_diary.TemplateResponse(name="reply.html", context={"request": request, "reply": "최근 일기가 없습니다."})
        return templates_diary.TemplateResponse(name="reply.html", context={"request": request, "reply": latest_diary.Response})
    else:
        return templates_auth.TemplateResponse("HaruPpojakSignIn.html", {"request": request})

@router.get("/diary/calendar", response_class=HTMLResponse)
async def diary_calendar_html(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token:
        currentUser = getCurrentUser(token, db)
        userid = currentUser.id
        diaries = checkdiary(db, userid)
        diaries = [diary_to_dict(diary) for diary in diaries]  # UserDiary 객체를 사전으로 변환
        return templates_diary.TemplateResponse("diaryCalendar.html", {"request": request, "diaries": diaries})
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
            return templates_diary.TemplateResponse(name="writeDiary.html", context={"request": request})
            
        return templates_diary.TemplateResponse("calendarInnerDiary.html", {"request": request,"diary": diary})
    else:
        return templates_auth.TemplateResponse("HaruPpojakSignIn.html", {"request": request})

@router.get("/diary/close", response_class=HTMLResponse)  # 앱 종료
async def diaryclosehtml(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return templates_diary.TemplateResponse(name="closeApp.html", request=request)
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)
    
@router.get("/haru/calendar", response_class=HTMLResponse)
async def getCalendar(request : Request):
    token = request.cookies.get("access_token")
    if token:
        # ppojakDayCount = ppojakDay(currentUser = getCurrentUser(token, db), month=month, db=db)
        return templates_calendar.TemplateResponse(name="calendar.html", request=request)
    else:
        return templates_auth.TemplateResponse(name="HaruPpojakSignIn.html", request=request)    

DiaryRouter = router