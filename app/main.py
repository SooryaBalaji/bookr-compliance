import os
import re
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.database import engine, Base, get_db
from app import models, schemas
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.seed_data import CORE_TASKS, NON_PROFIT_TASKS, FOR_PROFIT_TASKS

# Valid account roles. "admin" = co-admin/full access, "member_edit" = can
# log/create tasks but not manage users, "member_read" = read-only.
VALID_ROLES = ["admin", "member_edit", "member_read"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Bookr Compliance API", version="2.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def serve_dashboard():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


# ---------------------------------------------------------------------------
# RBAC Dependencies
# ---------------------------------------------------------------------------
async def get_current_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


async def get_current_editor(current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["admin", "member_edit"]:
        raise HTTPException(status_code=403, detail="Editor privileges required")
    return current_user

# Auth & User Management
@app.post("/auth/register", response_model=schemas.Token)
async def register(payload: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(models.User).where(models.User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")

    count_result = await db.execute(select(models.User.id))
    is_first = len(count_result.all()) == 0

    user = models.User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role="admin" if is_first else "member_read",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return schemas.Token(access_token=create_access_token(subject=user.email), user=user)


@app.post("/auth/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return schemas.Token(access_token=create_access_token(subject=user.email), user=user)


@app.get("/auth/me", response_model=schemas.UserResponse)
async def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/users/", response_model=List[schemas.UserResponse])
async def list_users(db: AsyncSession = Depends(get_db), admin: models.User = Depends(get_current_admin)):
    result = await db.execute(select(models.User))
    return result.scalars().all()


class RoleUpdate(BaseModel):
    role: str


@app.patch("/users/{user_id}/role")
async def update_user_role(user_id: int, payload: RoleUpdate, db: AsyncSession = Depends(get_db),
                           admin: models.User = Depends(get_current_admin)):
    if payload.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Guard against orphaning the org with zero admins.
    if user.role == "admin" and payload.role != "admin":
        admin_count_result = await db.execute(select(models.User.id).where(models.User.role == "admin"))
        if len(admin_count_result.all()) <= 1:
            raise HTTPException(status_code=403, detail="Cannot demote the last remaining Co-Admin.")

    user.role = payload.role
    await db.commit()
    return {"status": "success", "role": user.role}


class AdminUserCreate(BaseModel):
    """Lets an admin directly provision a new account with a chosen role,
    instead of waiting for the person to self-register and then be promoted."""
    email: str
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    role: str = "member_read"


@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(payload: AdminUserCreate, db: AsyncSession = Depends(get_db),
                      admin: models.User = Depends(get_current_admin)):
    if payload.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")

    existing = await db.execute(select(models.User).where(models.User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = models.User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db),
                      admin: models.User = Depends(get_current_admin)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Block deleting other Co-Admin accounts outright.
    if target_user.role == "admin" and target_user.id != admin.id:
        raise HTTPException(status_code=403, detail="Security Violation: Cannot delete other Admin accounts.")

    # Even deleting yourself shouldn't be able to leave the org with zero admins.
    if target_user.role == "admin":
        admin_count_result = await db.execute(select(models.User.id).where(models.User.role == "admin"))
        if len(admin_count_result.all()) <= 1:
            raise HTTPException(status_code=403, detail="Cannot delete the last remaining Co-Admin.")

    await db.delete(target_user)
    await db.commit()
    return {"status": "success", "message": "User deleted"}

# NAICS Onboarding Engine
# ---------------------------------------------------------------------------
# Classification is driven by the NAICS code itself, not by whatever the
# client happens to have selected in a dropdown. org_type, if supplied, is
# treated as an explicit override of the server's detection (e.g. the user
# confirms/corrects the auto-detected value in the UI) — but it still has to
# be one of the three valid values, and the code must be a real 6-digit
# NAICS code either way.
NAICS_CODE_RE = re.compile(r"^\d{6}$")
BOOKR_NAICS_CODE = "541511"  # Custom Computer Programming Services — Bookr's actual code
VALID_ORG_TYPES = ["bookr", "non-profit", "for-profit"]


def classify_naics(naics_code: str) -> str:
    """Server-side source of truth for NAICS -> org type detection."""
    if naics_code == BOOKR_NAICS_CODE:
        return "bookr"
    # NAICS 813xxx = Religious, Grantmaking, Civic, Professional & Similar
    # Organizations — the sector that covers most 501(c)(3) non-profits.
    if naics_code.startswith("813"):
        return "non-profit"
    return "for-profit"


class OnboardPayload(BaseModel):
    naics_code: str
    org_type: Optional[str] = None  # optional manual override of the detected type


@app.post("/system/onboard")
async def system_onboard(payload: OnboardPayload, db: AsyncSession = Depends(get_db),
                         admin: models.User = Depends(get_current_admin)):
    naics_code = payload.naics_code.strip()
    if not NAICS_CODE_RE.match(naics_code):
        raise HTTPException(status_code=400, detail="NAICS code must be exactly 6 digits.")

    detected_type = classify_naics(naics_code)

    final_type = payload.org_type or detected_type
    if final_type not in VALID_ORG_TYPES:
        raise HTTPException(status_code=400, detail="org_type must be one of: bookr, non-profit, for-profit.")

    # 1. Clear existing tasks (and any logs against them) for the fresh start.
    await db.execute(text("DELETE FROM compliance_logs"))
    await db.execute(text("DELETE FROM tasks"))

    # 2. Template router — each branch is a fully-formed, independent list.
    if final_type == "bookr":
        template = CORE_TASKS
    elif final_type == "non-profit":
        template = NON_PROFIT_TASKS
    else:
        template = FOR_PROFIT_TASKS

    for t in template:
        db.add(models.Task(is_core=True, deleted=False, **t))

    # 3. Persist the org's classification (singleton row) so the app remembers
    #    it and the admin panel can show/re-run it later.
    existing_settings = await db.execute(select(models.OrgSettings).where(models.OrgSettings.id == 1))
    settings = existing_settings.scalar_one_or_none()
    if settings:
        settings.naics_code = naics_code
        settings.org_type = final_type
        settings.detected_type = detected_type
        settings.updated_by = admin.id
    else:
        db.add(models.OrgSettings(
            id=1, naics_code=naics_code, org_type=final_type,
            detected_type=detected_type, updated_by=admin.id,
        ))

    await db.commit()
    return {
        "status": "success",
        "naics_code": naics_code,
        "detected_type": detected_type,
        "org_type": final_type,
        "seeded": len(template),
    }


@app.get("/system/org")
async def get_org_settings(db: AsyncSession = Depends(get_db),
                           current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.OrgSettings).where(models.OrgSettings.id == 1))
    settings = result.scalar_one_or_none()
    if not settings:
        return None
    return {
        "naics_code": settings.naics_code,
        "org_type": settings.org_type,
        "detected_type": settings.detected_type,
        "updated_at": settings.updated_at,
    }

# Tasks & Logs (Protected)
@app.get("/tasks/", response_model=List[schemas.TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Task).where(models.Task.deleted == False))
    return result.scalars().all()


@app.post("/tasks/", response_model=schemas.TaskResponse)
async def create_task(payload: schemas.TaskCreate, db: AsyncSession = Depends(get_db),
                      editor: models.User = Depends(get_current_editor)):
    key = f"cust_{int(__import__('time').time() * 1000)}"
    count_result = await db.execute(select(models.Task.id))
    next_num = len(count_result.all()) + 1
    task = models.Task(key=key, is_core=False, deleted=False, num=next_num, created_by=editor.id,
                       **payload.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db),
                      admin: models.User = Depends(get_current_admin)):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if task:
        task.deleted = True
        log_result = await db.execute(select(models.ComplianceLog).where(models.ComplianceLog.task_id == task_id))
        for log in log_result.scalars().all():
            await db.delete(log)
        await db.commit()
    return {"status": "success"}


@app.get("/logs/", response_model=List[schemas.LogResponse])
async def list_logs(task_id: Optional[int] = None, fiscal_year: Optional[int] = None,
                    db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = select(models.ComplianceLog)
    if task_id: query = query.where(models.ComplianceLog.task_id == task_id)
    if fiscal_year: query = query.where(models.ComplianceLog.fiscal_year == fiscal_year)
    result = await db.execute(query.order_by(models.ComplianceLog.timestamp.asc()))
    return result.scalars().all()


@app.post("/logs/", response_model=schemas.LogResponse)
async def create_log(payload: schemas.LogCreate, db: AsyncSession = Depends(get_db),
                     editor: models.User = Depends(get_current_editor)):
    log = models.ComplianceLog(actor_id=editor.id, **payload.model_dump())
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@app.delete("/logs/{log_id}")
async def delete_log(log_id: int, db: AsyncSession = Depends(get_db), admin: models.User = Depends(get_current_admin)):
    result = await db.execute(select(models.ComplianceLog).where(models.ComplianceLog.id == log_id))
    if log := result.scalar_one_or_none():
        await db.delete(log)
        await db.commit()
    return {"status": "success"}