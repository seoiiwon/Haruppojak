from sqlalchemy.orm import Session
from datetime import datetime
from Server.models.DiaryModel import UserDiary
from Server.schemas.DiarySchema import CreateDiarySchema
from sqlalchemy import desc
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"

# 다이어리 답장
def Diaryreply(diarycontent: CreateDiarySchema):

    messages =[{
    "role" : "system",
    "content" : "너는 매우 유능한 심리상담가야. 사용자의 말에 반응 해줘. 사용자의 언어에 맞춰 대답해줘. 친근한 말로 사용자의 일기에 공감하고 위로의 말을 건네줘. 때론 사용자의 고민에 해결책을 제시해줘. 그리고 항상 마무리는 사용자의 상황에 알맞은 명언 한마디씩 제시해줬으면 좋겠어. 귀여운 이모지도 같이 대답해줘.대답은 항상 500자 이상으로 대답해줘."
    }, {
    "role" : "user",
    "content" : diarycontent.content
    }]
    
    response = openai.chat.completions.create(model=model, messages=messages)
    reply = response.choices[0].message.content
    return reply

# 다이어리 생성
def CreateDiary(db: Session, diary: CreateDiarySchema, reply:str,  diaryuserid: int):
    dbdiary = UserDiary(
        Diaryuserid=diaryuserid,
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

# 일기 다시보기
# def getdiarydetail(db: Session, diary: UserDiary):
#     db

def getdiarydetail(db:Session, diaryid:int, targetdate:int):
    diary = db.query(UserDiary).filter(
            UserDiary.Diaryuserid == diaryid,
            UserDiary.Date == targetdate).first()
    return diary


# 답장 다시보기
# def getdiaryresponsedetail