from sqlalchemy.orm import Session
from ..models.ws_interested import WsInterested
from ..schemas.ws_interested_schema import WsInterestedCreate, WsInterestedUpdate

class WsInterestedValidator:
    @staticmethod
    def validate_user_id(user_id: int):
        """Validate user_id is positive"""
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer")

    @staticmethod
    def validate_ws_ext_id(ws_ext_id: str):
        """Validate ws_ext_id is not empty"""
        if not ws_ext_id or not ws_ext_id.strip():
            raise ValueError("The 'ws_ext_id' field is required and cannot be empty.")
        if len(ws_ext_id) > 50:
            raise ValueError("Weather station ext id cannot exceed 50 characters")

    @staticmethod
    def validate_notification(notification: dict):
        """Validate notification is a valid dict"""
        if not isinstance(notification, dict):
            raise ValueError("Notification must be a valid JSON object")
        if not notification:
            raise ValueError("Notification cannot be empty")

    @staticmethod
    def validate_unique_user_ws_combination(db: Session, user_id: int, ws_ext_id: str, exclude_id: int = None):
        """Check if user is already interested in this weather station"""
        query = db.query(WsInterested).filter(
            WsInterested.user_id == user_id,
            WsInterested.ws_ext_id == ws_ext_id
        )
        if exclude_id:
            query = query.filter(WsInterested.id != exclude_id)
        if query.first():
            raise ValueError(f"User {user_id} is already interested in weather station '{ws_ext_id}'")

    @staticmethod
    def create_validate(db: Session, obj_in: WsInterestedCreate):
        """Validation for ws_interested creation"""
        WsInterestedValidator.validate_user_id(obj_in.user_id)
        WsInterestedValidator.validate_ws_ext_id(obj_in.ws_ext_id)
        WsInterestedValidator.validate_notification(obj_in.notification)
        WsInterestedValidator.validate_unique_user_ws_combination(db, obj_in.user_id, obj_in.ws_ext_id)

    @staticmethod
    def update_validate(db: Session, obj_in: WsInterestedUpdate, ws_interested_id: int):
        """Validation for ws_interested updates"""
        if hasattr(obj_in, 'user_id') and obj_in.user_id is not None:
            WsInterestedValidator.validate_user_id(obj_in.user_id)

        if hasattr(obj_in, 'ws_ext_id') and obj_in.ws_ext_id is not None:
            WsInterestedValidator.validate_ws_ext_id(obj_in.ws_ext_id)

        if hasattr(obj_in, 'notification') and obj_in.notification is not None:
            WsInterestedValidator.validate_notification(obj_in.notification)

        # Check unique combination if both user_id and ws_ext_id are being updated
        if (hasattr(obj_in, 'user_id') and obj_in.user_id is not None and 
            hasattr(obj_in, 'ws_ext_id') and obj_in.ws_ext_id is not None):
            WsInterestedValidator.validate_unique_user_ws_combination(
                db, obj_in.user_id, obj_in.ws_ext_id, exclude_id=ws_interested_id
            )