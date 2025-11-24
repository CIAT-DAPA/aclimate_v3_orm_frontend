# AClimate V3 ORM Frontend ⛅️💾

## 🏷️ Version & Tags

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CIAT-DAPA/aclimate_v3_orm_frontend) ![](https://img.shields.io/github/v/tag/CIAT-DAPA/aclimate_v3_orm_frontend)

## 📌 Introduction

AClimate V3 ORM Frontend is an Object-Relational Mapping package designed for the AClimate platform's frontend services. It facilitates interaction with relational databases for user management, application configuration, and weather station interest tracking. The package provides a structured interface for managing frontend-specific data including user profiles, app configurations, and notification preferences.

This is an ORM (Object-Relational Mapping) built with the SQLAlchemy library for interfacing with relational databases, specifically designed for frontend application needs.

## Documentation

For complete documentation, visit the [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/CIAT-DAPA/aclimate_v3_orm_frontend)

## Features

- Modular structure organized by domain (user management, app configuration, notifications)
- Built using SQLAlchemy for efficient relational mapping
- Pydantic schemas for data validation and serialization
- Service layer pattern with comprehensive validation
- Enum support for type-safe profile management
- JSON column support for flexible notification configurations
- Compatible with Python > 3.10
- Designed for integration into AClimate frontend infrastructure

## ✅ Requirements

- Python > 3.10
- Relational database (PostgreSQL recommended, also compatible with MySQL and SQLite)
- Dependencies: SQLAlchemy, pydantic, typing_extensions

# Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/CIAT-DAPA/aclimate_v3_orm_frontend
```

To install a specific version:

```bash
pip install git+https://github.com/CIAT-DAPA/aclimate_v3_orm_frontend@v0.0.1
```

## 🔧 Environment Configuration

You can configure the database connection either by:

1. Creating a `.env` file in your project root, OR
2. Setting environment variables directly in your system

### Option 1: Using .env file

Create a file named `.env` with these configurations:

#### PostgreSQL

```ini
DATABASE_URL_FRONT=postgresql://username:password@localhost:5432/database
```

### Option 2: Setting Environment Variables

- Windows (CMD/PowerShell)

```bash
set DATABASE_URL_FRONT=postgresql://username:password@localhost:5432/database
```

- Linux/Ubuntu (Terminal)

```bash
export DATABASE_URL_FRONT="postgresql://username:password@localhost:5432/database"
```

> [!NOTE]  
> Replace username, password and localhost with your actual credentials

## 🚀 Usage

### Import

Examples

```python
# Models
from aclimate_v3_orm_frontend.models import (
    App,
    User,
    WsInterested
)

# Services
from aclimate_v3_orm_frontend.services import (
    AppService,
    UserService,
    WsInterestedService
)

# Schemas
from aclimate_v3_orm_frontend.schemas import (
    AppCreate, AppRead, AppUpdate,
    UserCreate, UserRead, UserUpdate,
    WsInterestedCreate, WsInterestedRead, WsInterestedUpdate
)

# Enums
from aclimate_v3_orm_frontend.enums import ProfileType
```

### Using

```python
# Init services
app_service = AppService()
user_service = UserService()
ws_service = WsInterestedService()

# Create new app
new_app = AppCreate(
    name="AClimate Colombia",
    country_ext_id="1",
    enable=True
)

app = app_service.create(obj_in=new_app)
print(app)

# Create new user
new_user = UserCreate(
    ext_key_clock_id="keycloak_user_123",
    app_id=app.id,
    profile=ProfileType.FARMER,
    enable=True
)

user = user_service.create(obj_in=new_user)
print(user)

# Create weather station interest
new_ws_interest = WsInterestedCreate(
    user_id=user.id,
    ws_ext_id="1",
    notification={"email": True, "sms": False, "push": True}
)

ws_interest = ws_service.create(obj_in=new_ws_interest)
print(ws_interest)

# Get data
apps = app_service.get_all()
users_by_app = user_service.get_by_app(app.id)
user_interests = ws_service.get_by_user(user.id)

print(f"Total apps: {len(apps)}")
print(f"Users in app: {len(users_by_app)}")
print(f"User interests: {len(user_interests)}")
```

## 🧪 Testing

### Test Structure

The test suite is organized to validate all service components:

```bash
tests/
├── conftest.py           # Test configuration and fixtures
├── test_app.py          # App service and validator tests
├── test_user.py         # User service and validator tests
├── test_ws_interested.py # Weather station interest tests
└── test_enums.py        # Enum functionality tests
```

### Example Test Execution

```bash
# Set up environment
python -m venv env
source env/bin/activate  # Linux/Mac
# or
env\Scripts\activate     # Windows

# Install test dependencies
pip install pytest pytest-mock pytest-cov

# Run all tests (Linux/Mac)
PYTHONPATH=$PYTHONPATH:./src pytest tests/

# Run all tests (Windows PowerShell)
set PYTHONPATH=%PYTHONPATH%;./src && pytest tests/

# Specific test examples:
pytest tests/test_app.py -v              # Run app tests
pytest tests/test_user.py -v             # Run user tests
pytest tests/test_ws_interested.py -v    # Run weather station tests
pytest -k "test_create"                  # Run tests matching pattern
pytest --cov=src tests/                  # Run with coverage
```

> [!NOTE]  
> All tests use an isolated SQLite in-memory database configured in conftest.py, ensuring test independence and execution speed.

## 🔄 CI/CD Pipeline Overview

### Workflow Architecture

Our GitHub Actions pipeline implements a three-stage deployment process:

```bash
Code Push → Test Stage → Merge Stage → Release Stage
```

## 📊 Project Structure

```bash
aclimate_v3_orm_frontend/
│
├── .github/
│   └── workflows/              # CI/CD pipeline configurations
│
├── src/
│   └── aclimate_v3_orm_frontend/
│       ├── models/             # SQLAlchemy ORM models
│       │   ├── __init__.py
│       │   ├── app.py          # App model with country association
│       │   ├── user.py         # User model with Keycloak integration
│       │   └── ws_interested.py # Weather station interest tracking
│       │
│       ├── schemas/            # Pydantic schemas for validation
│       │   ├── __init__.py
│       │   ├── app_schema.py   # App CRUD schemas
│       │   ├── user_schema.py  # User CRUD schemas
│       │   └── ws_interested_schema.py # WS interest schemas
│       │
│       ├── services/           # Service layer for business logic
│       │   ├── __init__.py
│       │   ├── base_service.py # Generic base service class
│       │   ├── app_service.py  # App-specific operations
│       │   ├── user_service.py # User management operations
│       │   └── ws_interested_service.py # Weather station operations
│       │
│       ├── validations/        # Business validation logic
│       │   ├── __init__.py
│       │   ├── app_validator.py # App validation rules
│       │   ├── user_validator.py # User validation rules
│       │   └── ws_interested_validator.py # WS validation rules
│       │
│       ├── enums/              # Type-safe enumerations
│       │   ├── __init__.py
│       │   └── profile_type.py # User profile types (FARMER, TECHNICIAN)
│       │
│       ├── database/           # Database connection management
│       │   ├── __init__.py
│       │   └── base.py         # SQLAlchemy base configuration
│       │
│       └── __init__.py
│
├── tests/                      # Test suite organized by service
│   ├── conftest.py            # Test configuration and fixtures
│   ├── test_app.py            # App service tests
│   ├── test_user.py           # User service tests
│   ├── test_ws_interested.py  # Weather station tests
│   └── test_enums.py          # Enum functionality tests
│
├── pyproject.toml             # Package configuration
├── requirements.txt           # Package dependencies
└── README.md                  # This documentation
```

## 🔗 Database Schema

### Entity Relationships

```
┌─────────────┐    ┌─────────────┐    ┌─────────────────┐
│     App     │    │    User     │    │  WsInterested   │
├─────────────┤    ├─────────────┤    ├─────────────────┤
│ id (PK)     │◄──┐│ id (PK)     │◄──┐│ id (PK)         │
│ name        │   └│ app_id (FK) │   └│ user_id (FK)    │
│ country_    │    │ ext_key_    │    │ ws_ext_id       │
│ ext_id      │    │ clock_id    │    │ notification    │
│ enable      │    │ profile     │    │ (JSON)          │
│ register    │    │ enable      │    └─────────────────┘
│ updated     │    │ register    │
└─────────────┘    │ updated     │
                   └─────────────┘
```

### Key Features:

- **App**: Application configurations per country
- **User**: User management with Keycloak integration and profile types
- **WsInterested**: Flexible notification preferences stored as JSON
- **ProfileType Enum**: Type-safe user classification (FARMER, TECHNICIAN)

## 🛠️ Development

### Adding New Models

1. Create model in `src/aclimate_v3_orm_frontend/models/`
2. Define Pydantic schemas in `src/aclimate_v3_orm_frontend/schemas/`
3. Implement service in `src/aclimate_v3_orm_frontend/services/`
4. Add validation logic in `src/aclimate_v3_orm_frontend/validations/`
5. Create comprehensive tests in `tests/`
