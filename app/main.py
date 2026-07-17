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

from app.database import engine, Base, get_db
from app import models, schemas
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.seed_data import CORE_TASKS


async def seed_core_tasks(db: AsyncSession):
    """Idempotently insert the ~32 built-in filings on first boot.
    Safe to call on every startup: existing rows (matched by `key`) are left alone."""
    result = await db.execute(select(models.Task.key).where(models.Task.is_core == True))  # noqa: E712
    existing_keys = {row[0] for row in result.all()}

    for t in CORE_TASKS:
        if t["key"] in existing_keys:
            continue
        db.add(models.Task(is_core=True, deleted=False, **t))
    await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        await seed_core_tasks(session)
    yield
    await engine.dispose()


app = FastAPI(
    title="Bookr Compliance API",
    description="Regulatory compliance and automated corporate filing tracker",
    version="2.0.0",
    lifespan=lifespan,
)

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
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "API is live, but index.html was not found in app/static."}


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable, please check back later")


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@app.post("/auth/register", response_model=schemas.Token)
async def register(payload: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(models.User).where(models.User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="An account with that email already exists")

    # The very first person to register becomes admin; everyone after is a regular member.
    count_result = await db.execute(select(models.User.id))
    is_first_user = len(count_result.all()) == 0

    user = models.User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role="admin" if is_first_user else "member",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(subject=user.email)
    return schemas.Token(access_token=token, user=user)


@app.post("/auth/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.email)
    return schemas.Token(access_token=token, user=user)


@app.get("/auth/me", response_model=schemas.UserResponse)
async def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

@app.get("/tasks/", response_model=List[schemas.TaskResponse])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Task).where(models.Task.deleted == False))  # noqa: E712
    return result.scalars().all()


@app.post("/tasks/", response_model=schemas.TaskResponse)
async def create_task(
    payload: schemas.TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    key = f"cust_{int(__import__('time').time() * 1000)}"
    count_result = await db.execute(select(models.Task.id))
    next_num = len(count_result.all()) + 1

    task = models.Task(
        key=key,
        is_core=False,
        deleted=False,
        num=next_num,
        created_by=current_user.id,
        **payload.model_dump(),
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Soft delete so core seed rows and audit history survive; also drop its logs,
    # matching the original app's "permanently delete" behavior.
    task.deleted = True
    log_result = await db.execute(select(models.ComplianceLog).where(models.ComplianceLog.task_id == task_id))
    for log in log_result.scalars().all():
        await db.delete(log)
    await db.commit()
    return {"status": "success", "message": "Task deleted"}


# ---------------------------------------------------------------------------
# Compliance logs
# ---------------------------------------------------------------------------

@app.get("/logs/", response_model=List[schemas.LogResponse])
async def list_logs(
    task_id: Optional[int] = None,
    fiscal_year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = select(models.ComplianceLog)
    if task_id is not None:
        query = query.where(models.ComplianceLog.task_id == task_id)
    if fiscal_year is not None:
        query = query.where(models.ComplianceLog.fiscal_year == fiscal_year)
    query = query.order_by(models.ComplianceLog.timestamp.asc())
    result = await db.execute(query)
    return result.scalars().all()


@app.post("/logs/", response_model=schemas.LogResponse)
async def create_log(
    payload: schemas.LogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    task_result = await db.execute(select(models.Task).where(models.Task.id == payload.task_id))
    if task_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Task not found")

    log = models.ComplianceLog(actor_id=current_user.id, **payload.model_dump())
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@app.delete("/logs/{log_id}")
async def delete_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.ComplianceLog).where(models.ComplianceLog.id == log_id))
    log = result.scalar_one_or_none()
    if log is None:
        raise HTTPException(status_code=404, detail="Log entry not found")
    await db.delete(log)
    await db.commit()
    return {"status": "success"}


@app.delete("/logs/")
async def bulk_delete_logs(
    task_id: Optional[int] = None,
    fiscal_year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Powers 'Reset current year to pending', 'Wipe history for this task',
    and 'Clear entire audit registry' from the UI."""
    query = select(models.ComplianceLog)
    if task_id is not None:
        query = query.where(models.ComplianceLog.task_id == task_id)
    if fiscal_year is not None:
        query = query.where(models.ComplianceLog.fiscal_year == fiscal_year)
    result = await db.execute(query)
    logs = result.scalars().all()
    for log in logs:
        await db.delete(log)
    await db.commit()
    return {"status": "success", "deleted": len(logs)}
