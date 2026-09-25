from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    
    title: str
    description: str
    due_date: datetime

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
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    is_completed: bool | None = None