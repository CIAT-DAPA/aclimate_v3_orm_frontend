import pytest
from unittest.mock import Mock, MagicMock, patch
from aclimate_v3_orm_frontend.services.user_service import UserService
from aclimate_v3_orm_frontend.schemas.user_schema import UserCreate
from aclimate_v3_orm_frontend.validations.user_validator import UserValidator
from aclimate_v3_orm_frontend.enums.profile_type import ProfileType

class TestUserService:
    
    def setup_method(self):
        """Setup for each test method"""
        self.user_service = UserService()
        self.mock_db = Mock()
        
    @patch('aclimate_v3_orm_frontend.schemas.user_schema.UserRead.model_validate')
    def test_get_by_profile_valid_enum_string(self, mock_validate):
        """Test get_by_profile with valid enum string"""
        # Arrange
        mock_user = Mock()
        mock_user.id = 1
        mock_user.ext_key_clock_id = "keycloak_123"
        mock_user.app_id = 1
        mock_user.profile = ProfileType.FARMER
        mock_user.enable = True
        
        # Mock the validation to return a simple dict
        mock_validate.return_value = {
            "id": 1,
            "ext_key_clock_id": "keycloak_123",
            "app_id": 1,
            "profile": "FARMER",
            "enable": True
        }
        
        # Mock the session and query chain
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value.all.return_value = [mock_user]
        
        self.user_service._session_scope = MagicMock()
        self.user_service._session_scope.return_value.__enter__.return_value = mock_session
        
        # Act
        result = self.user_service.get_by_profile("FARMER", db=self.mock_db)
        
        # Assert
        assert len(result) == 1
        mock_session.query.assert_called_once()
        mock_query.filter.assert_called_once()
        mock_validate.assert_called_once_with(mock_user)
        
    def test_get_by_profile_invalid_enum_string_raises_error(self):
        """Test get_by_profile with invalid enum string raises ValueError"""
        with pytest.raises(ValueError, match="Invalid profile type"):
            self.user_service.get_by_profile("INVALID_PROFILE", db=self.mock_db)
    
    @patch('aclimate_v3_orm_frontend.schemas.user_schema.UserRead.model_validate')
    def test_get_by_app_filters_by_app_id(self, mock_validate):
        """Test get_by_app filters by app_id correctly"""
        # Arrange
        mock_validate.return_value = {
            "id": 1,
            "ext_key_clock_id": "keycloak_123",
            "app_id": 1,
            "profile": "FARMER",
            "enable": True
        }
        
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value.all.return_value = []
        
        self.user_service._session_scope = MagicMock()
        self.user_service._session_scope.return_value.__enter__.return_value = mock_session
        
        # Act
        result = self.user_service.get_by_app(1, db=self.mock_db)
        
        # Assert
        mock_session.query.assert_called_once()
        mock_query.filter.assert_called_once()
        assert isinstance(result, list)

class TestUserValidator:
    
    def test_validate_ext_key_clock_id_empty_raises_error(self):
        """Test that empty ext_key_clock_id raises ValueError"""
        with pytest.raises(ValueError, match="The 'ext_key_clock_id' field is required"):
            UserValidator.validate_ext_key_clock_id("")
    
    def test_validate_ext_key_clock_id_too_long_raises_error(self):
        """Test that ext_key_clock_id too long raises ValueError"""
        long_id = "a" * 256
        with pytest.raises(ValueError, match="External Keycloak ID cannot exceed 255 characters"):
            UserValidator.validate_ext_key_clock_id(long_id)
    
    def test_validate_profile_valid_does_not_raise_error(self):
        """Test that valid profile does not raise ValueError"""
        # This should not raise any exception
        try:
            UserValidator.validate_profile(ProfileType.FARMER)
            UserValidator.validate_profile(ProfileType.TECHNICIAN)
        except ValueError:
            pytest.fail("validate_profile raised ValueError for valid ProfileType")
    
    def test_validate_app_id_negative_raises_error(self):
        """Test that negative app_id raises ValueError"""
        with pytest.raises(ValueError, match="App ID must be a positive integer"):
            UserValidator.validate_app_id(-1)
    
    def test_validate_app_id_zero_raises_error(self):
        """Test that zero app_id raises ValueError"""
        with pytest.raises(ValueError, match="App ID must be a positive integer"):
            UserValidator.validate_app_id(0)
    
    def test_create_validate_calls_all_validations(self):
        """Test that create_validate calls all necessary validations"""
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        user_create = UserCreate(
            ext_key_clock_id="keycloak_123",
            app_id=1,
            profile=ProfileType.FARMER,
            enable=True
        )
        
        # Should not raise any exception
        UserValidator.create_validate(mock_db, user_create)