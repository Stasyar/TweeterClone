from sqlalchemy import Column, ForeignKey, Integer

from core.models.base import Base


class Like(Base):
    __tablename__ = "like"

    id: int = Column(Integer, primary_key=True, nullable=False)
    user_id: int = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    tweet_id: int = Column(
        Integer, ForeignKey("tweet.id", ondelete="CASCADE"), nullable=False
    )
