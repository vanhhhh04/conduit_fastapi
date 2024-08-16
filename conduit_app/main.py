from fastapi import FastAPI
import uvicorn

from models.database import create_tables
from api.users import router as user_router
from api.articles import router as article_router


app = FastAPI()

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

app.include_router(user_router, tags=["user"])
app.include_router(article_router, tags=["articles"])


if __name__ == "__main__":
    create_tables()
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
