from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.config.database import get_db
from Server.schemas.AuthSchema import UserInfoSchema
from Server.crud.AuthCrud import signup
from Server.models.UserModel import UserInfo
import os

router = APIRouter()

template_dir = os.path.join(os.path.dirname(__file__), "../../Web/templates/AuthPage")
templates = Jinja2Templates(directory=template_dir)

# GET api

@router.get("/", response_class=HTMLResponse)
async def getLoginMenuHaruPpojak(request: Request):
    return templates.TemplateResponse(name="HaruPpojakLoginMenu.html", request=request)

@router.get("/auth/signin", response_class=HTMLResponse)
async def getSignInPage(request : Request):
    return templates.TemplateResponse(name="HaruPpojakSignIn.html", request=request)

@router.get("/auth/signup", response_class=HTMLResponse)
async def getSignUpPage(request : Request):
    return templates.TemplateResponse(name="HaruPpojakSignUp.html", request=request)

@router.get("/HP/intro", response_class=HTMLResponse)
async def getIntroPage(request : Request):
    return templates.TemplateResponse(name="HaruPpojakIntroPage.html", request=request)

@router.get("/HP/Cam", response_class=HTMLResponse)
async def getUserCam(request : Request):
    return templates.TemplateResponse(name="HaruPpojakCamera.html", request=request)

@router.post("/auth/signup", status_code=status.HTTP_204_NO_CONTENT)
async def postUserSignUp(newUserInfo : UserInfoSchema, db : Session=Depends(get_db)):
    userData = db.query(UserInfo).filter(UserInfo.userID == newUserInfo.userID).first()
    if userData:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
    signup(db=db, user=newUserInfo)
    return userData
    


# @app.post("/signup", response_model=UserInfoSchema)
# def create_user(user: UserInfoSchema, db: Session = Depends(get_db)):
#     db_user = db.query(UserInfo).filter(UserInfo.userID == user.userID).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="UserID already registered")

#     return db_user


auth_router = router
