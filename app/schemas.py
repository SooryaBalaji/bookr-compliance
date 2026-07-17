from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ---------- Auth / Users ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ---------- Tasks ----------

class TaskCreate(BaseModel):
    short: str
    title: str
    scope: str = "Internal"
    quarter: str = "ROLL"
    due_type: str = "fixed"
    due_month: Optional[int] = None
    due_day: Optional[int] = None
    due_text: Optional[str] = None
    target_year: Optional[int] = None
    entity: Optional[str] = "Bookr, Inc."
    portal_name: Optional[str] = None
    portal_url: Optional[str] = None
    alt_note: Optional[str] = None
    info: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    key: str
    is_core: bool
    num: Optional[int] = None
    quarter: Optional[str] = None
    scope: Optional[str] = None
    short: str
    title: str
    due_type: str
    due_month: Optional[int] = None
    due_day: Optional[int] = None
    due_text: Optional[str] = None
    target_year: Optional[int] = None
    entity: Optional[str] = None
    portal_name: Optional[str] = None
    portal_url: Optional[str] = None
    alt_note: Optional[str] = None
    info: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- Compliance logs ----------

class LogCreate(BaseModel):
    task_id: int
    fiscal_year: int
    action: str = "filed"
    date: Optional[str] = None
    cloud_link: Optional[str] = None
    note: Optional[str] = None
    file_name: Optional[str] = None
    file_data: Optional[str] = None


class LogResponse(BaseModel):
    id: int
    task_id: int
    fiscal_year: int
    action: str
    date: Optional[str] = None
    cloud_link: Optional[str] = None
    note: Optional[str] = None
    file_name: Optional[str] = None
    file_data: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True
