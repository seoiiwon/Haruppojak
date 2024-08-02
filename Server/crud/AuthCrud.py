from sqlalchemy.orm import Session
from datetime import date, datetime
from Server.models import UserModel
from Server.schemas import AuthSchema
from passlib.context import CryptContext

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def signup(db: Session, user: AuthSchema.UserInfoSchema):
    user_model = UserModel.UserInfo(
        userID=user.userID,
        userPassword=passwordContext.hash(user.userPassword),
        userName=user.userName,
        userBirth=user.userBirth,
        userEmail=user.userEmail,
        userGender=int(user.userGender),
        userPpojakCoin=user.userPpojakCoin,
        userProfileName=user.userProfileName,
        userProfileComment=user.userProfileComment,
        created_at=user.created_at,
        role=user.role,
        follower=user.follower,
        following=user.following,
        # 이우찬 수정부분
        age_group=user.age_group
    )
    db.add(user_model)
    db.commit()


def getUser(db: Session, ID: str):
    return db.query(UserModel.UserInfo).filter(UserModel.UserInfo.userID == ID).first()


def verifyPW(plainPW, hashedPW):
    return passwordContext.verify(plainPW, hashedPW)


def getUserInfo(user: AuthSchema.UserInfoSchema):
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

# 이우찬 수정부분


def calculate_age_group(birth_year: int) -> str:
    today = date.today()
    age = today.year - birth_year
    if age < 20:
        return '10대'
    elif age < 30:
        return '20대'
    elif age < 40:
        return '30대'
    else:
        return '40대 이상'
