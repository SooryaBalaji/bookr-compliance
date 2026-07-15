from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Task schemas
class TaskBase(BaseModel):
    title: str = Field(..., example="California Statement of Information")
    status: str = Field(..., example="Pending")
    description: str = Field(..., example="Details about the filing...")
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    # Schema for creating a new task from the front end
    pass

class TaskResponse(TaskBase):
    #Schema for sending task data back to the frontend
    id: int
    owner_id: Optional[int] = None

    class Config:
        # This tells Pydantic to read data directly from the SQLAlchemy ORM model
        from_attributes = True

# Audit Log Schemas
class AuditLogResponse(BaseModel):
    id: int
    timestamp: datetime
    action: str
    target_id: Optional[int]
    details: Optional[str]

    class Config:
        from_attributes = True