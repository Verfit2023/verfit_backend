# 문제집 생성
from pydantic import BaseModel, Field
from accounts.schemas import User

from typing import List, Optional
from datetime import datetime

class Comments(BaseModel):
    content: str = Field(..., description="댓글 내용")
    writer: User = Field(..., description="작성자")
    created_at: datetime = Field(..., description="생성 날짜")

class Workbook(BaseModel):
    workbook_id: int = Field(..., description="문제집 고유 ID")
    title: str = Field(..., description="제목")
    subject: str = Field(..., description="과목")
    description: Optional[str] = Field(None, description="설명")
    created_at: datetime = Field(..., description="생성 날짜")
    rate: int = Field(..., description="좋아요 수")
    problems: List[tuple] = Field(..., description="문제집에 포함되어 있는 문제들(type, questions, answers)")
    summaries: List[str] = Field(..., description="문제집에 포함된 요약 정리본들")
    owner: User = Field(..., description="소유자")
    comments: List[Comments] = Field(..., description="댓글")
    pubpriv: int = Field(..., description="공개여부")