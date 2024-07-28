from sqlalchemy import *
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime
from enum import Enum as PythonEnum

class UserRole(str, PythonEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    READER = "reader"

class UserInfo(Base):
    __tablename__ = "userinfo"

    id = Column(Integer, primary_key=True)

    userID = Column(String, nullable=False, unique=True)
    userPassword = Column(String, nullable=False)

    userName = Column(String(25), nullable=False, unique=True)
    userBirth = Column(Integer, nullable=False)
    userEmail = Column(String(255), nullable=False, unique=True)
    userGender = Column(Integer, nullable=False)

    userPpojakCoin = Column(Integer, nullable=False, default=0)
    userProfileName = Column(String, nullable=False)
    userProfileComment = Column(String, nullable=True, default="")

    created_at = Column(DateTime, default=datetime.now)

    role = Column(Enum(UserRole), default=UserRole.READER)

    follower = Column(Integer, default=0)
    following = Column(Integer, default=0)