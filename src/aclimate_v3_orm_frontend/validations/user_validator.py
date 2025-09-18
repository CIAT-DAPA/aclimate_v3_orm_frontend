from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user_schema import UserCreate, UserUpdate
from ..enums.profile_type import ProfileType

class UserValidator:
    @staticmethod
    def validate_ext_key_clock_id(ext_key_clock_id: str):
        """Validate ext_key_clock_id is not empty"""
        if not ext_key_clock_id or not ext_key_clock_id.strip():
            raise ValueError("The 'ext_key_clock_id' field is required and cannot be empty.")
        if len(ext_key_clock_id) > 255:
            raise ValueError("External Keycloak ID cannot exceed 255 characters")

    @staticmethod
    def validate_profile(profile: ProfileType):
        """Validate profile is a valid ProfileType"""
        if profile not in ProfileType:
            raise ValueError(f"Profile must be one of: {[p.value for p in ProfileType]}")

    @staticmethod
    def validate_app_id(app_id: int):
        """Validate app_id is positive"""
        if app_id <= 0:
            raise ValueError("App ID must be a positive integer")

    @staticmethod
    def validate_unique_keycloak_app_combination(db: Session, ext_key_clock_id: str, app_id: int, exclude_id: int = None):
        """Check if the combination of ext_key_clock_id and app_id already exists in database"""
        query = db.query(User).filter(User.ext_key_clock_id == ext_key_clock_id, User.app_id == app_id)
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        if query.first():
            raise ValueError(f"A user with ext_key_clock_id '{ext_key_clock_id}' already exists for app '{app_id}'")

    @staticmethod
    def create_validate(db: Session, obj_in: UserCreate):
        """Validation for user creation"""
        UserValidator.validate_ext_key_clock_id(obj_in.ext_key_clock_id)
        UserValidator.validate_profile(obj_in.profile)
        UserValidator.validate_app_id(obj_in.app_id)
        UserValidator.validate_unique_keycloak_app_combination(db, obj_in.ext_key_clock_id, obj_in.app_id)

    @staticmethod
    def update_validate(db: Session, obj_in: UserUpdate, user_id: int):
        """Validation for user updates"""
        if hasattr(obj_in, 'ext_key_clock_id') and obj_in.ext_key_clock_id is not None:
            UserValidator.validate_ext_key_clock_id(obj_in.ext_key_clock_id)

        if hasattr(obj_in, 'profile') and obj_in.profile is not None:
            UserValidator.validate_profile(obj_in.profile)

        if hasattr(obj_in, 'app_id') and obj_in.app_id is not None:
            UserValidator.validate_app_id(obj_in.app_id)

        # If both ext_key_clock_id and app_id are being updated, check combination
        if (hasattr(obj_in, 'ext_key_clock_id') and obj_in.ext_key_clock_id is not None and 
            hasattr(obj_in, 'app_id') and obj_in.app_id is not None):
            UserValidator.validate_unique_keycloak_app_combination(
                db, obj_in.ext_key_clock_id, obj_in.app_id, exclude_id=user_id
            )
        elif hasattr(obj_in, 'ext_key_clock_id') and obj_in.ext_key_clock_id is not None:
            # If only ext_key_clock_id is being updated, get current app_id to check combination
            current_user = db.query(User).filter(User.id == user_id).first()
            if current_user:
                UserValidator.validate_unique_keycloak_app_combination(
                    db, obj_in.ext_key_clock_id, current_user.app_id, exclude_id=user_id
                )
        elif hasattr(obj_in, 'app_id') and obj_in.app_id is not None:
            # If only app_id is being updated, get current ext_key_clock_id to check combination
            current_user = db.query(User).filter(User.id == user_id).first()
            if current_user:
                UserValidator.validate_unique_keycloak_app_combination(
                    db, current_user.ext_key_clock_id, obj_in.app_id, exclude_id=user_id
                )