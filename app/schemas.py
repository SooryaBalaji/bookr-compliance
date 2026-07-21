from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class USState(str, Enum):
    ALABAMA = "Alabama"
    ALASKA = "Alaska"
    ARIZONA = "Arizona"
    ARKANSAS = "Arkansas"
    CALIFORNIA = "California"
    COLORADO = "Colorado"
    CONNECTICUT = "Connecticut"
    DELAWARE = "Delaware"
    DISTRICT_OF_COLUMBIA = "District of Columbia"
    FLORIDA = "Florida"
    GEORGIA = "Georgia"
    HAWAII = "Hawaii"
    IDAHO = "Idaho"
    ILLINOIS = "Illinois"
    INDIANA = "Indiana"
    IOWA = "Iowa"
    KANSAS = "Kansas"
    KENTUCKY = "Kentucky"
    LOUISIANA = "Louisiana"
    MAINE = "Maine"
    MARYLAND = "Maryland"
    MASSACHUSETTS = "Massachusetts"
    MICHIGAN = "Michigan"
    MINNESOTA = "Minnesota"
    MISSISSIPPI = "Mississippi"
    MISSOURI = "Missouri"
    MONTANA = "Montana"
    NEBRASKA = "Nebraska"
    NEVADA = "Nevada"
    NEW_HAMPSHIRE = "New Hampshire"
    NEW_JERSEY = "New Jersey"
    NEW_MEXICO = "New Mexico"
    NEW_YORK = "New York"
    NORTH_CAROLINA = "North Carolina"
    NORTH_DAKOTA = "North Dakota"
    OHIO = "Ohio"
    OKLAHOMA = "Oklahoma"
    OREGON = "Oregon"
    PENNSYLVANIA = "Pennsylvania"
    RHODE_ISLAND = "Rhode Island"
    SOUTH_CAROLINA = "South Carolina"
    SOUTH_DAKOTA = "South Dakota"
    TENNESSEE = "Tennessee"
    TEXAS = "Texas"
    UTAH = "Utah"
    VERMONT = "Vermont"
    VIRGINIA = "Virginia"
    WASHINGTON = "Washington"
    WEST_VIRGINIA = "West Virginia"
    WISCONSIN = "Wisconsin"
    WYOMING = "Wyoming"

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

class EntityCreate(BaseModel):
    name: str
    org_type: str
    incorporation_state: USState
    headquarters: str
    naics_code: str
    creation_template: str
    is_restricted: Optional[bool] = False

class EntityResponse(BaseModel):
    id: int
    name: str
    org_type: str
    incorporation_state: str
    headquarters: str
    naics_code: str
    is_restricted: bool
    admin_id: Optional[int] = None
    class Config:
        from_attributes = True

class AssignAdminPayload(BaseModel):
    admin_id: int

# Tasks
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
    entity_id: Optional[int] = None
    entity_name: Optional[str] = None
    entity: Optional[str] = None  # Explicitly None to prevent accidental fallback overrides
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
    entity_id: Optional[int] = None
    entity_name: Optional[str] = None
    entity: Optional[str] = None
    portal_name: Optional[str] = None
    portal_url: Optional[str] = None
    alt_note: Optional[str] = None
    info: Optional[str] = None
    class Config:
        from_attributes = True

# Compliance logs
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