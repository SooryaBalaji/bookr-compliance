from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="member_read")  # "admin", "member_edit", "member_read"
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # 1-to-1 relationship mapping back to the entity they manage
    managed_entity = relationship("Entity", back_populates="admin_user", uselist=False)


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    org_type = Column(String, nullable=False)  # C-Corp, LLC, Non-Profit, etc.
    incorporation_state = Column(String, nullable=False)
    headquarters = Column(String, nullable=False)
    naics_code = Column(String, nullable=False)

    # Enforcing strict 1-to-1 admin assignment
    admin_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)

    admin_user = relationship("User", back_populates="managed_entity")
    tasks = relationship("Task", back_populates="assigned_entity", cascade="all, delete-orphan")


class OrgSettings(Base):
    """Legacy singleton for fallback if needed."""
    __tablename__ = "org_settings"

    id = Column(Integer, primary_key=True, default=1)
    naics_code = Column(String, nullable=False)
    org_type = Column(String, nullable=False)
    detected_type = Column(String, nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    is_core = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    num = Column(Integer, nullable=True)
    quarter = Column(String, nullable=True)
    scope = Column(String, nullable=True)
    short = Column(String, nullable=False)
    title = Column(String, nullable=False)

    due_type = Column(String, nullable=False, default="fixed")
    due_month = Column(Integer, nullable=True)
    due_day = Column(Integer, nullable=True)
    due_text = Column(String, nullable=True)
    target_year = Column(Integer, nullable=True)

    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=True)
    entity_name = Column(String, nullable=True)
    entity = Column(String, nullable=True)  # Legacy fallback

    portal_name = Column(String, nullable=True)
    portal_url = Column(String, nullable=True)
    alt_note = Column(Text, nullable=True)
    info = Column(Text, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    logs = relationship("ComplianceLog", back_populates="task", cascade="all, delete-orphan")
    assigned_entity = relationship("Entity", back_populates="tasks")


class ComplianceLog(Base):
    __tablename__ = "compliance_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    action = Column(String, default="filed")

    date = Column(String, nullable=True)
    cloud_link = Column(String, nullable=True)
    note = Column(Text, nullable=True)
    file_name = Column(String, nullable=True)
    file_data = Column(Text, nullable=True)

    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    task = relationship("Task", back_populates="logs")