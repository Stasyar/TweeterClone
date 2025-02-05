from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from core.models.base import Base


class Follow(Base):
    __tablename__ = "follow"

    id = Column(Integer, primary_key=True, nullable=False)
    follower_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("user.id"), nullable=False)

