from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Identity and Access Management
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True) # e.g., "Admin", "Manager", "Auditor"

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True) # e.g., "task:delete", "report:generate"

class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")

class UserOverride(Base):
    __tablename__ = "user_overrides"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    effect = Column(Boolean) # True = Grant, False = Revoke

# Core Compliance Engine
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String) # e.g., "Pending", "Executed"
    due_date = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String) # e.g., "TASK_EXECUTED", "HISTORY_WIPED"
    target_id = Column(Integer) # ID of the object changed
    details = Column(Text)