from fastapi import APIRouter, Depends, Request, status, HTTPException, Form, security, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from Server.config.database import get_db
from Server.schemas import ChallengeSchema
from Server.crud.AuthCrud import signup, getUser, verifyPW, getUserInfo
from Server.crud.ChallengeCrud import getChallengeListAll, saveImgFile, postNewChallenge
from Server.crud.TokenForAuth import getCurrentUser, createAccessToken, verityAccessToken
from Server.models.UserModel import UserInfo
import os
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()


base_path = Path(__file__).resolve().parent.parent.parent

template_dir = base_path / "Web" / "templates" / "ChallengePage"
templates = Jinja2Templates(directory=template_dir)


@router.get("/challenge/all", response_class=HTMLResponse)
async def getChallengeList(request : Request, db : Session=Depends(get_db)):
    challengeListAll = getChallengeListAll(db) 
    return templates.TemplateResponse(name="ChallengeList.html", context={"request" : request, "challengeList" : challengeListAll})

@router.post("/challenge/all", status_code=status.HTTP_204_NO_CONTENT, response_class=HTMLResponse)
async def postChallenge(request : Request,
                        challenge : ChallengeSchema.ChallengeCreate,
                        challengeThumbnail1 : UploadFile = File(...),
                        challengeThumbnail2 : UploadFile = File(None),
                        challengeThumbnail3 : UploadFile = File(None),
                        db : Session=Depends(get_db)
                        ):

    postNewChallenge(db, challenge, challengeThumbnail1, challengeThumbnail2, challengeThumbnail3)
    challengeListAll = getChallengeListAll(db) 
    return templates.TemplateResponse(name="ChallengeList.html", context={"request" : request, "challengeList" : challengeListAll})


ChallengeRouter = router