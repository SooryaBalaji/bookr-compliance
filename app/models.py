from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class User(Base):
    """A person who can log into the compliance tracker."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="member")  # "admin" or "member"
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class OrgSettings(Base):
    """
    Singleton row (id is always 1) holding the org-wide NAICS classification
    chosen during onboarding. Used so the app remembers which task template
    (Bookr / non-profit / for-profit) is active and can show/re-run it later.
    """
    __tablename__ = "org_settings"

    id = Column(Integer, primary_key=True, default=1)
    naics_code = Column(String, nullable=False)
    org_type = Column(String, nullable=False)  # 'bookr' | 'non-profit' | 'for-profit'
    detected_type = Column(String, nullable=True)  # what the server inferred from naics_code alone
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))


class Task(Base):
    """
    A single compliance milestone/filing. This covers both the ~32 seeded
    "core" filings (federal/state/insurance forms) and any custom milestones
    a user adds later. is_core distinguishes the two; deleted is a soft-delete
    flag so core tasks can be hidden without losing their seed row.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)  # stable slug, e.g. '1099nec' or 'cust_...'
    is_core = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    num = Column(Integer, nullable=True)
    quarter = Column(String, nullable=True)  # Q1/Q2/Q3/Q4/ROLL/INSURANCE
    scope = Column(String, nullable=True)    # Federal/California/Delaware/Internal/Insurance
    short = Column(String, nullable=False)
    title = Column(String, nullable=False)

    due_type = Column(String, nullable=False, default="fixed")  # 'fixed' or 'rolling'
    due_month = Column(Integer, nullable=True)
    due_day = Column(Integer, nullable=True)
    due_text = Column(String, nullable=True)
    target_year = Column(Integer, nullable=True)  # only set for custom one-off tasks

    entity = Column(String, nullable=True)
    portal_name = Column(String, nullable=True)
    portal_url = Column(String, nullable=True)
    alt_note = Column(Text, nullable=True)
    info = Column(Text, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    logs = relationship("ComplianceLog", back_populates="task", cascade="all, delete-orphan")


class ComplianceLog(Base):
    """An execution/filing record logged against a task for a given fiscal year."""
    __tablename__ = "compliance_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    action = Column(String, default="filed")  # currently only 'filed' is used by the UI

    date = Column(String, nullable=True)        # date executed, as entered by the user (YYYY-MM-DD)
    cloud_link = Column(String, nullable=True)
    note = Column(Text, nullable=True)
    file_name = Column(String, nullable=True)
    file_data = Column(Text, nullable=True)      # base64 data URL of an uploaded proof document

    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    task = relationship("Task", back_populates="logs")
