from datetime import datetime
from typing import List, Optional, Sequence

from pydantic import BaseModel, Field
from schema.users import Profile
from models.user import UserModel,ArticleModel


class Article(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    author: Profile


class SingleArticleResponse(BaseModel):
    article: Article

    @classmethod
    def from_article_instance(
        cls, article: ArticleModel, user: Optional[UserModel] = None
    ) -> "SingleArticleResponse":
        return cls(article=Article.from_article_instance(article=article, user=user))



class NewArticle(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tag_list: Optional[List[str]] = Field(None, alias="tagList")

