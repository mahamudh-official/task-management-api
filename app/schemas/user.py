from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    email: EmailStr
    phone_number: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


