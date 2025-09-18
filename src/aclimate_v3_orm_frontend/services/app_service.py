from typing import List, Optional
from sqlalchemy.orm import Session
from .base_service import BaseService
from ..models.app import App
from ..schemas.app_schema import AppCreate, AppUpdate, AppRead
from ..validations.app_validator import AppValidator

class AppService(BaseService[App, AppCreate, AppRead, AppUpdate]):

    def __init__(self):
        super().__init__(App, AppCreate, AppRead, AppUpdate)

    def get_by_country_ext_id(self, country_ext_id: str, enabled: bool = True, db: Optional[Session] = None) -> List[AppRead]:
        """
        Get apps by country_ext_id and enabled status
        :param country_ext_id: External country ID
        :param enabled: Filter by enabled status
        :param db: Optional SQLAlchemy session
        :return: List of AppRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.country_ext_id == country_ext_id, self.model.enable == enabled).all()
            return [AppRead.model_validate(obj) for obj in objs]

    def get_by_name(self, name: str, enabled: bool = True, db: Optional[Session] = None) -> List[AppRead]:
        """
        Get apps by exact name and enabled status
        :param name: App name
        :param enabled: Filter by enabled status
        :param db: Optional SQLAlchemy session
        :return: List of AppRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.name == name, self.model.enable == enabled).all()
            return [AppRead.model_validate(obj) for obj in objs]

    def search_by_name(self, name: str, enabled: bool = True, db: Optional[Session] = None) -> List[AppRead]:
        """
        Search apps by partial name match and enabled status
        :param name: Partial app name
        :param enabled: Filter by enabled status
        :param db: Optional SQLAlchemy session
        :return: List of AppRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.name.ilike(f"%{name}%"), self.model.enable == enabled).all()
            return [AppRead.model_validate(obj) for obj in objs]

    def get_all(self, enabled: bool = True, db: Optional[Session] = None) -> List[AppRead]:
        """
        Get all apps filtered by enabled status
        :param enabled: Filter by enabled status
        :param db: Optional SQLAlchemy session
        :return: List of AppRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.enable == enabled).all()
            return [AppRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: AppCreate, db: Optional[Session] = None):
        """Validation hook called automatically from BaseService.create()"""
        AppValidator.create_validate(db, obj_in)
