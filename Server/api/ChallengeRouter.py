from fastapi import APIRouter, Depends, Request, status, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.config.database import get_db
from Server.schemas import ChallengeSchema, AuthSchema
from Server.crud.AuthCrud import getUserInfo
from Server.crud.ChallengeCrud import getChallengeListAll, postNewChallenge, joinChallenge
from Server.crud.TokenForAuth import getCurrentUser
from pathlib import Path
from Server.models.UserModel import UserChallenge

router = APIRouter()
ChallengeRouter = router

base_path = Path(__file__).resolve().parent.parent.parent
template_dir = base_path / "Web" / "templates" / "MainPage"
templates = Jinja2Templates(directory=template_dir)

# GET


@router.get("/challenge/all", response_class=HTMLResponse)  # 전체 챌린지 페이지
async def getChallengeList(request: Request, db: Session = Depends(get_db), currentUser: AuthSchema.UserInfoSchema = Depends(getCurrentUser)):
    challengeListAll = getChallengeListAll(db)
    joinedChallenge = db.query(UserChallenge).filter(
        UserChallenge.user_id == currentUser.id).all()
    userChallengeID = [challenge.challenge_id for challenge in joinedChallenge]
    return templates.TemplateResponse(name="challengePage.html", context={"request": request, "challengeList": challengeListAll, "user": getUserInfo(currentUser), "userChallenge": userChallengeID})


# POST

# 챌린지 추가하는 요청
@router.post("/challenge/all", status_code=status.HTTP_204_NO_CONTENT, response_class=HTMLResponse)
async def postChallenge(request: Request,
                        challenge: ChallengeSchema.ChallengeCreateSchema,
                        challengeThumbnail1: UploadFile = File(...),
                        challengeThumbnail2: UploadFile = File(None),
                        challengeThumbnail3: UploadFile = File(None),
                        db: Session = Depends(get_db)):
    postNewChallenge(db, challenge, challengeThumbnail1,
                     challengeThumbnail2, challengeThumbnail3)
    challengeListAll = getChallengeListAll(db)
    return templates.TemplateResponse(name="ChallengeList.html", context={"request": request, "challengeList": challengeListAll})


# 챌린지 참여 요청
@router.post("/challenge/join", status_code=status.HTTP_204_NO_CONTENT)
async def joinNewChallenge(challenge_request: ChallengeSchema.ChallengeJoinRequest,
                           user: AuthSchema.UserInfoSchema = Depends(
                               getCurrentUser),
                           db: Session = Depends(get_db)):
    joinChallenge(challenge_id=challenge_request.challenge_id,
                  current_user=user, db=db)
