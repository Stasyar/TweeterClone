from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.models.base import Base


class Tweet(Base):
    __tablename__ = "tweet"

    id: int = Column(Integer, primary_key=True, nullable=False)
    author_id: int = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    content: str = Column(String(280), nullable=False)
    media = Column(ARRAY(Integer), nullable=True)

    likes = relationship(
        "Like", backref="tweet", cascade="all, delete", passive_deletes=True
    )
