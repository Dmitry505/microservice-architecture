from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseTable


class Users(BaseTable):
    __tablename__ = "users"

    username = Column(
        String(40),
        unique=True,
        nullable=False,
        index=True,
        doc="Username for authentication.",
    )

    email = Column(
        String(40), 
        unique=True, 
        nullable=False, 
        index=True, 
        doc="User's email"
    )

    password = Column(
        String(255), 
        unique=False, 
        nullable=False,  
        doc="User's password"
    )

    bio = Column(
        String(100), 
        unique=False, 
        nullable=True, 
        doc="User's bio"
    )

    image_url = Column(
        String(100), 
        unique=False, 
        nullable=True, 
        doc="User's image_url"
    )

    articles = relationship(
        "Articles",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    comments = relationship(
        "Comments",
        back_populates="user",
        cascade="all, delete-orphan",
    )