from pymongo import MongoClient
from workbooks.models import Workbook  # Workbook 모델 임포트
from typing import Optional

MONGODB_URL = "mongodb://localhost:27017"
client = MongoClient(MONGODB_URL)
db = client.Prosumer  # 데이터베이스 이름 설정

# 데이터베이스 워크북 생성
def create_workbook(workbook_data: Workbook):
    if db.Workbooks.find_one({"workbook_id": workbook_data.workbook_id}):
        return "Workbook already exists"
    
    db.Workbooks.insert_one(workbook_data.dict())
    return "Workbook created successfully"

# 데이터베이스 워크북 조회
def get_workbook(workbook_id: int):
    workbook = db.Workbooks.find_one({"workbook_id": workbook_id})
    if workbook:
        return Workbook(**workbook)
    else:
        return None

# 데이터베이스 워크북 수정
def update_workbook(workbook_id: int, workbook_data: Workbook):
    workbook = db.Workbooks.find_one({"workbook_id": workbook_id})
    if workbook:
        db.Workbooks.update_one({"workbook_id": workbook_id}, {"$set": workbook_data.dict()})
        return "Workbook updated successfully"
    else:
        return "Workbook not found"

# 데이터베이스 워크북 삭제
def delete_workbok(workbook_id: int):
    workbook = db.Workbooks.find_one({"workbook_id": workbook_id})
    if workbook:
        db.Workbooks.delete_one({"workbook_id": workbook_id})
        return "Workbook deleted successfully"
    else:
        return "Workbook not found"

# 데이터베이스 워크북 전체 조회 (상위 n개)
def get_workbooks(limit: int):
    workbooks = db.Workbooks.find().limit(limit)
    if workbooks:
        return [Workbook(**workbook) for workbook in workbooks]
    else:
        return None

# 데이터베이스 워크북 검색 (제목)
def search_workbooks(search: str):
    query = {"$or": [
        {"title": {"$regex": search}},
        {"subject": {"$regex": search}},
        {"description": {"$regex": search}}
    ]}
    workbooks = db.Workbooks.find(query)
    if workbooks:
        return [Workbook(**workbook) for workbook in workbooks]
    else:
        return None

# 데이터베이스 워크북 필터
def filter_workbooks(Subject, Type, Date):
    if Subject and Type and Date:
        workbooks = db.Workbooks.find({"subject": Subject, "type": int(Type), "date": Date})
    elif Subject and Type:
        workbooks = db.Workbooks.find({"subject": Subject, "type": int(Type)})
    elif Subject and Date:
        workbooks = db.Workbooks.find({"subject": Subject, "date": Date})
    elif Type and Date:
        workbooks = db.Workbooks.find({"type": int(Type), "date": Date}) 
    elif Subject:
        workbooks = db.Workbooks.find({"subject": Subject})
    elif Type:
        workbooks = db.Workbooks.find({"type": int(Type)})
    elif Date:
        workbooks = db.Workbooks.find({"date": Date})
    else:
        return None
    
    if workbooks:
        return [Workbook(**workbook) for workbook in workbooks]
    else:
        return None
