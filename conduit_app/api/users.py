from fastapi import APIRouter, Depends, HTTPException,Response
from models.user import ArticleModel
from typing import List,Union
from sqlmodel import Session, select
from models.database import get_session

router = APIRouter()

@router.post("/articles/", tags=["articles"], response_model=ArticleModel)
async def post_articles(article: ArticleModel, session: Session = Depends(get_session)):
    session.add(article)
    session.commit()
    session.refresh(article)
    return article
