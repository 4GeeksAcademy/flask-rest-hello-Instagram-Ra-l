from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Integer, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

follower_table = Table(
    "followers",
    db.metadata,
    Column("follower", ForeignKey("user.id"), primary_key=True),
    Column("follow_by", ForeignKey("user.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    followers: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        back_populates="follower_by"
    )
    following: Mapped[list["User"]] = relationship
    post: Mapped [List["Post"]]= relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites":self.favorites
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped [User] = relationship ("User", back_populates="post")
    media: Mapped[List["Media"]] = relationship("Media", back_populates="post")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")


class Comment(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    comment_text:Mapped[str] = mapped_column(String(500), nullable=False)
    author_id:Mapped [int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped [int] = mapped_column(ForeignKey("post.id")) 
    

    post: Mapped [List["User"]]= relationship(back_populates="user")


class Media(db.Model):
     id:Mapped[int] = mapped_column(primary_key=True)
     type:Mapped[str] = mapped_column(String(50), nullable=False)
     url:Mapped[str] = mapped_column(String(500), nullable=False)
     post_id:Mapped[int] = mapped_column(ForeignKey("post.id"))

