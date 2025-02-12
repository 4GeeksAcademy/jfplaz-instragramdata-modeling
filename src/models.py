import os
import sys
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, Column, Table, ForeignKey, Integer,String,Enum
from eralchemy2 import render_er
import enum
from typing import List

class MyEnum(enum.Enum):
    video = ".mp4"
    imagen= ".img"






Base = declarative_base()

# Segun la documentacion tenia que hacer una tabla de relacion. las hice pero no las entendi  y quede en blanco y por eso las
# comentadas. si puedes dejame un feedback al respecto. 

# post_association = Table(
#     "post_association",
#     Base.metadata,
#     Column("user_id", ForeignKey("user.id"), primary_key=True),
#     Column("post_id", ForeignKey("post.id"), primary_key=True),
# )

# Tabla de asociación para Comment
# comment_association = Table(
#     "comment_association",
#     Base.metadata,
#     Column("user_id", ForeignKey("user.id"), primary_key=True),
#     Column("comment_id", ForeignKey("comment.id"), primary_key=True),
# )

follower = Table(
    "followers",
    Base.metadata,
    Column("user_from_id", ForeignKey("user.id")),
    Column("user_to_id", ForeignKey("user.id")),
)

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firtsname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(String(80),nullable=False, unique=False)
    email: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")

   
class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] =  mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"), nullable=False)

    # Relaciones
    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    media: Mapped["media"] = relationship()
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    #  Relaciones
    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")
    media: Mapped[List["Media"]] = relationship("Media", back_populates="post")


class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MyEnum] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"), nullable=False)

    #  Relación con Post
    post: Mapped["Post"] = relationship("Post", back_populates="media")

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
