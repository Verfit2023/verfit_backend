from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
import PyPDF2
from openai import OpenAI

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

    return text


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
