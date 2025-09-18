import pytest
from unittest.mock import Mock, MagicMock, patch
from aclimate_v3_orm_frontend.services.app_service import AppService
from aclimate_v3_orm_frontend.schemas.app_schema import AppCreate
from aclimate_v3_orm_frontend.validations.app_validator import AppValidator

class TestAppService:
    
    def setup_method(self):
        """Setup for each test method"""
        self.app_service = AppService()
        self.mock_db = Mock()
        
    @patch('aclimate_v3_orm_frontend.schemas.app_schema.AppRead.model_validate')
    def test_get_by_name_returns_apps(self, mock_validate):
        """Test get_by_name returns list of apps"""
        # Arrange
        mock_app = Mock()
        mock_app.id = 1
        mock_app.name = "Test App"
        mock_app.country_ext_id = "1"
        mock_app.enable = True
        
        # Mock the validation to return a simple dict
        mock_validate.return_value = {
            "id": 1, 
            "name": "Test App", 
            "country_ext_id": "1", 
            "enable": True
        }
        
        # Mock the session and query chain
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value.all.return_value = [mock_app]
        
        self.app_service._session_scope = MagicMock()
        self.app_service._session_scope.return_value.__enter__.return_value = mock_session
        
        # Act
        result = self.app_service.get_by_name("Test App", db=self.mock_db)
        
        # Assert
        assert len(result) == 1
        mock_session.query.assert_called_once()
        mock_query.filter.assert_called_once()
        mock_validate.assert_called_once_with(mock_app)
        
    @patch('aclimate_v3_orm_frontend.schemas.app_schema.AppRead.model_validate')
    def test_search_by_name_uses_ilike(self, mock_validate):
        """Test search_by_name uses partial matching"""
        # Arrange
        mock_validate.return_value = {"id": 1, "name": "Test App", "country_ext_id": "CO", "enable": True}
        
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value.all.return_value = []
        
        self.app_service._session_scope = MagicMock()
        self.app_service._session_scope.return_value.__enter__.return_value = mock_session
        
        # Act
        result = self.app_service.search_by_name("Test", db=self.mock_db)
        
        # Assert
        mock_session.query.assert_called_once()
        mock_query.filter.assert_called_once()
        assert isinstance(result, list)

class TestAppValidator:
    
    def test_validate_name_empty_raises_error(self):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="The 'name' field is required"):
            AppValidator.validate_name("")
    
    def test_validate_name_too_long_raises_error(self):
        """Test that name too long raises ValueError"""
        long_name = "a" * 256
        with pytest.raises(ValueError, match="App name cannot exceed 255 characters"):
            AppValidator.validate_name(long_name)
    
    def test_validate_country_ext_id_empty_raises_error(self):
        """Test that empty country_ext_id raises ValueError"""
        with pytest.raises(ValueError, match="The 'country_ext_id' field is required"):
            AppValidator.validate_country_ext_id("")
    
    def test_validate_country_ext_id_too_long_raises_error(self):
        """Test that country_ext_id too long raises ValueError"""
        long_id = "a" * 51
        with pytest.raises(ValueError, match="Country ext id cannot exceed 50 characters"):
            AppValidator.validate_country_ext_id(long_id)
    
    def test_create_validate_calls_all_validations(self):
        """Test that create_validate calls all necessary validations"""
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        app_create = AppCreate(
            name="Test App",
            country_ext_id="CO",
            enable=True
        )
        
        # Should not raise any exception
        AppValidator.create_validate(mock_db, app_create)