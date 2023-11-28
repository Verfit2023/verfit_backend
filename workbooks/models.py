from pydantic import BaseModel, Field

from typing import List, Optional
from datetime import datetime

# 문제집 생성
class Workbook(BaseModel):
    workbook_id: int = Field(..., description="문제집 고유 ID")
    title: str = Field(..., description="제목")
    subject: str = Field(..., description="과목")
    description: Optional[str] = Field(None, description="설명")
    created_at: datetime = Field(..., description="생성 날짜")
    rate: int = Field(..., description="좋아요 수")
    type: int = Field(..., description="문제 유형")
    questions: List[str] = Field(..., description="문제 내용")
    answers: List[str] = Field(..., description="문제의 답")
