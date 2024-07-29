from Server.config.database import Base
from .DiaryModel import UserDiary
from .TodoListModel import TodoList
from .UserModel import UserInfo, UserChallenge
from .ChallengeModel import Challenge

metadata = Base.metadata