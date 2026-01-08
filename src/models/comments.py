from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.orm import relationship

from .base import BaseTable


class Comments(BaseTable):
    __tablename__ = "comments"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    articles_id = Column(
        UUID(as_uuid=True),
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
    )

    body = Column(Text, nullable=False)

    user = relationship("Users", back_populates="comments")

    articles = relationship("Articles", back_populates="comments")

