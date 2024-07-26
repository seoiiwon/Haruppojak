from sqlalchemy.orm import Session
from datetime import datetime
from Server.models import UserModel
from Server.schemas import AuthSchema
from passlib.context import CryptContext

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def signup(db : Session, user : AuthSchema.UserInfoSchema):
    user = UserModel.UserInfo(userID = user.userID,
                              userPassword = passwordContext.hash(user.userPassword),
                              userName = user.userName,
                              userBirth = user.userBirth,
                              userEmail = user.userEmail,
                              userGender = user.userGender,
                              userPpojakCoin = user.userPpojakCoin,
                              userProfileName = user.userName,
                              userProfileComment = user.userProfileName,
                              created_at = datetime.now(),
                              role = user.role,
                              follower = user.follower,
                              following = user.following)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def getUser(db : Session, ID : str):
    return db.query(UserModel.UserInfo).filter(UserModel.UserInfo.userID == ID).first

def verifyPW(plainPW, hashedPW):
    return passwordContext.verify(plainPW, hashedPW)