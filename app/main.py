import os
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import engine, Base, get_db
from app import models, schemas
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.seed_data import CORE_TASKS


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
    if payload.role not in ["admin", "member_edit", "member_read"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = payload.role
    await db.commit()
    return {"status": "success", "role": user.role}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db),
                      admin: models.User = Depends(get_current_admin)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Block deleting other admins
    if target_user.role == "admin" and target_user.id != admin.id:
        raise HTTPException(status_code=403, detail="Security Violation: Cannot delete other Admin accounts.")

    await db.delete(target_user)
    await db.commit()
    return {"status": "success", "message": "User deleted"}

# NAICS Onboarding Engine (Hybrid Detection)
class OnboardPayload(BaseModel):
    naics_code: str
    org_type: str


@app.post("/system/onboard")
async def system_onboard(payload: OnboardPayload, db: AsyncSession = Depends(get_db),
                         admin: models.User = Depends(get_current_admin)):
    await db.execute(text("DELETE FROM tasks"))
    tasks_to_seed = []

    # Priority given to explicit dropdown type
    if payload.org_type == "bookr" or payload.naics_code == "541511":
        tasks_to_seed = CORE_TASKS
    elif payload.org_type == "non-profit":
        tasks_to_seed = [
            {"key": "990", "is_core": True, "deleted": False, "num": 1, "quarter": "Q2", "scope": "Federal",
             "short": "Form 990", "title": "Return of Organization Exempt from Income Tax", "due_type": "fixed",
             "due_month": 5, "due_day": 15, "due_text": "May 15", "entity": "Generic Org",
             "info": "Annual IRS filing for tax-exempt organizations."},
            {"key": "charity", "is_core": True, "deleted": False, "num": 2, "quarter": "ROLL", "scope": "State",
             "short": "AG Reg", "title": "Attorney General Charitable Solicitation", "due_type": "rolling",
             "due_month": None, "due_day": None, "due_text": "Annually", "entity": "Generic Org",
             "info": "Required to legally ask for donations in the state."},
        ]
    else:
        tasks_to_seed = [
            {"key": "1120", "is_core": True, "deleted": False, "num": 1, "quarter": "Q1", "scope": "Federal",
             "short": "Form 1120", "title": "U.S. Corporation Income Tax Return", "due_type": "fixed", "due_month": 4,
             "due_day": 15, "due_text": "April 15", "entity": "Generic Org", "info": "Standard corporate tax return."},
            {"key": "soi", "is_core": True, "deleted": False, "num": 2, "quarter": "ROLL", "scope": "State",
             "short": "State AR", "title": "Annual Report / Statement of Information", "due_type": "rolling",
             "due_month": None, "due_day": None, "due_text": "Annually", "entity": "Generic Org",
             "info": "State required business entity renewal."},
        ]

    for t in tasks_to_seed:
        db.add(models.Task(**t))
    await db.commit()
    return {"status": "success", "seeded": len(tasks_to_seed)}

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