from fastapi import FastAPI
import uvicorn

from routers import generation
from domain.accounts import accounts_router

"""
alembic 없이 테이블 생성하기
데이터베이스에 테이블이 존재하지 않을 경우에만 테이블을 생성한다. 한번 생성된 테이블에 대한 변경 관리를 할 수는 없다.
import models
from database import engine
models.Base.metadata.create_all(bind=engine)
"""


app = FastAPI()

app.include_router(generation.router)
app.include_router(accounts_router.router)

@app.get("/test")
def test():
    return "hello"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

