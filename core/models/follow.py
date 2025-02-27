from sqlalchemy import Column, ForeignKey, Integer

from core.models.base import Base


class Follow(Base):
    __tablename__ = "follow"

    id: int = Column(Integer, primary_key=True, nullable=False)
    follower_id: int = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    following_id: int = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
