from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True, nullable=False)
    api_key: str = Column(String, unique=True, nullable=False)
    name: str = Column(String, nullable=True)

    tweets = relationship("Tweet", backref="author")
