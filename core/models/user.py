from sqlalchemy import ARRAY, Column, Integer
from sqlalchemy.orm import Mapped, relationship

from core.models.base import Base


class User(Base):
    __tablename__ = "user"

    followers = Column(ARRAY(Integer))
    following = Column(ARRAY(Integer))

    tweets = relationship("Tweet", back_populates="author")

    def __repr__(self):
        return f"User {self.id}"
