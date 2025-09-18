from typing import List, Optional
from sqlalchemy.orm import Session
from .base_service import BaseService
from ..models.user import User
from ..schemas.user_schema import UserCreate, UserUpdate, UserRead
from ..enums.profile_type import ProfileType
from ..validations.user_validator import UserValidator

class UserService(BaseService[User, UserCreate, UserRead, UserUpdate]):
    def __init__(self):
        super().__init__(User, UserCreate, UserRead, UserUpdate)

    def get_by_profile(self, profile: str, enabled: bool = True, db: Optional[Session] = None) -> List[UserRead]:
        """
        Get users by profile and enabled status
        :param profile: User profile type as string (will be converted to ProfileType enum)
        :param enabled: Filter by enabled status
        :param db: Optional SQLAlchemy session
        :return: List of UserRead schemas
        :raises ValueError: If profile string is not a valid ProfileType
        """
        try:
            profile_enum = ProfileType(profile)
        except ValueError:
            raise ValueError(f"Invalid profile type: {profile}. Valid options are: {[p.value for p in ProfileType]}")
        
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.profile == profile_enum, self.model.enable == enabled).all()
            return [UserRead.model_validate(obj) for obj in objs]

    def get_by_app(self, app_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[UserRead]:
        """
        Get users by app_id and enabled status
        :param app_id: Associated App ID
        :param enabled: Filter by enabled status
        :param db: Optional SQLAlchemy session
        :return: List of UserRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.app_id == app_id, self.model.enable == enabled).all()
            return [UserRead.model_validate(obj) for obj in objs]

    def get_by_ext_key_clock_id(self, ext_key_clock_id: str, enabled: bool = True, db: Optional[Session] = None) -> List[UserRead]:
        """
        Get users by ext_key_clock_id and enabled status
        :param ext_key_clock_id: External Keycloak ID
        :param enabled: Filter by enabled status
        :param db: Optional SQLAlchemy session
        :return: List of UserRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.ext_key_clock_id == ext_key_clock_id, self.model.enable == enabled).all()
            return [UserRead.model_validate(obj) for obj in objs]

    def get_all(self, enabled: bool = True, db: Optional[Session] = None) -> List[UserRead]:
        """
        Get all users filtered by enabled status
        :param enabled: Filter by enabled status
        :param db: Optional SQLAlchemy session
        :return: List of UserRead schemas
        """
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.enable == enabled).all()
            return [UserRead.model_validate(obj) for obj in objs]

    def get_by_profile_and_app(self, profile: str, app_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[UserRead]:
        """
        Get users by profile, app_id and enabled status
        :param profile: User profile type as string (will be converted to ProfileType enum)
        :param app_id: Associated App ID
        :param enabled: Filter by enabled status
        :param db: Optional SQLAlchemy session
        :return: List of UserRead schemas
        :raises ValueError: If profile string is not a valid ProfileType
        """
        try:
            profile_enum = ProfileType(profile)
        except ValueError:
            raise ValueError(f"Invalid profile type: {profile}. Valid options are: {[p.value for p in ProfileType]}")
        
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.profile == profile_enum,
                self.model.app_id == app_id,
                self.model.enable == enabled
            ).all()
            return [UserRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: UserCreate, db: Optional[Session] = None):
        """Validation hook called automatically from BaseService.create()"""
        UserValidator.create_validate(db, obj_in)
