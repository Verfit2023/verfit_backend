from fastapi import APIRouter, HTTPException, UploadFile, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from accounts.schemas import Token, User, UserInDB
from dotenv import load_dotenv
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from workbooks import database

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(
    prefix="/home",
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = database.get_user_by_token(token)
    if not user:
        return None
    return user

@router.get("", tags=['home'])
def get_workbooks(limit: int, current_user: UserInDB = Depends(get_current_user)):
    workbooks = database.get_workbooks(limit)
    if workbooks:
        response = {"workbooks": workbooks}
        if current_user:
            response["usernmae"] = current_user.nickname
        return response
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