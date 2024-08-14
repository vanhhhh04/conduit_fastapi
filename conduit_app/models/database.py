
from sqlmodel import Field, SQLModel, create_engine
from typing import Optional 
from models.user import UserModel,ArticleModel,CommentModel


URL_DATABASE = 'postgresql://postgres:postgres@localhost:5432/conduit'

engine = create_engine(f"{URL_DATABASE}", echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)

