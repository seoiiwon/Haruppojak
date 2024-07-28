from config.database import get_db, SessionLocal
from models.DiaryModel import UserDiary
from datetime import datetime
 
db = SessionLocal()

diary = UserDiary(
    Date = datetime.now(),
    Diarycontent = "kjdkdksksfksfksflkslsf",
    Response = "dlksjlkdsjfsk",
    Diarytodo = "sdhfjsahflkdj"
)

db.add(diary)
db.commit()

# 함수 이름 써서 db 실행 되는지 확인