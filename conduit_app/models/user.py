from sqlmodel import Field, Relationship, SQLModel,create_engine
from pydantic import EmailStr
from typing import Optional

from datetime import datetime

URL_DATABASE = 'postgresql://postgres:postgres@localhost:5432/conduit'

engine = create_engine(f"{URL_DATABASE}", echo=True)
class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    bio: Optional[str] = None
    image: Optional[str] = None
    # following_ids: int | None = Field(default=None, foreign_key="users.id")

class ArticleModel(SQLModel, table=True):
    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str
    # NOTE: slug is not a primary field because it could change and this would imply to
    # change all the references
    title: str
    description: str
    body: str
    # tag_list: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    author: int | None = Field(default=None, foreign_key="users.id")

    # favorited_user_ids: Tuple[ObjectId, ...] = ()
    comments: int | None = Field(default=None, foreign_key="users.id")


class CommentModel(SQLModel, table=True):
    __tablename__ ="comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    body: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: int | None = Field(default=None, foreign_key="users.id") 
class CommentModel(SQLModel, table=True):
    __tablename__ ="comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    body: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: int | None = Field(default=None, foreign_key="users.id") 
