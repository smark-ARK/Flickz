from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    related_text = Column(String, primary_key=False, nullable=True)
    images = Column(ARRAY(String), primary_key=False, nullable=True)
    published = Column(Boolean, server_default="TRUE")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")
    comments = relationship("Comment")


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    about = Column(String, nullable=True)
    profile_photo = Column(
        String,
        nullable=True,
        default="https://storage.googleapis.com/simple-social-posts/person_male.jpg",
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    followers = relationship(
        "Followers", foreign_keys="[Followers.follower_id]", back_populates="follower"
    )
    following = relationship(
        "Followers", foreign_keys="[Followers.following_id]", back_populates="following"
    )


class Votes(Base):
    __tablename__ = "votes"
    user_id = Column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )


class Followers(Base):
    __tablename__ = "followers"
    id = Column(Integer, primary_key=True, nullable=False)
    follower_id = Column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
    )
    following_id = Column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="followers"
    )
    following = relationship(
        "User", foreign_keys=[following_id], back_populates="following"
    )


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    comment = Column(String, nullable=False)
    post = relationship("post", back_populates="comments")
