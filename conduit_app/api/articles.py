from fastapi import APIRouter, Depends, HTTPException,Response, Body
from models.user import ArticleModel,UserModel
from .users import user_dependency
from typing import List,Union,Dict, Optional
from sqlmodel import Session, select
from models.database import get_session
from schema.articles import SingleArticleResponse,NewArticle
from datetime import datetime
from pydantic import BaseModel


# from sqlmodel import

router = APIRouter()
class AuthorResponse(BaseModel):
    username: Optional[str]  # Allow None values
    bio: Optional[str] = None
    image: Optional[str] = None
    following: Optional[bool] = None

class ArticleResponse(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tagList: List[str] = []
    createdAt: datetime
    updatedAt: datetime
    favorited: Optional[bool] = None
    favoritesCount: int
    author: Optional[AuthorResponse]  # Allow None values for author

class ArticlesResponse(BaseModel):
    articles: List[ArticleResponse]
    articlesCount: int


@router.get("/articles", tags=["articles"], response_model=ArticlesResponse)
async def articles(session: Session = Depends(get_session)):
    try:
        # Query to select all articles
        statement = select(ArticleModel)
        results = session.exec(statement)
        articles = results.all()

        response_articles = []

        for article in articles:
            response_articles.append({
                "slug": article.slug,
                "title": article.title,
                "description": article.description,
                "body": article.body,
                "tagList": [],  # Assuming tags are handled elsewhere
                "createdAt": article.created_at.isoformat(),
                "updatedAt": article.updated_at.isoformat(),
                "favorited": False,  # Placeholder, replace with actual logic if needed
                "favoritesCount": 0,  # Placeholder, replace with actual logic if needed
                "author": {
                    "username": article.author.username if article.author else "Unknown",
                    "bio": article.author.bio if article.author else None,
                    "image": article.author.image if article.author else None,
                    "following": False  # Placeholder, replace with actual logic if needed
                } if article.author else {
                    "username": "Unknown",
                    "bio": None,
                    "image": None,
                    "following": False
                }
            })

        return {"articles": response_articles, "articlesCount": len(articles)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/articles/{article_slug}", tags=["articles"])
async def article(article_slug: str, response:Response ,session: Session = Depends(get_session)):
    try:
        article = session.query(ArticleModel).filter(ArticleModel.slug == article_slug).first()
        if article is None:
            response.status_code = 404
            return "Article not found"
        return {"article":{
            "slug":article.slug,
            "title":article.title,
            "description":article.description,
            "body":article.body,
            "tagList":[],
            "createdAt":article.created_at,
            "updatedAt":article.updated_at,
            "favorited":None,
            "favoritesCount":0,
            "author":{
                "username":article.author.username,
                "bio":article.author.bio,
                "image":article.author.image,
                "following":None
            }
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/articles", tags=["articles"], response_model=SingleArticleResponse)
async def post_articles(
    user_instance: user_dependency,
    article: NewArticle = Body(embed=True),
    session: Session = Depends(get_session)
):
    try:
        print(type(article))
        article = ArticleModel(author=user_instance, **article.dict())
        # Add the new article to the session and commit
        session.add(article)
        session.commit()
        session.refresh(article)
        return {
  "article": {
    "slug": article.slug,
    "title": article.title,
    "description": article.description,
    "body": article.body,
    "tagList": ["dragons", "training"],
    "createdAt": article.created_at,
    "updatedAt": article.updated_at,
    "favorited": None,
    "favoritesCount": 0,
    "author": {
      "username": user_instance.username,
      "bio":user_instance.bio,
      "image": user_instance.image,
      "following": None,
    }
  }
}
    except Exception as e:
        print("Received article data:", article)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/article/{article_id}", tags=["articles"], response_model=Union[ArticleModel, str])
async def put_article(
    article_id: int,
    response:Response ,
    article: ArticleModel = Body(embed=True),
    session: Session = Depends(get_session)
):
    article = session.get(ArticleModel, article_id)

    if article is None:
        response.status_code = 404
        return "Article not found"
    article_dict = article.dict(exclude_unset=True)
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

