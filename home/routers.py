from fastapi import APIRouter
from dotenv import load_dotenv
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from workbook import database

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/home",
)


@router.get("", tags=['home'])
def get_workbooks(
    type: Optional[str] = None,
    keyword: Optional[str] = None,
):
    workbooks = database.get_workbooks()
    if type and keyword:
        if type == "제목":
            filtered_workbooks = [wb for wb in workbooks if keyword in wb.title]
        elif type == "과목":
            filtered_workbooks = [wb for wb in workbooks if keyword in wb.subject]
        elif type == "설명":
            filtered_workbooks = [wb for wb in workbooks if keyword in wb.description]
        else:
            filtered_workbooks = \
                [wb for wb in workbooks if (keyword in wb.title) or
                 (keyword in wb.subject) or (keyword in wb.description)]

        if filtered_workbooks:
            return {"workbooks": filtered_workbooks}
        else:
            return {"workbooks": [], "message": "Matching Workbooks not found", "type": type, "keyword": keyword}
    else:
        if workbooks:
            return {"workbooks": workbooks}
        else:
            return {"workbooks": [], "message": "Workbook not found"}
