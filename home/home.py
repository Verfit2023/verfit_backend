from accounts.database import get_current_user
from fastapi import APIRouter, HTTPException, UploadFile, Depends, HTTPException, status
from pydantic import BaseModel
import workbooks.database as database
from workbooks.models import Workbook
from accounts.models import Users
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Optional
import PyPDF2
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(
    prefix="/home",
)

@router.get("/current-user", tags=['home'])
def current_user(current_user: Users = Depends(get_current_user)):
    return {"username": current_user.username}


# 화면 띄우기(문제집 조회)
@router.get("", tags=['home'])
def get_workbooks(limit: int):
    workbooks = database.get_workbooks(limit)
    if workbooks:
        return workbooks
    else:
        return {"message": "Workbook not found"}

# 문제집 검색
@router.get("/search", tags=['home'])
def search_workbooks(search: str):
    workbooks = database.search_workbooks(search)
    if workbooks:
        return workbooks
    else:
        return {"message": "Workbook not found"}

# 문제집 필터
@router.get("/search/{params}", tags=['home'])
def filter_workbooks(Subject: Optional[str] = None, Type: Optional[int] = None, Date: Optional[str] = None):
    workbooks = database.filter_workbooks(Subject, Type, Date)
    if workbooks:
        return workbooks
    else:
        return {"message": "Workbook not found"}

'''
@router.get("", tags=['home'])
def get_workbook(workbook_id: int):

    workbook = database.get_workbook(workbook_id)
    if workbook:
        return workbook
    else:
        return {"message": "Workbook not found"}
'''