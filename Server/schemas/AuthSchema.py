from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum
from fastapi import HTTPException, status

class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    READER = "reader"

class UserInfoSchema(BaseModel):
    id : Optional[int] = None
    userID: str
    userPassword: str
    userName: str
    userBirth: int
    userEmail: EmailStr
    userGender: int
    userPpojakCoin: Optional[int] = Field(0)
    userProfileName: str
    userProfileComment: Optional[str] = Field("")
    created_at: Optional[datetime] = None 
    role: Optional[UserRole] = Field(UserRole.READER)
    follower: Optional[int] = Field(0)
    following: Optional[int] = Field(0)

    @field_validator('userID', 'userPassword', 'userName', 'userEmail')
    def check_empty_str_fields(cls, value):
        if not value or str(value).isspace():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="필수 항목을 입력하세요.")
        return value

    @field_validator('userBirth', 'userGender')
    def check_empty_int_fields(cls, value):
        if value is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="필수 항목을 입력하세요.")
        return value

    @field_validator('userPassword')
    def checkPassword(cls, value):
        if len(value) < 8 or not any(str(char).isdigit() for char in value) or not any(str(char).isalpha() for char in value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="문자와 숫자를 포함한 8자리 이상의 비밀번호를 입력해주세요.")
        return value

    @field_validator('userBirth')
    def validate_birth_year(cls, value):
        monthDict = {"31month": [1, 3, 5, 7, 8, 10, 12], "30month": [4, 6, 9, 11], "28month": [2]}
        year = value // 10000
        month = (value % 10000) // 100
        day = value % 100

        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            leap = True
        else:
            leap = False

        if month < 1 or month > 12:
            raise ValueError('Invalid month')

        if (month in monthDict["31month"] and 1 <= day <= 31) or \
           (month in monthDict["30month"] and 1 <= day <= 30) or \
           (month == 2 and ((leap and 1 <= day <= 29) or (not leap and 1 <= day <= 28))):
            return value
        else:
            raise ValueError('Invalid birth')

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    userID : Optional[str] = None
