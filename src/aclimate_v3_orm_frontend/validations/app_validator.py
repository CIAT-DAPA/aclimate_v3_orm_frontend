from sqlalchemy.orm import Session
from ..models.app import App
from ..schemas.app_schema import AppCreate, AppUpdate

class AppValidator:
    @staticmethod
    def validate_name(name: str):
        """Validate app name is not empty"""
        if not name or not name.strip():
            raise ValueError("The 'name' field is required and cannot be empty.")
        if len(name) > 255:
            raise ValueError("App name cannot exceed 255 characters")

    @staticmethod
    def validate_country_ext_id(country_ext_id: str):
        """Validate country_ext_id is not empty"""
        if not country_ext_id or not country_ext_id.strip():
            raise ValueError("The 'country_ext_id' field is required and cannot be empty.")
        if len(country_ext_id) > 50:
            raise ValueError("Country ext id cannot exceed 50 characters")

    @staticmethod
    def validate_unique_name_country_combination(db: Session, name: str, country_ext_id: str, exclude_id: int = None):
        """Check if the combination of name and country_ext_id already exists in database"""
        query = db.query(App).filter(App.name == name, App.country_ext_id == country_ext_id)
        if exclude_id:
            query = query.filter(App.id != exclude_id)
        if query.first():
            raise ValueError(f"An app with name '{name}' already exists for country '{country_ext_id}'")

    @staticmethod
    def create_validate(db: Session, obj_in: AppCreate):
        """Validation for app creation"""
        AppValidator.validate_name(obj_in.name)
        AppValidator.validate_country_ext_id(obj_in.country_ext_id)
        AppValidator.validate_unique_name_country_combination(db, obj_in.name, obj_in.country_ext_id)

    @staticmethod
    def update_validate(db: Session, obj_in: AppUpdate, app_id: int):
        """Validation for app updates"""
        if hasattr(obj_in, 'name') and obj_in.name is not None:
            AppValidator.validate_name(obj_in.name)

        if hasattr(obj_in, 'country_ext_id') and obj_in.country_ext_id is not None:
            AppValidator.validate_country_ext_id(obj_in.country_ext_id)

        # If both name and country_ext_id are being updated, check combination
        if (hasattr(obj_in, 'name') and obj_in.name is not None and 
            hasattr(obj_in, 'country_ext_id') and obj_in.country_ext_id is not None):
            AppValidator.validate_unique_name_country_combination(
                db, obj_in.name, obj_in.country_ext_id, exclude_id=app_id
            )
        elif hasattr(obj_in, 'name') and obj_in.name is not None:
            # If only name is being updated, get current country_ext_id to check combination
            current_app = db.query(App).filter(App.id == app_id).first()
            if current_app:
                AppValidator.validate_unique_name_country_combination(
                    db, obj_in.name, current_app.country_ext_id, exclude_id=app_id
                )
        elif hasattr(obj_in, 'country_ext_id') and obj_in.country_ext_id is not None:
            # If only country_ext_id is being updated, get current name to check combination
            current_app = db.query(App).filter(App.id == app_id).first()
            if current_app:
                AppValidator.validate_unique_name_country_combination(
                    db, current_app.name, obj_in.country_ext_id, exclude_id=app_id
                )