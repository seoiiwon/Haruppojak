from fastapi import APIRouter, Depends, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.config.database import get_db
import os

router = APIRouter()

template_dir = os.path.join(os.path.dirname(__file__), "../../Web/templates/AuthPage")
templates = Jinja2Templates(directory=template_dir)

@router.get("/", response_class=HTMLResponse)
async def getLoginMenuHaruPpojak(request: Request):
    return templates.TemplateResponse(name="HaruPpojakLoginMenu.html", request=request)
    # return templates.TemplateResponse("HaruPpojakLoginMenu.html", {"request" : request})

@router.get("/auth/signin", response_class=HTMLResponse)
async def getSignInPage(request : Request):
    return templates.TemplateResponse("HaruPpojakSignIn.html", {"request" : request})

@router.get("/auth/signup", response_class=HTMLResponse)
async def getSignUpPage(request : Request):
    return templates.TemplateResponse("HaruPpojakSignUp.html", {"request" : request})

@router.get("/HaruPpojak/intro", response_class=HTMLResponse)
async def getIntroPage(request : Request):
    return templates.TemplateResponse("HaruPpojakIntroPage.html", {"request" : request})

@router.get("/HaruPpojak/Cam", response_class=HTMLResponse)
async def getUserCam(request : Request):
    return templates.TemplateResponse("HaruPpojakCamera.html", {"request" : request})

auth_router = router
