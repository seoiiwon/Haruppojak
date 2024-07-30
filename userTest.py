from Server.config.database import SessionLocal, engine
from Server.models.UserModel import Base, UserInfo
from sqlalchemy.orm import sessionmaker
from Server.models.DiaryModel import UserDiary
from datetime import datetime
from Server.crud.DiaryCrud import *

db = SessionLocal()

diary_data = CreateDiarySchema(
    content="김뽀짝의 일기장",
    response="뽀짝아 안녕",
    todo="운동하기"
)

CreateDiary(db, diary_data)

db = SessionLocal()

diary_to_delete = db.query(UserDiary).filter(UserDiary.id == 5).first()

if diary_to_delete:
    deleteDiary(db, diary_to_delete)
else:
    print("삭제할 일기 항목이 없습니다.")

# 세션 종료
db.close()