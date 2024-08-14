from datetime import datetime
from typing import List, Tuple 
from uuid import uuid4 

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base
from sqlmodel import Field, Relationship, SQLModel

# class Comment(Base):
#     __tablename__ ="comments"

#     id = Column(Integer, primary_key=True)
#     body = Column(String, index=True)
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)
#     # author_id = relationship()

# class Article(Base):
#     __tablename__ ="articles"

#     id = Column(Integer, primary_key=True)
#     slug = Column(String, index=True)
#     title = Column(String, index=True)
#     description = Column(String)
#     body = Column(String)
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)
    

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#     items = relationship("Item", back_populates="owner")

