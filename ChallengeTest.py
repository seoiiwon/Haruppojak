from Server.config.database import SessionLocal
from Server.models.ChallengeModel import Challenge
from Server.schemas.ChallengeSchema import ChallengeCreate
from Server.crud.ChallengeCrud import saveImgFile, postNewChallenge
from fastapi import UploadFile
from io import BytesIO
from datetime import datetime
import os

# 데이터베이스 세션 생성
db = SessionLocal()

# 실제 파일 경로에서 UploadFile 객체를 생성하는 함수
def create_upload_file_from_path(file_path: str) -> UploadFile:
    with open(file_path, "rb") as file:
        file_content = file.read()
    file_like_object = BytesIO(file_content)
    file_like_object.name = os.path.basename(file_path)
    return UploadFile(file=file_like_object, filename=file_like_object.name)

test_img1_path = "/Users/seojiwon/Downloads/likelion.png"
test_img2_path = None
test_img3_path = None

try:
    test_img1 = create_upload_file_from_path(test_img1_path)
except FileNotFoundError as e:
    print(e)
    test_img1 = None

# 실제 파일 경로에서 UploadFile 객체를 생성
test_img1 = create_upload_file_from_path("/Users/seojiwon/Downloads/likelion.png")
test_img2 = create_upload_file_from_path(test_img2_path) if test_img2_path else None
test_img3 = create_upload_file_from_path(test_img3_path) if test_img3_path else None


# 이미지 파일을 서버에 저장하고 저장된 파일의 경로를 얻음
imgFileLocation1 = saveImgFile(test_img1)
imgFileLocation2 = saveImgFile(test_img2) if test_img2 else None
imgFileLocation3 = saveImgFile(test_img3) if test_img3 else None

# 챌린지 데이터 생성
newChallenge = ChallengeCreate(
    challengeOwner = "@likelion univ",
    challengeTitle = "멋쟁이사자처럼 12기 해커톤",
    challengeComment = "당신을 멋쟁이사자처럼 12기 해커톤에 초대합니다.",
    challengeReward = 300,
    challengeThumbnail1=imgFileLocation1,
    challengeThumbnail2=imgFileLocation2,
    challengeThumbnail3=imgFileLocation3
)

# 챌린지 데이터 추가 함수 호출
created_challenge = postNewChallenge(
    db=db,
    challenge=newChallenge,
    challengeThumbnail1=test_img1,
    challengeThumbnail2=test_img2,
    challengeThumbnail3=test_img3
)

# 결과 출력
print(f"Created Challenge: {created_challenge}")

# 데이터베이스 세션 종료
db.close()
