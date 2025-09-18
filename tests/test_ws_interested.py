import pytest
from unittest.mock import Mock, MagicMock, patch
from aclimate_v3_orm_frontend.services.ws_interested_service import WsInterestedService
from aclimate_v3_orm_frontend.schemas.ws_interested_schema import WsInterestedCreate
from aclimate_v3_orm_frontend.validations.ws_interested_validator import WsInterestedValidator

class TestWsInterestedService:
    
    def setup_method(self):
        """Setup for each test method"""
        self.ws_service = WsInterestedService()
        self.mock_db = Mock()
        
    @patch('aclimate_v3_orm_frontend.schemas.ws_interested_schema.WsInterestedRead.model_validate')
    def test_get_by_user_filters_correctly(self, mock_validate):
        """Test get_by_user filters by user_id correctly"""
        # Arrange
        mock_validate.return_value = {
            "id": 1,
            "user_id": 1,
            "ws_ext_id": "WS_123",
            "notification": {"email": True, "wp": False}
        }
        
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value.all.return_value = []
        
        self.ws_service._session_scope = MagicMock()
        self.ws_service._session_scope.return_value.__enter__.return_value = mock_session
        
        # Act
        result = self.ws_service.get_by_user(1, db=self.mock_db)
        
        # Assert
        mock_session.query.assert_called_once()
        mock_query.filter.assert_called_once()
        assert isinstance(result, list)
        
    @patch('aclimate_v3_orm_frontend.schemas.ws_interested_schema.WsInterestedRead.model_validate')
    def test_get_by_ws_ext_id_filters_correctly(self, mock_validate):
        """Test get_by_ws_ext_id filters by ws_ext_id correctly"""
        # Arrange
        mock_validate.return_value = {
            "id": 1,
            "user_id": 1,
            "ws_ext_id": "WS_123",
            "notification": {"email": True, "wp": False}
        }
        
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value.all.return_value = []
        
        self.ws_service._session_scope = MagicMock()
        self.ws_service._session_scope.return_value.__enter__.return_value = mock_session
        
        # Act
        result = self.ws_service.get_by_ws_ext_id("WS_123", db=self.mock_db)
        
        # Assert
        mock_session.query.assert_called_once()
        mock_query.filter.assert_called_once()
        assert isinstance(result, list)

class TestWsInterestedValidator:
    
    def test_validate_user_id_negative_raises_error(self):
        """Test that negative user_id raises ValueError"""
        with pytest.raises(ValueError, match="User ID must be a positive integer"):
            WsInterestedValidator.validate_user_id(-1)
    
    def test_validate_user_id_zero_raises_error(self):
        """Test that zero user_id raises ValueError"""
        with pytest.raises(ValueError, match="User ID must be a positive integer"):
            WsInterestedValidator.validate_user_id(0)
    
    def test_validate_ws_ext_id_empty_raises_error(self):
        """Test that empty ws_ext_id raises ValueError"""
        with pytest.raises(ValueError, match="The 'ws_ext_id' field is required"):
            WsInterestedValidator.validate_ws_ext_id("")
    
    def test_validate_ws_ext_id_too_long_raises_error(self):
        """Test that ws_ext_id too long raises ValueError"""
        long_id = "a" * 51
        with pytest.raises(ValueError, match="Weather station ext id cannot exceed 50 characters"):
            WsInterestedValidator.validate_ws_ext_id(long_id)
    
    def test_validate_notification_not_dict_raises_error(self):
        """Test that non-dict notification raises ValueError"""
        with pytest.raises(ValueError, match="Notification must be a valid JSON object"):
            WsInterestedValidator.validate_notification("not a dict")
    
    def test_validate_notification_empty_dict_raises_error(self):
        """Test that empty dict notification raises ValueError"""
        with pytest.raises(ValueError, match="Notification cannot be empty"):
            WsInterestedValidator.validate_notification({})
    
    def test_create_validate_calls_all_validations(self):
        """Test that create_validate calls all necessary validations"""
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        ws_create = WsInterestedCreate(
            user_id=1,
            ws_ext_id="WS_123",
            notification={"email": True, "wp": False}
        )
        
        # Should not raise any exception
        WsInterestedValidator.create_validate(mock_db, ws_create)