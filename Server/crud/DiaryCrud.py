from sqlalchemy.orm import Session
from datetime import datetime
from Server.models.DiaryModel import UserDiary
from Server.schemas.DiarySchema import CreateDiarySchema
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"

# 다이어리 답장
def Diaryreply(diarycontent: CreateDiarySchema):
    messages = [
        {
            "role": "system",
            "content": "너는 매우 유능한 심리상담가야. 사용자의 말에 반응 해줘. 한국어로 대답부탁해."
        },
        {
            "role": "user",
            "content": diarycontent.content
        }
    ]
    
    response = openai.chat.completions.create(model=model, messages=messages)
    reply = response.choices[0].message.content
    return reply

# 다이어리 생성
def CreateDiary(db: Session, diary: CreateDiarySchema, reply:str):
    dbdiary = UserDiary(
        Diarycontent=diary.content,
        Date=datetime.now(),
        Response=reply,
        Diarytodo=diary.todo
    )
    db.add(dbdiary)
    db.commit()

# 다이어리 삭제
def DeleteDiary(db: Session, diary: UserDiary):
    db.delete(diary)
    db.commit()

