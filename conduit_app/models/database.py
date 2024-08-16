
from sqlmodel import Field, SQLModel, create_engine
from typing import Optional
from models.user import UserModel,ArticleModel,CommentModel
from sqlmodel import Session


URL_DATABASE = 'postgresql://postgres:postgres@localhost:5433/conduit_fast'

engine = create_engine(f"{URL_DATABASE}", echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

