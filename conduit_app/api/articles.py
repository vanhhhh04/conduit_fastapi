from fastapi import APIRouter


router = APIRouter()
@router.get("/articles/", tags=["articles"])
async def read_articles():
    return [{"name": "article1"}, {"date_relase": "2024-10-08"}]
