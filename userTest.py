from Server.config.database import SessionLocal, engine
from Server.models.UserModel import Base, UserInfo
from sqlalchemy.orm import sessionmaker
from Server.models.DiaryModel import UserDiary
from datetime import datetime
from Server.crud.DiaryCrud import *

db = SessionLocal()

# Initialize diary data
diary_data = CreateDiarySchema(
    content="오늘은 일기장을 새로 샀어",
    todo="운동하기",
    response=""  # Placeholder for the reply
)

# Get a reply for the diary entry
reply = Diaryreply(diary_data)

# Set the reply in diary_data's response field
diary_data.response = reply

# Save the diary entry to the database
CreateDiary(db, diary_data, reply)

# db = SessionLocal()

# diary_to_delete = db.query(UserDiary).filter(UserDiary.id == 1).first()

# if diary_to_delete:
#     DeleteDiary(db, diary_to_delete)
# else:
#     print("삭제할 일기 항목이 없습니다.")

# 세션 종료
db.close()

