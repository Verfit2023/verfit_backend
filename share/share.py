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
    prefix="/share",
)

@router.get("/search", tags=['share'])
def search_workbooks(search: str):
    workbooks = database.search_workbooks(search)
    if workbooks:
        return workbooks
    else:
        return {"message": "Workbook not found"}
    
@router.get("/search/{params}", tags=['share'])
def filter_workbooks(Subject: Optional[str] = None, Type: Optional[int] = None, Date: Optional[str] = None):
    workbooks = database.filter_workbooks(Subject, Type, Date)
    if workbooks:
        return workbooks
    else:
        return {"message": "Workbook not found"}
    



