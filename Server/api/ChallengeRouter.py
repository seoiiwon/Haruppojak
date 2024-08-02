from fastapi import APIRouter, Depends, Request, status, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Server.config.database import get_db
from Server.schemas import ChallengeSchema, AuthSchema
from Server.crud.ChallengeCrud import getChallengeListAll, postNewChallenge, joinChallenge
from Server.crud.TokenForAuth import getCurrentUser
from pathlib import Path

router = APIRouter()
ChallengeRouter = router

base_path = Path(__file__).resolve().parent.parent.parent
template_dir = base_path / "Web" / "templates" / "ChallengePage"
templates = Jinja2Templates(directory=template_dir)

# GET

@router.get("/challenge/all", response_class=HTMLResponse) # 전체 챌린지 페이지
async def getChallengeList(request : Request, db : Session=Depends(get_db)):
    challengeListAll = getChallengeListAll(db) 
    return templates.TemplateResponse(name="ChallengeList.html", context={"request" : request, "challengeList" : challengeListAll})


# POST 

@router.post("/challenge/all", status_code=status.HTTP_204_NO_CONTENT, response_class=HTMLResponse) # 챌린지 추가하는 요청
async def postChallenge(request : Request,
                        challenge : ChallengeSchema.ChallengeCreateSchema,
                        challengeThumbnail1 : UploadFile = File(...),
                        challengeThumbnail2 : UploadFile = File(None),
                        challengeThumbnail3 : UploadFile = File(None),
                        db : Session=Depends(get_db)):
    postNewChallenge(db, challenge, challengeThumbnail1, challengeThumbnail2, challengeThumbnail3)
    challengeListAll = getChallengeListAll(db) 
    return templates.TemplateResponse(name="ChallengeList.html", context={"request" : request, "challengeList" : challengeListAll})


@router.post("/challenge/join", status_code=status.HTTP_204_NO_CONTENT) # 챌린지 참여 요청
async def joinNewChallenge(challenge_request: ChallengeSchema.ChallengeJoinRequest,
                           user: AuthSchema.UserInfoSchema = Depends(getCurrentUser),
                           db: Session = Depends(get_db)):
    joinChallenge(challenge_id=challenge_request.challenge_id, current_user=user, db=db)