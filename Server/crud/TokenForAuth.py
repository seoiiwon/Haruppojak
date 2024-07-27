from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, security
from sqlalchemy.orm import Session
from Server.schemas.AuthSchema import TokenData
from Server.crud.AuthCrud import getUser
from Server.config.database import get_db
import os
from dotenv import load_dotenv
from typing import Union, Optional

load_dotenv()

# 이 시크릿키 안 보이게 해야하는데 어카지...
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# function for JWT
from datetime import timedelta

oauth2Scheme = security.OAuth2PasswordBearer(tokenUrl='/auth/signin')

# def createAccessToken(data : dict, expiresDelta : timedelta | None = None): -> 이 형식은 파이썬 3.10 이상에서 유효함
def createAccessToken(data : dict, expiresDelta : Optional[Union[timedelta, None]] = None):
    toEncode = data.copy()
    if expiresDelta:
        expire = datetime.now(tz=timezone.utc) + expiresDelta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    toEncode.update({"exp" : expire})
    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT

def verityAccessToken(token : str, credentialsException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
            raise credentialsException
        tokenData = TokenData(username=username)
    except JWTError:
        raise credentialsException
    return tokenData

def getCurrentUser(token : str=Depends(oauth2Scheme), db : Session=Depends(get_db)):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"}
    )
    tokenData = verityAccessToken(token, credentialsException)
    user = getUser(db, tokenData.userID)
    if user is None:
        raise credentialsException
    return user

