from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class WsInterestedBase(BaseModel):
    user_id: int = Field(..., gt=0, description="Associated User ID")
    ws_ext_id: str = Field(..., max_length=50, description="External weather station ID")
    notification: dict = Field(..., description="Notification settings as JSON")

class WsInterestedCreate(BaseModel):
    user_id: int = Field(..., gt=0, description="Associated User ID")
    ws_ext_id: str = Field(..., max_length=50, description="External weather station ID")
    notification: dict = Field(..., description="Notification settings as JSON")

class WsInterestedUpdate(BaseModel):
    user_id: Optional[int] = Field(None, gt=0)
    ws_ext_id: Optional[str] = Field(None, max_length=50)
    notification: Optional[dict] = None

class WsInterestedRead(WsInterestedBase):
    id: int
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
