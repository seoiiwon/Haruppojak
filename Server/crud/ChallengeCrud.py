from sqlalchemy.orm import Session
from datetime import datetime, timezone
from Server.models import ChallengeModel, UserChallenge
from Server.schemas import ChallengeSchema, AuthSchema
from fastapi import HTTPException, UploadFile
import shutil
from pathlib import Path
import os
from typing import List

def getChallengeListAll(db : Session):
    challengeList = db.query(ChallengeModel.Challenge).order_by(ChallengeModel.Challenge.created_at.desc()).all()
    return challengeList

def saveImgFile(imgFile: UploadFile) -> str: # 이 부분 수정 해야할듯 js에서 파일 열고 파일 선택하면 파일 위치 가져오도록 해야할듯... 아닌가 라우터 수정해야하나
    STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "Web" / "static" / "img" / "ChallengeImg"
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    
    if imgFile is None:
        raise ValueError("No file provided.")
    
    imgFile.file.seek(0, os.SEEK_END) 
    file_size = imgFile.file.tell() 
    imgFile.file.seek(0)

    if file_size == 0:
        raise ValueError(f"File {imgFile.filename} is empty.")
    
    uploadTime = datetime.now().strftime("%Y%m%d%H%M%S")
    fileName = f"{uploadTime}_{imgFile.filename}"
    fileDir = STATIC_DIR / fileName 
    
    with open(fileDir, "wb") as fileObject:
        shutil.copyfileobj(imgFile.file, fileObject)
    
    return str(fileDir.relative_to(STATIC_DIR)) 


def postNewChallenge(db : Session, 
                     challenge : ChallengeSchema.ChallengeCreateSchema,
                     challengeThumbnail1 : UploadFile,
                     challengeThumbnail2 : UploadFile = None,
                     challengeThumbnail3 : UploadFile = None) -> ChallengeModel.Challenge:
    imgFileLocation1 = saveImgFile(challengeThumbnail1)
    imgFileLocation2 = saveImgFile(challengeThumbnail2) if challengeThumbnail2 else None
    imgFileLocation3 = saveImgFile(challengeThumbnail3) if challengeThumbnail3 else None


    newChallenge = ChallengeModel.Challenge(
        challengeOwner = challenge.challengeOwner,
        challengeTitle = challenge.challengeTitle,
        challengeComment = challenge.challengeComment,
        challengeReward = challenge.challengeReward,
        challengeThumbnail1 = imgFileLocation1,
        challengeThumbnail2 = imgFileLocation2,
        challengeThumbnail3 = imgFileLocation3
        )
    db.add(newChallenge)
    db.commit()
    db.refresh(newChallenge)
    return newChallenge

def joinChallenge(challenge_id: int, current_user: AuthSchema.UserInfoSchema, db: Session):
    user_challenge = db.query(UserChallenge).filter(UserChallenge.user_id == current_user.id,
                                                    UserChallenge.challenge_id == challenge_id).first()
    if user_challenge:
        raise HTTPException(status_code=400, detail="참여중인 챌린지입니다.")

    newUserChallenge = UserChallenge(
        user_id=current_user.id,
        challenge_id=challenge_id,
        joined_at=datetime.now(tz=timezone.utc)
    )
    db.add(newUserChallenge)
    db.commit()
    db.refresh(newUserChallenge)

    return newUserChallenge


def joinedChallengeID(user_id : int, db : Session) -> List[int]:
    user_challenge = db.query(UserChallenge).filter(UserChallenge.user_id == user_id).all()
    return [uc.challenge_id for uc in user_challenge]

def joinedChallenge(challenge_id_list: List[int], db: Session):
    challenges = db.query(ChallengeModel.Challenge).filter(ChallengeModel.Challenge.id.in_(challenge_id_list)).all()
    return challenges

