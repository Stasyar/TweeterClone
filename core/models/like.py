from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from core.models.base import Base


class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweet.id"), nullable=False)

