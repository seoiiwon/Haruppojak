from sqlalchemy import *
from sqlalchemy.orm import relationship
from Server.config.database import Base
from datetime import datetime

class UserDiary(Base):

    __tablename__= "userdiary"

    id = Column(Integer,primary_key=True)

    Date = Column(DateTime, nullable=False)
    Diarycontent = Column(Text,nullable=False)
    # Response = Column(Text,nullable=False)
    # Diarytodo = Column(String, nullable=True)
    
    # Diaryuserid = Column(Integer, ForeignKey('userinfo.id'))
    # Diaryuser =  relationship("UserInfo", back_populates="Diary")