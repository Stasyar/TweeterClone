from sqlalchemy import Column, Integer, String

from core.models.base import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, nullable=False)
    filename = Column(String, nullable=False)
