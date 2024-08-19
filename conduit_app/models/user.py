from sqlmodel import Field, Relationship, SQLModel,create_engine
from pydantic import EmailStr
from typing import Optional,List

from datetime import datetime

URL_DATABASE = 'postgresql://postgres:postgres@localhost:5432/conduit'

engine = create_engine(f"{URL_DATABASE}", echo=True)



class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = Field(default=None)
    email: str
    hashed_password: str
    bio: Optional[str] = None
    image: Optional[str] = None

    # Define a one-to-many relationship with ArticleModel
    articles: List["ArticleModel"] = Relationship(back_populates="author")

class ArticleModel(SQLModel, table=True):
    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str
    title: str
    description: str
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: Optional[int] = Field(default=None, foreign_key="users.id")
    # tag_list: Optional[List[str]] = Field(None, alias="tagList")
    # Define a relationship to UserModel
    author: Optional[UserModel] = Relationship(back_populates="articles")

class CommentModel(SQLModel, table=True):
    __tablename__ ="comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: int | None = Field(default=None, foreign_key="users.id")

