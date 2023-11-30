from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
import PyPDF2
from openai import OpenAI
from workbook.database import *
from accounts.schemas import *
from fastapi.responses import RedirectResponse
from datetime import datetime

load_dotenv()

router = APIRouter(
    prefix="/generation",
)

class Text(BaseModel):
    text: str


@router.post('/upload-file', tags=['generation'])
def upload_lecture_file(file: UploadFile):
    pdf_reader = PyPDF2.PdfReader(file.file)

    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
        text += '\n'

    if text == "":
        response = {"message": "파일 업로드 과정에서 에러가 발생했습니다."}
    else:
        response = {"message": "파일이 정상적으로 업로드 되었습니다."}

    return response


@router.post('/question', tags=['generation'])
def make_question_and_answer(problemType: int, text: Text):
    client = OpenAI()

    try:
        if problemType == 1:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "다음 내용 바탕으로 TF문제 3문제를 답과 함께 생성해주세요."},
                    {"role": "user", "content": text.text}
                ]
            )
        elif problemType == 2:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "다음 내용 바탕으로 빈칸 채우기 문제 3문제를 답과 함께 생성해주세요."},
                    {"role": "user", "content": text.text}
                ]
            )
        elif problemType == 3:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "다음 내용 바탕으로 단답형 문제 3문제를 답과 함께 생성해주세요."},
                    {"role": "user", "content": text.text}
                ]
            )
        else:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "다음 내용 바탕으로 서술형 문제 3문제를 답과 함께 생성해주세요."},
                    {"role": "user", "content": text.text}
                ]
            )
        
        return {"content": response.choices[0].message.content, "message": "문제가 생성되었습니다"}
    except:
        return {"message": "문제 생성 과정에서 오류가 발생하였습니다."} 



@router.post('/question/save', tags=['generation'])
def save_question(problemType: int, problem: Text, workbook_id: int):

    workbook = get_workbook(workbook_id)

    if workbook:
        list_of_probs = workbook.get("problems", [])
        list_of_probs.append((problemType, problem)) # question과 answer 어떻게 구분할 것인지 논의

        try:
            update_workbook(workbook_id, {"$set": {"problems": list_of_probs}})
            return {"message": "문제가 정상적으로 저장되었습니다."}
        except:
            return {"message": "문제 저장 과정에서 오류가 발생하였습니다."}
    else:
        return RedirectResponse(url="/newworkbook") # 이거 제대로 가는지 아직 확실 X...
    
@router.post('/summary', tags=['generation'])
def make_summary(text: Text):
    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "다음 내용을 노션 개요식으로 요약 및 정리해 주세요."},
                {"role": "user", "content": text.text}
            ]
        )
        return {"content": response.choices[0].message.content, "message": "요약본이 정상적으로 생성되었습니다."}
    except:
        return {"message": "요약 과정에서 에러가 발생하였습니다."}
    
@router.post('/summary/save', tags=['generation'])
def save_summary(content: Text, workbook_id: int):

    workbook = get_workbook(workbook_id)

    if workbook:
        list_of_sums = workbook.get("summaries", [])
        list_of_sums.append(content)

        try:
            update_workbook(workbook_id, {"$set": {"summaries": list_of_sums}})
            return {"message": "요약본이 정상적으로 저장되었습니다."}
        except:
            return {"message": "요약본 저장 과정에서 오류가 발생하였습니다."}
        
@router.post('/newworkbook', tags=['generation'])
def create_new_workbook(title: str, subject: str, description: str, owner: User):
    workbook = {"workbook_id":get_total_num_of_workbooks()+1, "title":title, "subject":subject, "description":description, "created_at":datetime(), "rate":0, "problems":[], "summaries":[], "owner": owner, "comments":[], "pubpriv":0}
    added_or_not = create_workbook(workbook)
    if added_or_not:
        return {"message": "새로운 문제집이 정상적으로 저장되었습니다."} 
    else:
        return {"message": "새로운 문제집을 저장하는 과정에서 오류가 발생하였거나, 문제집이 이미 존재합니다."} 