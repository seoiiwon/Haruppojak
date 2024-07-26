from sqlalchemy.orm import Session
from datetime import datetime
from Server.models import DiaryModel
from Server.schemas import DiarySchema

def CreateDiary(db: Session, diary: DiarySchema.CreateDiarySchema):
    diary = DiaryModel.UserDiary(content = diary.content,
                      date = datetime.now())
    db.add(diary)
    db.commit()
