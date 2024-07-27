from fastapi import APIRouter, Depends, Request, status, HTTPException, Form, security
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.config.database import get_db
from Server.schemas.AuthSchema import UserInfoSchema
from Server.crud.AuthCrud import signup, getUser, verifyPW, getUserInfo
from Server.crud.TokenForAuth import getCurrentUser, createAccessToken, verityAccessToken
from Server.models.UserModel import UserInfo
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

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


# post api

@router.post("/auth/signup", status_code=status.HTTP_204_NO_CONTENT)
async def postUserSignUp(newUserInfo: UserInfoSchema, db: Session = Depends(get_db)):
    userData = db.query(UserInfo).filter(UserInfo.userID == newUserInfo.userID).first()
    if userData:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 사용자입니다.")
    signup(db=db, user=newUserInfo)
    return {"detail": "회원가입 완료"}
    
@router.post("/auth/signin")
async def postUserSignIn(response : Response, loginForm : security.OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = getUser(db, loginForm.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="회원가입이 필요합니다.")
    
    res = verifyPW(loginForm.password, user.userPassword)
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="아이디나 비밀번호를 확인해주세요.")
    
    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    accessToken = createAccessToken(data={"sub" : user.userID}, expiresDelta=accessTokenExpires)

    response.set_cookie(key="accessToken", value=accessToken, expires=accessTokenExpires, httponly=True)
    return {"access_token": accessToken, "token_type": "bearer"}
    # return HTTPException(status_code=status.HTTP_200_OK, detail="로그인 성공!")

@router.get("/haru/mypage", response_class=HTMLResponse)
async def read_mypage(currentUser: UserInfoSchema = Depends(getCurrentUser)):
    return templates.TemplateResponse(name="MyPage.html", context={"currentUser" : getUserInfo(currentUser)})
    # return getUserInfo(current_user)

# 로그아웃 부분 수정해서 활용하도록 하죠...
@router.get("/auth/logout")
async def logout(response : Response, request : Request):
    accessToken = request.cookies.get("accessToken")
    response.delete_cookie(key="accessToken")
    return HTTPException(status_code=status.HTTP_200_OK, detail="야호! 로그아웃 성공!")


authRouter = router
