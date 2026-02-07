from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass
    
class UserInDBBase(UserBase):
    id: UUID4
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    pass
