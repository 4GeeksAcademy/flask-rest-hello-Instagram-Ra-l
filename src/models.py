from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Integer, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

follower_table = Table(
    "followers",
    db.metadata,
    Column("follower", ForeignKey("user.id"), primary_key=True),
    Column("followed", ForeignKey("user.id"), primary_key=True)
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
        primaryjoin=id == follower_table.c.followed,
        secondaryjoin=id == follower_table.c.follower,
        back_populates="following"
    )
    following: Mapped[list["User"]] = relationship(
        "User",
        secondary = follower_table,
        primaryjoin=id == follower_table.c.follower,
        secondaryjoin=id == follower_table.c.followed,
        back_populates="followers",
    )

    posts: Mapped [List["Post"]]= relationship(back_populates="user")
    comments: Mapped[List["Comment"]]= relationship("Comment", back_populates="author")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped [User] = relationship ("User", back_populates="posts")
    media: Mapped[List["Media"]] = relationship("Media", back_populates="post")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")


class Comment(db.Model):
    __tablename__ = "comment"

    id:Mapped[int] = mapped_column(primary_key=True)
    comment_text:Mapped[str] = mapped_column(String(500), nullable=False)
    author_id:Mapped [int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped [int] = mapped_column(ForeignKey("post.id")) 
    

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class Media(db.Model):
    __tablename__ = "media" 
    
    id:Mapped[int] = mapped_column(primary_key=True)
    type:Mapped[str] = mapped_column(String(50), nullable=False)
    url:Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"), nullable=False)
    post: Mapped[Post] = relationship("Post", back_populates="media")

