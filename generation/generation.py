from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
import PyPDF2
from openai import OpenAI
from workbook.database import *
from workbook.models import *
from accounts.schemas import *
from fastapi.responses import RedirectResponse
from datetime import datetime
import os
import openai

API_KEY= 'sk-**'
os.environ["OPENAI_API_KEY"] = API_KEY

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

@router.get("/newworkbook/getdata", tags=['generation'])
def get_data():
    return


@router.post('/newworkbook', tags=['generation'])
def create_new_workbook(title: str, subject: str, description: str, owner: User):
    workbook = Workbook(workbook_id=get_total_num_of_workbooks()+1, title=title, subject=subject, description=description, created_at=datetime.now(), rate=0, problems=[], summaries=[], owner_email=owner.useremail, comments=[], pubpriv=0)
    try:
        added_or_not = create_workbook(workbook)
        return {"message": "새로운 문제집이 정상적으로 저장되었습니다."} 
    except Exception as e:
        return {"message": f"새로운 문제집을 저장하는 과정에서 오류가 발생하였거나, 문제집이 이미 존재합니다: {str(e)}"} 


@router.post('/question', tags=['generation'])
def make_question_and_answer(problemType: int, text: Text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        if problemType == 1:
            response = openai.completions.create(
                model="ft:davinci-002:verfit::8PV6Zmzw",
                prompt="role: user, content: based on lecture content "+text.text+", create 10 True or False questions with answers and explanations.",
                max_tokens=2048,
                temperature=0.8
            )
        elif problemType == 2:
             response = openai.completions.create(
                model="ft:babbage-002:verfit::8PV5wQQV",
                prompt="role: user, content:"+text.text+"의 학습 자료를 기반으로, Fill in the Blank 유형의 문제 10개를 problem의 변수명으로, 그리고 답을 answer의 변수명으로, 그에 대한 설명을 explanations의 변수명으로 생성해 주세요"
            )
        elif problemType == 3:
            response = openai.completions.create(
                model="ft:babbage-002:verfit::8PV5wQQV",
                prompt="role: user, content:"+text.text+"의 학습 자료를 기반으로, Short Answer 유형의 문제 10개를 problem의 변수명으로, 그리고 답을 answer의 변수명으로, 그에 대한 설명을 explanations의 변수명으로 생성해 주세요"
            )
        else:
            response = openai.completions.create(
                model="ft:babbage-002:verfit::8PV5wQQV",
                prompt="role: user, content:"+text.text+"의 학습 자료를 기반으로, Essay 유형의 문제 10개를 problem의 변수명으로, 그리고 답을 answer의 변수명으로, 그에 대한 설명을 explanations의 변수명으로 생성해 주세요"
            )
        
        return {"content": response.choices[0].text, "message": "문제가 생성되었습니다"}
    except Exception as e:
        return {"message": f"문제 생성 과정에서 오류가 발생하였습니다: {str(e)}"}




@router.post('/question/save', tags=['generation'])
def save_question(problemType: int, problem: Text, workbook_id: int):

    workbook = get_workbook(workbook_id)

    if workbook:
        list_of_probs = workbook.problems
        list_of_probs.append((problemType, problem)) # question과 answer 어떻게 구분할 것인지 논의

        try:
            update_workbook(workbook_id, workbook)
            return {"message": "문제가 정상적으로 저장되었습니다."}
        except Exception as e:
            return {"message": f"문제 저장 과정에서 오류가 발생하였습니다: {str(e)}"}
    else:
        return RedirectResponse("/generation/newworkbook/getdata", status_code=303) # 이거 제대로 가는지 아직 확실 X...
    
@router.post('/summary', tags=['generation'])
def make_summary(text: Text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "다음 내용을 노션 개요식으로 요약 및 정리해 주세요."},
                {"role": "user", "content": text.text}
            ]
        )
        return {"content": response.choices[0].message.content, "message": "요약본이 정상적으로 생성되었습니다."}
    except Exception as e:
        return {"message": "요약 과정에서 에러가 발생하였습니다."}
    
@router.post('/summary/save', tags=['generation'])
def save_summary(content: Text, workbook_id: int):

    workbook = get_workbook(workbook_id)

    if workbook:
        list_of_sums = workbook.summaries
        list_of_sums.append(content)

        try:
            update_workbook(workbook_id, workbook)
            return {"message": "요약본이 정상적으로 저장되었습니다."}
        except:
            return {"message": "요약본 저장 과정에서 오류가 발생하였습니다."}