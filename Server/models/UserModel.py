from sqlalchemy import *
from sqlalchemy.orm import relationship
from Server.config.database import Base
from datetime import datetime, timezone
from enum import Enum as PythonEnum
# 아래는 모델 등록을 위한 import 이후 사용하진 않음
from .ChallengeModel import Challenge
from .ProofShotModel import ProofShot


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
    challenges = relationship('UserChallenge', back_populates='user')
    proofShots = relationship('UserProofShot', back_populates='user')

class UserChallenge(Base):
    __tablename__ = "userChallenge"

    user_id = Column(Integer, ForeignKey('userinfo.id'), primary_key=True)
    challenge_id = Column(Integer, ForeignKey(
        'challenge.id'), primary_key=True)
    joined_at = Column(DateTime, default=datetime.now(tz=timezone.utc))

    user = relationship("UserInfo", back_populates="challenges")
    challenge = relationship("Challenge", back_populates="participants")


class UserProofShot(Base):
    __tablename__ = "userProofShot"

    user_id = Column(Integer, ForeignKey('userinfo.id'), primary_key=True)
    photo_id = Column(String, ForeignKey('proofShot.id'), primary_key=True)

    user = relationship("UserInfo", back_populates="proofShots")
    proofShot = relationship(
        "ProofShot", back_populates="participants")  # 이 부분때문에 모델 수정 요망
