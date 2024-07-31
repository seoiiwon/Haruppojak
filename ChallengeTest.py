from Server.config.database import SessionLocal
from Server.models.ChallengeModel import Challenge
from Server.schemas.ChallengeSchema import ChallengeCreateSchema
from Server.crud.ChallengeCrud import saveImgFile, postNewChallenge
from fastapi import UploadFile
from io import BytesIO
import os

db = SessionLocal()

def create_upload_file_from_path(file_path: str) -> UploadFile:
    if not file_path or not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "rb") as file:
        file_content = file.read()
        if not file_content:
            raise ValueError(f"File is empty: {file_path}")
        file_like_object = BytesIO(file_content)
        file_like_object.name = os.path.basename(file_path)
        return UploadFile(file=file_like_object, filename=file_like_object.name)


test_img1_path = "/Users/seojiwon/Downloads/likelion.png"
test_img2_path = None
test_img3_path = None

if not os.path.isfile(test_img1_path):
    print(f"File path is incorrect or file does not exist: {test_img1_path}")
else:
    print(f"File path is correct: {test_img1_path}")

test_img1 = create_upload_file_from_path(test_img1_path)
test_img2 = create_upload_file_from_path(test_img2_path) if test_img2_path else None
test_img3 = create_upload_file_from_path(test_img3_path) if test_img3_path else None

imgFileLocation1 = saveImgFile(test_img1) if test_img1 else None
imgFileLocation2 = saveImgFile(test_img2) if test_img2 else None
imgFileLocation3 = saveImgFile(test_img3) if test_img3 else None

newChallenge = ChallengeCreateSchema(
    challengeOwner = "@likelion univ",
    challengeTitle = "멋쟁이사자처럼 12기 해커톤",
    challengeComment = "당신을 멋쟁이사자처럼 12기 해커톤에 초대합니다.",
    challengeReward = 300,
    challengeThumbnail1 = imgFileLocation1,
    challengeThumbnail2 = imgFileLocation2,
    challengeThumbnail3 = imgFileLocation3
)

postNewChallenge(
    db=db,
    challenge=newChallenge,
    challengeThumbnail1=test_img1,
    challengeThumbnail2=test_img2,
    challengeThumbnail3=test_img3
)


