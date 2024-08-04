from Server.config.database import SessionLocal, engine
from Server.models.UserModel import Base, UserInfo
from sqlalchemy.orm import sessionmaker
from Server.models.DiaryModel import UserDiary
from Server.crud.TokenForAuth import *
from datetime import datetime
from Server.crud.DiaryCrud import *

db = SessionLocal()

diary_data = CreateDiarySchema(
    content="일이 내 생각대로 풀리지 않아.",
    todo="운동하기",
    response="",
    id=0
)

userid=1

reply = Diaryreply(diary_data)

diary_data.response = reply

CreateDiary(db, diary_data, reply, userid)


# def writediary():
#     userid = int(input("userid는? "))
#     latest_diary = db.query(UserDiary).filter(UserDiary.Diaryuserid == userid).order_by(desc(UserDiary.Date)).first()
#     print(f"{latest_diary.Response}")

# while 1:
#     upload_type = int(input("1 : 다이어리 작성 / 2 : 종료 "))
#     if upload_type == 1:
#         writediary()

#     if upload_type ==2:
#         print()
#         break


# db = SessionLocal()

# diary_to_delete = db.query(UserDiary).filter(UserDiary.id == 8).first()

# if diary_to_delete:
#     DeleteDiary(db, diary_to_delete)
# else:
#     print("삭제할 일기 항목이 없습니다.")

# 세션 종료
# db.close()


