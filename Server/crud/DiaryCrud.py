# from sqlalchemy.orm import Session
# from datetime import datetime
# from Server.models.DiaryModel import *
# from Server.schemas.DiarySchema import *

# def CreateDiary(db: Session, diary: CreateDiarySchema):
#     dbdiary = UserDiary(content = diary.content,
#                       date = datetime.now(),
#                       response=diary.response,
#                       todo=diary.todo
#                       )
#     db.add(dbdiary)
#     db.commit()
