from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="viewer")  # "super_admin", "co_admin", "editor", "viewer"
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    memberships = relationship("EntityMember", back_populates="user", cascade="all, delete-orphan")


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    org_type = Column(String, nullable=False)  # C-Corp, LLC, Non-Profit, etc.
    incorporation_state = Column(String, nullable=False)
    headquarters = Column(String, nullable=False)
    naics_code = Column(String, nullable=False)

    # Security Flag: Restricts visibility & modifications strictly to Super Admins
    is_restricted = Column(Boolean, default=False, nullable=False)

    members = relationship("EntityMember", back_populates="entity", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="assigned_entity", cascade="all, delete-orphan")


class EntityMember(Base):
    __tablename__ = "entity_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)

    # Ensures a user isn't assigned to the same organization twice
    __table_args__ = (UniqueConstraint('user_id', 'entity_id', name='_user_entity_uc'),)

    user = relationship("User", back_populates="memberships")
    entity = relationship("Entity", back_populates="members")


class OrgSettings(Base):
    # Legacy singleton for fallback if needed
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

    # SET NULL prevents cascading deletes if the employee who created this task is removed
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    logs = relationship("ComplianceLog", back_populates="task", cascade="all, delete-orphan")
    assigned_entity = relationship("Entity", back_populates="tasks")


class ComplianceLog(Base):
    __tablename__ = "compliance_logs"

    # Prevents duplicate submissions for the exact same task in the exact same fiscal year
    __table_args__ = (UniqueConstraint('task_id', 'fiscal_year', name='_task_fiscal_year_uc'),)

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    action = Column(String, default="filed")

    date = Column(String, nullable=True)
    cloud_link = Column(String, nullable=True)
    note = Column(Text, nullable=True)
    file_name = Column(String, nullable=True)
    file_data = Column(Text, nullable=True)  # Stores URL paths instead of heavy Base64 strings

    # SET NULL preserves vital legal compliance history even if the employee account is deleted
    actor_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    task = relationship("Task", back_populates="logs")
