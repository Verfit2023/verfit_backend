from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from accounts.schemas import User
from workbook.database import *
from workbook.models import *
from fastapi.responses import RedirectResponse
from accounts.dependencies import oauth2_scheme, get_current_user
from datetime import datetime
from database import db
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from accounts.dependencies import get_current_user

load_dotenv()

router = APIRouter(
    prefix="/workbook",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/{workbook_id}', tags=['workbook'])
def get_requested_workbook(workbook_id: int, current_user: UserInDB = Depends(get_current_user)):
    workbook = get_workbook(workbook_id)
    is_owner = False
    is_fav = False
    if workbook:
        if workbook.owner_email == current_user["useremail"]:
            is_owner = True
        if workbook.workbook_id in current_user["fav_workbook_id"]:
            is_fav = True
        return {"workbook":workbook, "isOwner": is_owner, "isFav": is_fav, "message":"해당하는 문제집을 성공적으로 불러왔습니다"}
    else:
        return {"message":"해당 문제집을 불러오는 과정에서 에러가 발생하였습니다"}


@router.post('/{workbook_id}/like', tags=['workbook'])
def like_or_dislike(workbook_id: int, current_user: UserInDB = Depends(get_current_user)):
    list_of_fav = current_user["fav_workbook_id"]
    if workbook_id in list_of_fav:
        list_of_fav.remove(workbook_id)
        is_fav = False
    else:
        list_of_fav.append(workbook_id)
        is_fav = True
    
    try:
        update_user_fav_workbooks(current_user["useremail"], list_of_fav)
        return {"isFav": is_fav, "message": "문제집을 즐겨찾기에 추가 혹은 삭제 완료하였습니다."}
    except:
        return {"message": "문제집을 즐겨찾기에 추가/삭제하는 도중 오류가 발생했습니다."}


@router.post('/{workbook_id}/addcomment', tags=['workbook'])
def add_comment(workbook_id: int, user: User, comment_content: str):

    workbook = get_workbook(workbook_id)

    if workbook:
        list_of_comm = workbook.comments
        comment = Comments(content=comment_content, writer=user.useremail, created_at=datetime.now())
        list_of_comm.append(comment)

        try:
            update_workbook(workbook_id, workbook)
            return {"message": "댓글이 성공적으로 추가되었습니다."}
        except:
            return {"message": "댓글 추가 중 오류가 발생했습니다."}
        
@router.post('/{workbook_id}/pubpriv', tags=['workbook'])
def pub_or_priv(workbook_id: int, user: User):

    list_of_made_workbooks = user.made_workbook_id

    workbook = get_workbook(workbook_id)

    if workbook_id in list_of_made_workbooks:
        if workbook.pubpriv == 0:
            workbook.pubpriv = 1
        else:
            workbook.pubpriv = 0

        try:
            update_workbook(workbook_id, workbook)
            return {"message": "문제집의 공개 여부를 변환 완료하였습니다."}
        except:
            return {"message": "문제집의 공개 여부를 변환하는 과정에서 오류가 발생하였습니다."}
    else:
        return {"message": "현재 유저가 만든 문제집이 아닙니다."}