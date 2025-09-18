from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database.base import Base

class WsInterested(Base):
    __tablename__ = 'ws_interested'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ws_ext_id = Column(String(50), nullable=False)
    notification = Column(JSON, nullable=False)

    user = relationship("User", back_populates="ws_interested")
