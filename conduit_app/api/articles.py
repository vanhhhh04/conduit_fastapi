from fastapi import APIRouter, Depends, HTTPException,Response
from models.user import ArticleModel 
from typing import List,Union
from sqlmodel import Session, select
from models.database import get_session
# from sqlmodel import

router = APIRouter()


@router.get("/articles/", tags=["articles"], response_model=List[ArticleModel])
async def articles(session: Session = Depends(get_session)):
    try:
        statement = select(ArticleModel)
        results = session.exec(statement)
        articles = results.all()
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/articles/{article_id}", tags=["articles"], response_model=Union[ArticleModel, str])
async def article(article_id: int, response:Response ,session: Session = Depends(get_session)):
    try:
        article = session.get(ArithmeticError, article_id)
        if article is None: 
            response.status_code = 404 
            return "Artucle not found"
        return article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/articles/", tags=["articles"], response_model=ArticleModel)
async def articles(article: ArticleModel, session: Session = Depends(get_session)):
    session.add(article)
    session.commit()
    session.refresh(article)
    return article 