from sqlalchemy import *
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class UserInfo(Base):
    __tablename__ = "userinfo"

    id = Column(Integer, primary_key=True)

    userID = Column(String, nullable=False)
    userPassword = Column(String, nullable=False)

    userName = Column(String, nullable=False)
    userBirth = Column(Date, nullable=False)  # 수정 필요
    userEmail = Column(String, nullable=False)
    userGender = Column(Integer, nullable=False)

    userPpojakCoin = Column(Integer, nullable=False)
    userProfileName = Column(String, nullable=False)
    userProfileComment = Column(String, nullable=True)

    # Follower, Following column 추가
    # Follower, Following column 추가