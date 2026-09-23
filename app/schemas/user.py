from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    email: EmailStr
    phone_number: str = Field(min_length=10, max_length=20)
    password: str = Field(min_length=8, max_length=128)

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


