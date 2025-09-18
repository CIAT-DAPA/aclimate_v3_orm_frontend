from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class AppBase(BaseModel):
    name: str = Field(..., max_length=255, description="App name")
    country_ext_id: str = Field(..., max_length=50, description="External country id")
    enable: bool = Field(default=True, description="Whether the source is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class AppCreate(BaseModel):
    name: str = Field(..., max_length=255)
    country_ext_id: str = Field(..., max_length=50)
    enable: bool = Field(default=True)

class AppUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    country_ext_id: Optional[str] = Field(None, max_length=50)
    enable: Optional[bool] = None

class AppRead(AppBase):
    id: int
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
