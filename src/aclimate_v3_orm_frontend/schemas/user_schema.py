from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from ..enums.profile_type import ProfileType

class UserBase(BaseModel):
    ext_key_clock_id: str = Field(..., max_length=255, description="External Keycloak ID")
    app_id: int = Field(..., gt=0, description="Associated App ID")
    profile: ProfileType = Field(..., description="User profile type")
    enable: bool = Field(default=True, description="Whether the source is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class UserCreate(BaseModel):
    ext_key_clock_id: str = Field(..., max_length=255, description="External Keycloak ID")
    app_id: int = Field(..., gt=0, description="Associated App ID")
    profile: ProfileType = Field(..., description="User profile type")
    enable: bool = Field(default=True, description="Whether the source is enabled")

class UserUpdate(BaseModel):
    ext_key_clock_id: Optional[str] = Field(None, max_length=255)
    app_id: Optional[int] = Field(None, gt=0)
    profile: Optional[ProfileType] = None
    enable: Optional[bool] = None

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
