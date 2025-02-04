from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from core.models.base import Base


class Tweet(Base):
    __tablename__ = "tweet"

    data: String = Column(String(200), nullable=False)
    media = Column(ARRAY(Integer))
    likes = Column(ARRAY(Integer))

    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="tweets")

    def __repr__(self):
        return f"Tweet {self.id}"
