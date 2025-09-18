from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from ..enums.enums import ProfileType
from datetime import datetime, timezone

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    ext_key_clock_id = Column(String(255), nullable=False)
    app_id = Column(Integer, ForeignKey('apps.id'))
    profile = Column(Enum(ProfileType), nullable=False)
    enable = Column(Boolean, default=True)
    register = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    app = relationship("App", back_populates="users")
    ws_interested = relationship("WsInterested", back_populates="user")
