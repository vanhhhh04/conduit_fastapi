from fastapi import APIRouter, Depends, HTTPException,Response, Body
from models.user import ArticleModel
from typing import List,Union,Dict
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
        article = session.get(ArticleModel, article_id)
        print(1)
        if article is None:
            response.status_code = 404
            return "Article not found"
        print(2)
        return article
    except Exception as e:
        print(3)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/articles/", tags=["articles"], response_model=ArticleModel)
async def post_articles(
    new_article: ArticleModel = Body(..., embed=True, alias="article"), session: Session = Depends(get_session)):
    try:
        # Extract the actual article dictionary from the nested structure
        print(new_article)
        new_article = ArticleModel(**new_article)

        # Add the new article to the session and commit
        session.add(new_article)
        session.commit()
        session.refresh(new_article)

        return new_article
    except Exception as e:
        print(1)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/article/{article_id}", tags=["articles"], response_model=Union[ArticleModel, str])
async def put_article(article_id: int, updated_article:ArticleModel, response:Response ,session: Session = Depends(get_session)):
    article = session.get(ArticleModel, article_id)

    if article is None:
        response.status_code = 404
        return "Article not found"
    article_dict = updated_article.dict(exclude_unset=True)
    for key,value in article_dict.items():
        if key != 'id':
            setattr(article, key, value)
            # article[key] = value
    session.add(article)
    session.commit()
    session.refresh(article)
    return article



@router.delete("/article/{article_id}", tags=["articles"], response_model=Union[ArticleModel, str])
async def delete_article(article_id: int, updated_article:ArticleModel, response:Response ,session: Session = Depends(get_session)):
    article = session.get(ArticleModel, article_id)

    if article is None:
        response.status_code = 404
        return "Article not found"

    session.delete(article)
    session.commit()
    return Response(status_code=200)