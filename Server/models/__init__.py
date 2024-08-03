from Server.config.database import Base
from .DiaryModel import UserDiary
from .TodoListModel import TodoList
from .UserModel import UserInfo, UserChallenge, UserProofShot, UserRole
from .ChallengeModel import Challenge
from .ProofShotModel import ProofShot

metadata = Base.metadata