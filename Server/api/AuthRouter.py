from fastapi import APIRouter, Depends, Request, status, HTTPException, security, UploadFile, File
from fastapi.responses import HTMLResponse, Response, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from Server.config.database import get_db
from Server.crud.MainCrud import create_intro_todos
from Server.schemas import TodoListSchema
from Server.schemas.AuthSchema import UserInfoSchema, ProofShot
from Server.schemas.TodoListSchema import TodoCreate, TodoCreateRequest
from Server.crud.AuthCrud import signup, getUser, verifyPW, getUserInfo, postProofShot
from Server.crud.TokenForAuth import getCurrentUser, createAccessToken
from Server.models.UserModel import UserInfo
from Server.models import ProofShotModel
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from pathlib import Path
import shutil
import logging


load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()
authRouter = router

template_dir = os.path.join(os.path.dirname(
    __file__), "../../Web/templates/AuthPage")
templates = Jinja2Templates(directory=template_dir)

# GET


@router.get("/", response_class=HTMLResponse)  # 로그인 선택 페이지 (초기 화면)
async def getLoginMenuHaruPpojak(request: Request):
    return templates.TemplateResponse(name="HaruPpojakLoginMenu.html", request=request)


@router.get("/auth/signin", response_class=HTMLResponse)  # 로그인 페이지
async def getSignInPage(request: Request):
    return templates.TemplateResponse(name="HaruPpojakSignIn.html", request=request)


@router.get("/auth/signup", response_class=HTMLResponse)  # 회원가입 페이지
async def getSignUpPage(request: Request):
    return templates.TemplateResponse(name="HaruPpojakSignUp.html", request=request)


@router.get("/haru/intro", response_class=HTMLResponse)  # 초기 투두리스트 입력하는 페이지
async def getIntroPage(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return templates.TemplateResponse(name="HaruPpojakIntroPage.html", request=request)
    else:
        return templates.TemplateResponse(name="HaruPpojakSignIn.html", request=request)


@router.get("/haru/photo", response_class=HTMLResponse)  # 뽀짝 인증 사진 촬영 페이지
async def getUserCam(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return templates.TemplateResponse(name="HaruPpojakCamera.html", request=request)
    else:
        return templates.TemplateResponse(name="HaruPpojakSignIn.html", request=request)


@router.get("/haru/mypage", response_class=HTMLResponse)  # 마이페이지 페이지
async def getMypage(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token:
        currentUser = getCurrentUser(token, db)
        return templates.TemplateResponse(name="HaruPpojakMyPage.html", context={"request": request, "currentUser": getUserInfo(currentUser)})
    else:
        return templates.TemplateResponse(name="HaruPpojakSignIn.html", request=request)


# POST

@router.post("/auth/signup", status_code=status.HTTP_204_NO_CONTENT)
async def postUserSignUp(newUserInfo: UserInfoSchema, db: Session = Depends(get_db)):
    userData = db.query(UserInfo).filter(
        UserInfo.userID == newUserInfo.userID).first()
    if userData:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 사용자입니다.")
    signup(db=db, user=newUserInfo)


@router.post("/auth/signin")  # 로그인 요청
async def postUserSignIn(response: Response, loginForm: security.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = getUser(db, loginForm.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="회원가입이 필요합니다.")

    res = verifyPW(loginForm.password, user.userPassword)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="아이디나 비밀번호를 확인해주세요.")

    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    accessToken = createAccessToken(
        data={"sub": user.userID}, expiresDelta=accessTokenExpires)

    response.set_cookie(key="access_token", value=accessToken,
                        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, httponly=True)
    return {"access_token": accessToken, "token_type": "bearer"}


@router.post("/auth/photo", status_code=status.HTTP_204_NO_CONTENT)
async def postUserPhoto(db: Session = Depends(get_db), ):
    pass


# @router.post("/haru/intro", status_code=status.HTTP_204_NO_CONTENT)
# async def postFirstTodo(request: Request, todolist: TodoCreateRequest, currentUser: UserInfoSchema = Depends(getCurrentUser), db: Session = Depends(get_db)):
#     return create_intro_todos(db=db, todo_request=todolist)



@router.post("/haru/intro", status_code=status.HTTP_204_NO_CONTENT)
async def postFirstTodo(todolist: TodoCreateRequest, currentUser: UserInfoSchema = Depends(getCurrentUser), db: Session = Depends(get_db)):
    create_intro_todos(db=db, todo_request=todolist, user_id=currentUser.id)


@router.get("/haru/upload/imgFile")
async def get_upload_image(request: Request, currentUser: UserInfoSchema = Depends(getCurrentUser), db: Session = Depends(get_db)):
    user_id = currentUser.id
    date = datetime.now().strftime("%Y%m%d")
    fileName = f"{user_id}_{date}.png"
    return templates.TemplateResponse(
        name="HaruPpojakFeed.html",
        request=request,
        context={"fileName": fileName, "user_id": user_id}
    )

UPLOAD_DIR = Path('Web/static/img/ProofShot')

@router.post("/haru/upload/imgFile")
async def upload_image(image: UploadFile = File(...), currentUser :  UserInfoSchema = Depends(getCurrentUser), db: Session = Depends(get_db)):
    try:
        # 사용자 ID와 촬영 날짜를 얻기 위한 예시, 실제로는 로그인 세션 등에서 사용자 ID를 받아와야 함
        user_id = str(currentUser.id)  # 예시 사용자 ID
        now = datetime.now().strftime('%Y%m%d')
        
        user_dir = UPLOAD_DIR / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        
        file_name = f"{user_id}_{now}.png"
        file_path = user_dir / file_name
        
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(image.file, f)
        
        image_url = f"/static/img/ProofShot/{user_id}/{file_name}"
        
        return JSONResponse(content={"imageUrl": image_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")


@router.post("/haru/upload/comment")
async def uploadComment(proofshot: ProofShot, currentUser: UserInfoSchema = Depends(getCurrentUser), db: Session = Depends(get_db)):
    user_id = str(currentUser.id)  
    now = str(datetime.now().strftime('%Y%m%d'))
    proofShot = ProofShotModel.ProofShot(
        userID=currentUser.id,
        date=datetime.now(),
        photoComment=proofshot.photoComment,
        photoName=user_id + "_" + now + ".png"
    )
    db.add(proofShot)
    db.commit()



# 로그아웃 부분 수정해서 활용하도록 하죠...
# @router.get("/auth/logout")
# async def logout(response : Response, request : Request):
#     accessToken = request.cookies.get("accessToken")
#     response.delete_cookie(key="accessToken")
#     return HTTPException(status_code=status.HTTP_200_OK, detail="야호! 로그아웃 성공!")
