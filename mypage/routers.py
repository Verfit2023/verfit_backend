# routers.py
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from .crud import get_user_info, update_user_info, perform_ability_test
from .schemas import MyPageResponse, UserInfo, AbilityTestAnswers, UserUpdate, AbilityTestResult
from accounts.dependencies import oauth2_scheme, get_current_user, get_token_from_session
from .abilityTest import questions


router = APIRouter(prefix="/mypage", tags=['mypage'])

@router.post("",response_model=MyPageResponse) 
async def get_my_page(request: Request):
    token = await get_token_from_session(request)
    
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = await get_current_user(token)

    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user_info = await get_user_info(user['useremail'])

    return MyPageResponse(
        nickname=user_info.user['username'],
        useremail=user_info.user['useremail'],
        ability_score=user_info.user['ability_score'],
        myWorkbooks=user_info.myWorkbooks,
        favWorkbooks=user_info.favWorkbooks
    )

#update user-info
@router.put("/profile", response_model=MyPageResponse)
async def update_profile(user_update: UserUpdate, request: Request):
    token = await get_token_from_session(request)
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = await get_current_user(token)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    updated_user_info = await update_user_info(user['useremail'], user_update)
    return MyPageResponse(
        nickname=updated_user_info.user['username'],
        useremail=updated_user_info.user['useremail'],
        ability_score=updated_user_info.user['ability_score'],
        myWorkbooks=updated_user_info.myWorkbooks,
        favWorkbooks=updated_user_info.favWorkbooks
    )


@router.post("/ability_test/submit") #, response_model=AbilityTestResult
async def ability_test_submit( test_answer: AbilityTestAnswers, request: Request):
    token = await get_token_from_session(request)
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = await get_current_user(token)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    test_result = await perform_ability_test(user['useremail'], test_answer)
    return test_result # AbilityTestResult(test_result) #**test_result

@router.get("/ability_test")
async def get_ability_test():
    return questions
