from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta, datetime
from database import get_db
from domain.accounts import accounts_crud, accounts_schema
from domain.accounts.accounts_crud import pwd_context

router = APIRouter(prefix="/accounts",)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login")

class OAuth2PasswordRequestFormWithEmail(OAuth2PasswordRequestForm):
    email: str  # 기본적으로 username과 password 필드만 제공하므로, 이메일 필드 추가

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

#openssl rand -hex 32로 생성, 프로덕션 환경으로 이동하기 전에 secret_key 바꿀 예정, 그땐 git에 업로드 x
SECRET_KEY = "26dd12faef256d92eb89f24341fb01c591d0a9b563e6e5ce4e2e48d052a4f64a"
ALGORITHM = "HS256"

def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

#signup<-create
@router.post("/signup", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: accounts_schema.UserCreate, db: Session = Depends(get_db)):
    user = accounts_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    accounts_crud.create_user(db=db, user_create=_user_create)

#login
@router.post("/login", response_model=accounts_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestFormWithEmail = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = accounts_crud.get_user(db, form_data.email)

    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.email, #username이 아닌, email로 사용자 구분
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "useremail": user.email #email로 사용자 구분
    }


# User 회원 탈퇴
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), email: str = Depends(get_current_user_email)):
    user = accounts_crud.get_user(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
    
    db.delete(user)
    db.commit()
    return {"message": "계정이 성공적으로 삭제되었습니다."}

#admin signup
@router.post("/admin/signup", status_code=status.HTTP_204_NO_CONTENT)
def admin_create(_admin_create: accounts_schema.AdminCreate, db: Session = Depends(get_db)):
    admin = accounts_crud.get_existing_admin(db, admin_create=_admin_create)
    if admin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 관리자입니다.")
    accounts_crud.create_admin(db=db, admin_create=_admin_create)

#login
@router.post("/admin/login", response_model=accounts_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestFormWithEmail = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    admin = accounts_crud.get_admin(db, form_data.email)
    if not admin or not pwd_context.verify(form_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": admin.email, #username이 아닌, email로 사용자 구분
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "adminemail": admin.email #email로 사용자 구분
    }

# Admin 회원 탈퇴
@router.delete("/admin/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(db: Session = Depends(get_db), email: str = Depends(get_current_user_email)):
    admin = accounts_crud.get_admin(db, email)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="관리자를 찾을 수 없습니다.")

    db.delete(admin)
    db.commit()
    return {"message": "관리자가 성공적으로 삭제되었습니다."}