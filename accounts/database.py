from pymongo import MongoClient
from workbooks.models import Workbook  # Workbook 모델 임포트
from typing import Optional

MONGODB_URL = "mongodb://localhost:27017"
client = MongoClient(MONGODB_URL)
db = client.Prosumer  # 데이터베이스 이름 설정

# 사용자 정보 조회
def get_current_user(username: str):
    user = db.users.find_one({"username": username})
    if user:
        return user
    else:
        return None