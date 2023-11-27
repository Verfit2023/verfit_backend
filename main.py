from fastapi import FastAPI
from generation import generation
from workbook import workbook
from accounts import routers as accounts
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

from database import db

app = FastAPI(
    title="My API",
    description="API description",
    version="0.1.0",
    docs_url="/docs",
)

app.db = db
app.add_middleware(SessionMiddleware, secret_key="f65db23bc05cf219709a76078fead95507d023cc2ef0d278ff09a180c92100d9") #정식 배포전 변경, 분리 예정

app.include_router(generation.router)
app.include_router(workbook.router)
app.include_router(accounts.router)

@app.get("/test")
def test():
    return "hello"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

