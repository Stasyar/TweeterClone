from sqlalchemy import Column, Integer, String

from core.models.base import Base


class Media(Base):
    __tablename__ = "media"

    id: int = Column(Integer, primary_key=True, nullable=False)
    filename: str = Column(String, nullable=False)
