from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from accounts.models import Users
from workbook.database import *
from fastapi.responses import RedirectResponse
from datetime import datetime

load_dotenv()

router = APIRouter(
    prefix="/workbook",
)


@router.get('/{workbook_id}', tags=['workbook'])
def get_requested_workbook(workbook_id: int):
    workbook = get_workbook(workbook_id)
    if workbook:
        return {"workbook":workbook, "message":"해당하는 문제집을 성공적으로 불러왔습니다"}
    else:
        return {"message":"해당 문제집을 불러오는 과정에서 에러가 발생하였습니다"}
    
@router.post('/{workbook_id}/like', tags=['workbook'])
def like_or_dislike(workbook_id: int, user: Users):
    list_of_fav = user.get("fav_workbook_id", [])
    if workbook_id in list_of_fav:
        list_of_fav.remove(workbook_id)
    else:
        list_of_fav.append(workbook_id)
    
    try:
        db.Users.update_one({"useremail": user.useremail}, {"$set": {"list_of_fav": list_of_fav}})
        return {"message": "문제집을 즐겨찾기에 추가 혹은 삭제 완료하였습니다."}
    except:
        return {"message": "문제집을 즐겨찾기에 추가/삭제하는 도중 오류가 발생했습니다."}
    
@router.post('/{workbook_id}/addcomment', tags=['workbook'])
def add_comment(workbook_id: int, user: Users, comment_content: str):

    workbook = get_workbook(workbook_id)

    if workbook:
        list_of_comm = workbook.get("comments", [])
        comment = {"content":comment_content, "writer":user, "created_at":datetime()}
        list_of_comm.append(comment)

        try:
            update_workbook(workbook_id, {"$set": {"summaries": list_of_comm}})
            return {"message": "댓글이 성공적으로 추가되었습니다."}
        except:
            return {"message": "댓글 추가 중 오류가 발생했습니다."}
        
@router.post('/{workbook_id}/pubpriv', tags=['workbook'])
def pub_or_priv(workbook_id: int, user: Users):

    list_of_made_workbooks = user.get("made_workbook_id", [])

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