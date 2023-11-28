from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
import workbooks.database as database
from workbooks.models import Workbook
from dotenv import load_dotenv
import PyPDF2
from openai import OpenAI

load_dotenv()

router = APIRouter(
    prefix="/generation",
)

class Text(BaseModel):
    text: str

# PDF 파일
# PDF 파일 업로드
@router.post('/upload-file', tags=['generation'])
def upload_lecture_file(file: UploadFile):
    pdf_reader = PyPDF2.PdfReader(file.file)

    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
        text += '\n'

    return text

# 텍스트로 문제 생성
@router.post('/question', tags=['generation'])
def make_question(text: Text):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "다음 내용 바탕으로 TF 3문제를 답과 함께 생성해주세요."},
            {"role": "user", "content": text.text}
        ]
    )
    return response.choices[0].message.content

# Workbooks column 
# 데이터베이스 워크북 생성
@router.post("/workbooks/", tags=['generation'])
def add_workbook(workbook: Workbook):
    response = database.create_workbook(workbook)
    return {"message": response}

'''
# 데이터베이스 워크북 조회
@router.get("/workbooks/{workbook_id}", tags=['generation'])
def get_workbook(workbook_id: int):
    workbook = database.get_workbook(workbook_id)
    if workbook:
        return workbook
    else:
        return {"message": "Workbook not found"}

# 데이터베이스 워크북 수정
@router.put("/workbooks/{workbook_id}", tags=['generation'])
def update_workbook(workbook_id: int, workbook: Workbook):
    response = database.update_workbook(workbook_id, workbook)
    return {"message": response}

# 데이터베이스 워크북 삭제
@router.delete("/workbooks/{workbook_id}", tags=['generation'])
def delete_workbook(workbook_id: int):
    response = database.delete_workbok(workbook_id)
    return {"message": response}
'''