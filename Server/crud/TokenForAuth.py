from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request, security
from sqlalchemy.orm import Session
from Server.schemas.AuthSchema import TokenData
from Server.crud.AuthCrud import getUser
from Server.config.database import get_db
import os
from dotenv import load_dotenv
from typing import Union, Optional

load_dotenv()

# 환경 변수에서 시크릿 키 및 알고리즘 가져오기
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class OAuth2PasswordBearerWithCookie(security.OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str):
        super().__init__(tokenUrl=tokenUrl)  # 부모 클래스 초기화
        
    async def __call__(self, request: Request) -> str:
        authorization: str = request.cookies.get("access_token")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return authorization

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/signin")

def createAccessToken(data: dict, expiresDelta: Optional[Union[timedelta, None]] = None):
    toEncode = data.copy()
    if expiresDelta:
        expire = datetime.now(tz=timezone.utc) + expiresDelta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})
    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT

def verifyAccessToken(token: str, credentialsException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userID: str = payload.get("sub")
        if userID is None:
            raise credentialsException
        tokenData = TokenData(userID=userID)
    except JWTError:
        raise credentialsException
    return tokenData

# 사용자 정보를 가져오는 함수
def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    tokenData = verifyAccessToken(token, credentialsException)
    user = getUser(db, tokenData.userID)
    if user is None:
        raise credentialsException
    return user
