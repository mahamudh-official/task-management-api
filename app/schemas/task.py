from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=5000)
    due_date: datetime

    @field_validator("title", "description")
    @classmethod
    def validate_title(cls, value: str, info)-> str:
        value = value.strip()
        if not value:
            raise ValueError(f"{info.field_name} cannot be empty or whitespace.")
        return value

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value: datetime) -> datetime:

        now = datetime.now(timezone.utc)

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        if value < now:
            raise ValueError("Due date cannot be in the past.")
        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    user_id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes= True)

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    due_date: datetime | None = None
    is_completed: bool | None = None

    @field_validator("title", "description")
    @classmethod
    def validate_title(cls, value: str | None, info) -> str | None:
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError(f"{info.field_name} cannot be empty or whitespace.")
        return value


    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value: datetime | None) -> datetime | None:

        if value is None:
            return value

        now = datetime.now(timezone.utc)

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        if value < now:
            raise ValueError("Due date cannot be in the past.")
        return value

class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    limit: int
    total_pages: int