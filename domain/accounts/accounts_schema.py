from pydantic import BaseModel, field_validator, EmailStr, Field
from pydantic.fields import FieldInfo
from pydantic_core.core_schema import FieldValidationInfo

class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    useremail: EmailStr

    @field_validator('username', 'password1', 'password2', 'useremail')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return v

class AdminCreate(BaseModel):
    password1: str
    password2: str
    adminemail: EmailStr

    @field_validator( 'password1', 'password2', 'adminemail')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

#로그인 API의 출력 항목인 access_token, token_type, email을 속성으로 하는 스키마
class Token(BaseModel):
    access_token: str
    token_type: str
    useremail: str