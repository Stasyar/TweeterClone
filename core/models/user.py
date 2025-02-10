from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.models.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    api_key = Column(String, unique=True, nullable=False)

    tweets = relationship("Tweet", backref="author")
