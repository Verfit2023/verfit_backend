from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
import routers.database as database
from routers.model import Workbook
from pymongo import MongoClient
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

router = APIRouter(
    prefix="/home",
)

# 화면 띄우기(문제집 조회)
@router.get("", tags=['home'])
def get_workbooks(limit: int = 10):
    workbooks = database.get_workbooks(limit)
    if not workbooks:
        raise HTTPException(status_code=404, detail="Workbook not found")
    return workbooks





'''
@router.get("", tags=['home'])
def get_workbook(workbook_id: int):

    workbook = database.get_workbook(workbook_id)
    if workbook:
        return workbook
    else:
        return {"message": "Workbook not found"}

'''