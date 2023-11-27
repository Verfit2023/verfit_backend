from fastapi import APIRouter, Depends, HTTPException
from . import schemas, crud, dependencies
from .dependencies import oauth2_scheme, create_access_token, admin_oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

router = APIRouter(prefix="/accounts")


@router.post("/signup", response_model=schemas.User)
async def signup(user: schemas.User):
    if await crud.get_user_by_email(user.useremail):
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user)

@router.post("/admin/signup", response_model=schemas.Admin)
async def admin_signup(admin: schemas.Admin):
    if await crud.get_admin_by_email(admin.adminemail):
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_admin(admin)

@router.post("/login")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await dependencies.authenticate_accounts(form_data.username, form_data.password, is_admin=False)
        access_token = create_access_token(data={"sub": user["useremail"]})
        request.session['token'] = access_token
        return {
            "message": "User logged in successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "email": form_data.username #email로 사용자 구분
        }
    except:
        raise HTTPException(status_code=401, detail="Incorrect useremail or password",headers={"WWW-Authenticate": "Bearer"},)


@router.post("/admin/login")
async def adminLogin_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        admin = await dependencies.authenticate_accounts(form_data.username, form_data.password, is_admin= True)
        access_token = create_access_token(data={"sub": admin["adminemail"]})
        request.session['token'] = access_token
        return {
            "message": "Admin logged in successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "email": form_data.username, #email로 사용자 구분
        }
    except:
        raise HTTPException(status_code=401, detail="Incorrect adminemail or password",headers={"WWW-Authenticate": "Bearer"},)


@router.post("/logout")
async def user_logout(request: Request):
    token = await dependencies.get_token_from_session(request)
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = dependencies.decode_access_token(token)
    await crud.logout_user(dependencies.db, token_jti=payload["jti"], token_exp=datetime.fromtimestamp(payload["exp"]))
    request.session.pop('token', None)  # 세션에서 토큰 제거
    return {"message": "User logged out successfully"}

@router.post("/admin/logout")
async def admin_logout(request: Request): 
    token = await dependencies.get_token_from_session(request)
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = dependencies.decode_access_token(token)
    await crud.logout_user(dependencies.db, token_jti=payload["jti"], token_exp=datetime.fromtimestamp(payload["exp"]))
    request.session.pop('token', None)  # 세션에서 토큰 제거
    return {"message": "Admin logged out successfully"}


@router.delete("/delete")
async def delete_user_account(request: Request):
    token = await dependencies.get_token_from_session(request)
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = await dependencies.get_current_user(token)
    await crud.delete_user(user["useremail"])
    return {"message": "User account deleted successfully"}

@router.delete("/admin/delete")
async def delete_admin_account(request: Request):
    token = await dependencies.get_token_from_session(request)
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    admin = await dependencies.get_current_admin(token)
    await crud.delete_admin(admin["adminemail"])
    return {"message": "Admin account deleted successfully"}