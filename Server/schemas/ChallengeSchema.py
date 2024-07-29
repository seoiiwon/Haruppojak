from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChallengeBase(BaseModel):
    challengeOwner: str
    challengeTitle: str
    challengeComment: str
    challengeReward: int
    challengeThumbnail1: str
    challengeThumbnail2: Optional[str] = None
    challengeThumbnail3: Optional[str] = None

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeRead(ChallengeBase):
    id: int
    challenger: int
    created_at: datetime

    class Config:
        orm_mode = True
