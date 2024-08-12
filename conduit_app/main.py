from fastapi import APIRouter,FastAPI
import uvicorn

# from .models import user
from .models.database import SessionLocal, engine
from .models import database
from .api.users import router as user_router
from .api.articles import router as article_router


app = FastAPI()


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

app.include_router(user_router, tags=["user"])
app.include_router(article_router, tags=["articles"])


database.Base.metadata.create_all(bind=engine)

