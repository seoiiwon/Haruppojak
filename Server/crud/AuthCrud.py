from sqlalchemy.orm import Session
from datetime import datetime
from Server.models import UserModel
from Server.schemas import AuthSchema
from passlib.context import CryptContext
from fastapi import security, Depends, HTTPException
from jose import JWTError, jwt


passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def signup(db : Session, user : AuthSchema.UserInfoSchema):
    user = UserModel.UserInfo(userID = user.userID,
                              userPassword = passwordContext.hash(user.userPassword),
                              userName = user.userName,
                              userBirth = user.userBirth,
                              userEmail = user.userEmail,
                              userGender = user.userGender,
                              userPpojakCoin = user.userPpojakCoin,
                              userProfileName = user.userID,
                              userProfileComment = user.userProfileComment,
                              created_at = datetime.now(),
                              role = user.role,
                              follower = user.follower,
                              following = user.following)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def getUser(db : Session, ID : str):
    return db.query(UserModel.UserInfo).filter(UserModel.UserInfo.userID == ID).first()

def verifyPW(plainPW, hashedPW):
    return passwordContext.verify(plainPW, hashedPW)

def getUserInfo(user : AuthSchema.UserInfoSchema):
    userInfo = {
        "userID": user.userID,
        "userName": user.userName,
        "userEmail": user.userEmail,
        "userGender": user.userGender,
        "userBirth": user.userBirth,
        "userProfileName": user.userProfileName,
        "userProfileComment": user.userProfileComment,
        "created_at": user.created_at,
        "role": user.role,
        "follower": user.follower,
        "following": user.following
    }
    return userInfo