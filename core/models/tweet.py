from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String

from core.models.base import Base


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True, nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    content = Column(String(280), nullable=False)
    media = Column(ARRAY(Integer), nullable=True)
