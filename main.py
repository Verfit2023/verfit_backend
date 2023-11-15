from fastapi import FastAPI
from routers import generation
import uvicorn

app = FastAPI()

app.include_router(generation.router)


@app.get("/test")
def test():
    return "hello"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
