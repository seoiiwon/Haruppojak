from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChallengeSchema(BaseModel):
    id: Optional[int] = Field(None)
    challengeOwner: str
    challengeTitle: str
    challengeComment: str
    challengeReward: int
    challengeThumbnail1: str
    challengeThumbnail2: Optional[str] = None
    challengeThumbnail3: Optional[str] = None

class ChallengeCreateSchema(ChallengeSchema):
    pass

class ChallengeReadSchema(ChallengeSchema):
    id: int
    challenger: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChallengeJoinRequest(BaseModel):
    challenge_id: int

class UserChallenge(BaseModel):
    user_id : int