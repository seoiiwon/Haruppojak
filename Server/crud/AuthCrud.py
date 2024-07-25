from sqlalchemy.orm import Session
from datetime import datetime
from Server.models import UserModel
from Server.schemas import AuthSchema


def signup(db : Session, user : AuthSchema.UserInfoSchema):
    user = UserModel.UserInfo(userID = user.userID,
                              userPassword = user.userPassword,
                              userName = user.userName,
                              userBirth = user.userBirth,
                              userEmail = user.userEmail,
                              userGender = user.userGender,
                              userPpojakCoin = 0,
                              userProfileName = user.userName,
                              userProfileComment = "",
                              created_at = datetime.now(),
                              role = user.role,
                              follower = 0,
                              following = 0)
    db.add(user)
    db.commit()
    # db.refresh(user)
