from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
import PyPDF2

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
