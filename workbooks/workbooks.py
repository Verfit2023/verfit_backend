from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
import workbooks.database as database
from workbooks.models import Workbook
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Optional
import PyPDF2

load_dotenv()

router = APIRouter(
    prefix="/workbooks",
)

# 문제집 검색
@router.get("/search", tags=['workbooks'])
def search_workbooks(search: str):
    workbooks = database.search_workbooks(search)
    if workbooks:
        return workbooks
    else:
        return {"message": "Workbook not found"}
