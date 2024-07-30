from sqlalchemy.orm import Session
from datetime import datetime
from Server.models.DiaryModel import UserDiary
from Server.schemas.DiarySchema import CreateDiarySchema

def CreateDiary(db: Session, diary: CreateDiarySchema):
    dbdiary = UserDiary(
        Diarycontent=diary.content,
        Date=datetime.now(),
        Response=diary.response,
        Diarytodo=diary.todo
    )
    db.add(dbdiary)
    db.commit()

def deleteDiary(db: Session, diary: UserDiary):
    db.delete(diary)
    db.commit()
