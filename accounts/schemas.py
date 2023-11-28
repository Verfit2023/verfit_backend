from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# User 모델
class User(BaseModel):
    username: Optional[str] = Field(default="익명이", description="User 닉네임")
    useremail: EmailStr = Field(..., description="User 고유 email")
    userpassword: str = Field(..., description="User 비밀번호")
    made_workbook_id: List[int] = Field(description="자신이 생성한 문제집 list")
    fav_workbook_id: List[int] = Field(description="즐겨찾기 한 문제집 list")
    userpassword_confirm: str = Field(alias="userpasswordConfirm")

    # 비밀번호 일치 검증 메서드 추가
    def password_match(self):
        return self.userpassword == self.userpassword_confirm

class UserInDB(User):
    hashed_password: str

# Admin 모델
class Admin(BaseModel):
    adminname: Optional[str] = Field(default="관리자", description="Admin 닉네임")
    adminemail: EmailStr = Field(..., description="Admin 고유 email")
    adminpassword: str = Field(..., description="Admin 비밀번호")
    adminpassword_confirm: str = Field(alias="adminpasswordConfirm")

    def password_match(self):
        return self.adminpassword == self.adminpassword_confirm

class AdminInDB(Admin):
    hashed_password: str

# 토큰 모델
class Token(BaseModel):
    access_token: str
    token_type: str
    email: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[str] = None

class TokenBlacklist(BaseModel):
    jti: str=Field(..., description="jti")
    exp: datetime=Field(description="datetime")