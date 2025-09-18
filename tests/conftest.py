# Test configuration file for pytest
import sys
import os
from sqlalchemy import create_engine
# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# You can add pytest fixtures here if needed
import pytest


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture
def sample_app_data():
    """Sample app data for testing"""
    return {
        "name": "Test App",
        "country_ext_id": "1",
        "enable": True
    }

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "ext_key_clock_id": "keycloak_123",
        "app_id": 1,
        "profile": "FARMER",
        "enable": True
    }

@pytest.fixture
def sample_ws_interested_data():
    """Sample ws_interested data for testing"""
    return {
        "user_id": 1,
        "ws_ext_id": "WS_123",
        "notification": {"email": True, "wp": False}
    }