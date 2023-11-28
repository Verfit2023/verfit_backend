from fastapi import FastAPI
import uvicorn
from generation import generation
from home import home
from workbooks import workbooks
from share import share

app = FastAPI()

app.include_router(generation.router)
app.include_router(home.router)
app.include_router(workbooks.router)
app.include_router(share.router)

@app.get("/test")
def test():
    return "hello"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)