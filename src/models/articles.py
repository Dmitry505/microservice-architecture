import enum

from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, ForeignKey, Text, String, Enum
from sqlalchemy.orm import relationship

from .base import BaseTable


class ArticlesTags(str, enum.Enum):
    BACKEND = 'BACKEND' 
    FRONTEND = 'FRONTEND'
    QA = 'QA'
    FULLSTACK = 'FULLSTACK'
    DESIGN = 'DESIGN'
    ML = 'ML'


class Articles(BaseTable):
    __tablename__ = "articles"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(String(40),  nullable=False)

    description = Column(Text, nullable=False)

    body = Column(Text, nullable=False)

    tag_list = Column(ARRAY(String(50)), nullable=True)

    user = relationship("Users", back_populates="articles")

    comments = relationship(
        "Comments",
        back_populates="articles",
        cascade="all, delete-orphan",
    )
