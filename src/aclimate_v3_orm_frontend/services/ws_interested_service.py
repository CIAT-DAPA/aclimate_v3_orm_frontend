from typing import List, Optional
from sqlalchemy.orm import Session
from .base_service import BaseService
from ..models.ws_interested import WsInterested
from ..schemas.ws_interested_schema import WsInterestedCreate, WsInterestedUpdate, WsInterestedRead
from ..validations.ws_interested_validator import WsInterestedValidator

class WsInterestedService(BaseService[WsInterested, WsInterestedCreate, WsInterestedRead, WsInterestedUpdate]):
    def __init__(self):
        super().__init__(WsInterested, WsInterestedCreate, WsInterestedRead, WsInterestedUpdate)

    def get_by_user(self, user_id: int, db: Optional[Session] = None) -> List[WsInterestedRead]:
        """
        Get weather station interests by user_id
        :param user_id: Associated User ID
        :param db: Optional SQLAlchemy session
        :return: List of WsInterestedRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.user_id == user_id).all()
            return [WsInterestedRead.model_validate(obj) for obj in objs]

    def get_by_ws_ext_id(self, ws_ext_id: str, db: Optional[Session] = None) -> List[WsInterestedRead]:
        """
        Get weather station interests by ws_ext_id
        :param ws_ext_id: External weather station ID
        :param db: Optional SQLAlchemy session
        :return: List of WsInterestedRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.ws_ext_id == ws_ext_id).all()
            return [WsInterestedRead.model_validate(obj) for obj in objs]

    def get_all(self, db: Optional[Session] = None) -> List[WsInterestedRead]:
        """
        Get all weather station interests
        :param db: Optional SQLAlchemy session
        :return: List of WsInterestedRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).all()
            return [WsInterestedRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: WsInterestedCreate, db: Optional[Session] = None):
        """Validation hook called automatically from BaseService.create()"""
        WsInterestedValidator.create_validate(db, obj_in)
