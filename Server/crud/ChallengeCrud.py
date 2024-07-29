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

def saveImgFile(imgFile: UploadFile) -> str:
    STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "Web" / "static" / "img" / "ChallengeImg"
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    
    if imgFile is None:
        raise ValueError("No file provided.")
    
    imgFile.file.seek(0, os.SEEK_END)  # Move the cursor to the end of the file
    file_size = imgFile.file.tell()  # Get the cursor position, which is the file size
    imgFile.file.seek(0)  # Reset the cursor to the beginning of the file

    if file_size == 0:
        raise ValueError(f"File {imgFile.filename} is empty.")
    
    uploadTime = datetime.now().strftime("%Y%m%d%H%M%S")
    fileName = f"{uploadTime}_{imgFile.filename}"
    fileDir = STATIC_DIR / fileName  # Use Path object for file directory
    
    with open(fileDir, "wb") as fileObject:
        shutil.copyfileobj(imgFile.file, fileObject)
    
    return str(fileDir.relative_to(STATIC_DIR))  # Return relative path as string




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

