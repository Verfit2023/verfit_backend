from fastapi import FastAPI
from generation import generation
from workbook import workbook
import uvicorn

app = FastAPI(
    title="My API",
    description="API description",
    version="0.1.0",
    docs_url="/docs",
)

app.include_router(generation.router)
app.include_router(workbook.router)


@app.get("/test")
def test():
    return "hello"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
