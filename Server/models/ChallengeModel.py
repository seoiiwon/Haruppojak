from sqlalchemy import *
from sqlalchemy.orm import relationship
from Server.config.database import Base
from datetime import datetime, timezone
from .UserModel import UserChallenge
# from enum import Enum as PythonEnum

class Challenge(Base):
    __tablename__ = "challenge"

    id = Column(Integer, primary_key=True)
    challengeOwner = Column(String, nullable=False)
    challengeTitle = Column(String, nullable=False)
    challengeComment = Column(Text, nullable=False)
    challenger = Column(Integer, nullable=False, default=0)
    challengeReward = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    challengeThumbnail1 = Column(String, nullable=False)
    challengeThumbnail2 = Column(String, nullable=True)
    challengeThumbnail3 = Column(String, nullable=True)

    participants = relationship('UserChallenge', back_populates='challenge')