from sqlalchemy.orm import Session
from datetime import datetime
from Server.models import UserModel, ChallengeModel
from Server.schemas import ChallengeSchema
from passlib.context import CryptContext
from fastapi import security, Depends, HTTPException, UploadFile, File
from jose import JWTError, jwt
import shutil
from pathlib import Path
import os

def getChallengeListAll(db : Session):
    challengeList = db.query(ChallengeModel.Challenge).order_by(ChallengeModel.Challenge.created_at.desc()).all()
    return challengeList

def saveImgFile(imgFile : UploadFile) -> str:
    STATIC_DIR = "Server/img/challengeImg/"
    Path(STATIC_DIR).mkdir(parents=True, exist_ok=True)
    uploadTime = datetime.now().strftime("%Y%m%d%H%M%S")
    fileName = f"{uploadTime}_{imgFile.filename}"
    fileDir = os.path.join(STATIC_DIR, fileName)
    with open(fileDir, "wb") as fileObject:
        shutil.copyfileobj(imgFile.file, fileObject)
    return fileDir

def postNewChallenge(db : Session, 
                     challenge : ChallengeSchema.ChallengeCreate,
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

