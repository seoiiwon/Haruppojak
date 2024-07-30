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

db.close()