from pydantic import BaseModel, Field
from typing import List, Optional

class Users(BaseModel):
    useremail: str = Field(..., description="이메일")
    password: str = Field(..., description="비밀번호")
    nickname: str = Field(..., description="닉네임")
    made_workbook_id: List[int] = Field(..., description="자신이 생성한 문제집 list")
    fav_workbook_id: List[int] = Field(..., description="즐겨찾기 한 문제집 list")