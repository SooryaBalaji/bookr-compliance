import os
import base64
import uuid
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field

from app.database import engine, Base, get_db
from app import models, schemas
from app.auth import hash_password, verify_password, create_access_token, get_current_user

from app.seed_data import (
    CORE_TASKS,
    CA_FOR_PROFIT_TASKS,
    DELAWARE_CCORP_TASKS,
    PEBBLE_TASKS,
    NON_PROFIT_TASKS,
    GENERAL_LLC_TASKS
)

VALID_ROLES = ["super_admin", "co_admin", "editor", "viewer"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Bookr Compliance API", version="2.5.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

# Mount static frontend
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Mount dynamic uploads directory for Base64 extracted files
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


class TaskUpdate(BaseModel):
    due_type: str
    due_month: Optional[int] = None
    due_day: Optional[int] = None
    due_text: str


@app.get("/")
async def serve_dashboard():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


# RBAC Dependencies & Verification
async def get_current_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "co_admin"]:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


async def get_current_editor(current_user: models.User = Depends(get_current_user)):
    if current_user.role == "viewer":
        raise HTTPException(status_code=403, detail="Editor write privileges required")
    return current_user


async def verify_org_access(db: AsyncSession, user: models.User, entity_id: int):
    """Verifies that the user has been granted access to this specific organization."""
    if user.role == "super_admin":
        return True
    res = await db.execute(select(models.EntityMember).where(
        models.EntityMember.user_id == user.id, models.EntityMember.entity_id == entity_id
    ))
    if not res.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Cross-organization security violation blocked.")
    return True


# Auth & User Management
@app.post("/auth/register")
async def register(payload: schemas.UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(models.User).where(models.User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")

    count_result = await db.execute(select(models.User.id))
    is_first = len(count_result.all()) == 0

    if not is_first:
        raise HTTPException(status_code=403, detail="Public registration disabled. Contact a Bookr Super Admin.")

    user = models.User(email=payload.email, full_name=payload.full_name, password_hash=hash_password(payload.password),
                       role="super_admin")
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(subject=user.email)
    response.set_cookie(
        key="bookr_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 24 * 7 * 60  # 7 days
    )
    return {"status": "success", "user": user.email}


@app.post("/auth/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(subject=user.email)
    response.set_cookie(
        key="bookr_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 24 * 7 * 60  # 7 days
    )
    return {"status": "success", "user": user.email}


@app.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(key="bookr_token", httponly=True, secure=True, samesite="lax")
    return {"status": "success"}


class EmergencyResetPayload(BaseModel):
    email: str
    new_password: str
    master_key: str


@app.post("/auth/emergency-reset")
async def emergency_password_reset(payload: EmergencyResetPayload, db: AsyncSession = Depends(get_db)):
    expected_key = os.getenv("MASTER_RESET_KEY")
    if not expected_key or payload.master_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid or disabled master key.")

    result = await db.execute(select(models.User).where(models.User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.password_hash = hash_password(payload.new_password)
    await db.commit()
    return {"status": "success", "message": "Password forcefully reset."}


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

    if user.role == "super_admin" and payload.role != "super_admin":
        admin_count_result = await db.execute(select(models.User.id).where(models.User.role == "super_admin"))
        if len(admin_count_result.all()) <= 1:
            raise HTTPException(status_code=403, detail="Cannot demote the last remaining Super Admin.")

    user.role = payload.role
    await db.commit()
    return {"status": "success", "role": user.role}


class AdminUserCreate(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    role: str = "viewer"


@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(payload: AdminUserCreate, db: AsyncSession = Depends(get_db),
                      admin: models.User = Depends(get_current_admin)):
    if payload.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")
    existing = await db.execute(select(models.User).where(models.User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = models.User(email=payload.email, full_name=payload.full_name, password_hash=hash_password(payload.password),
                       role=payload.role)
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
    if target_user.role == "super_admin" and target_user.id != admin.id:
        raise HTTPException(status_code=403, detail="Security Violation: Cannot delete other Super Admin accounts.")
    if target_user.role == "super_admin":
        admin_count_result = await db.execute(select(models.User.id).where(models.User.role == "super_admin"))
        if len(admin_count_result.all()) <= 1:
            raise HTTPException(status_code=403, detail="Cannot delete the last remaining Super Admin.")
    await db.delete(target_user)
    await db.commit()
    return {"status": "success", "message": "User deleted"}

# Entity Control & Architecture Core
@app.post("/entities/", response_model=schemas.EntityResponse)
async def create_entity(payload: schemas.EntityCreate, db: AsyncSession = Depends(get_db),
                        admin: models.User = Depends(get_current_admin)):
    entity = models.Entity(
        name=payload.name,
        org_type=payload.org_type,
        incorporation_state=payload.incorporation_state,
        headquarters=payload.headquarters,
        naics_code=payload.naics_code
    )
    db.add(entity)
    await db.commit()
    await db.refresh(entity)

    if payload.creation_template == "bookr":
        template = CORE_TASKS
    elif payload.creation_template == "pebble":
        template = PEBBLE_TASKS
    else:
        org = payload.org_type.lower()
        state = payload.incorporation_state.lower()

        if "non-profit" in org:
            template = NON_PROFIT_TASKS
        elif "llc" in org:
            template = GENERAL_LLC_TASKS
        elif state == "delaware":
            template = DELAWARE_CCORP_TASKS
        else:
            template = CA_FOR_PROFIT_TASKS

    for t in template:
        task_data = t.copy()
        task_data["entity_id"] = entity.id
        task_data["entity_name"] = entity.name
        task_data["entity"] = entity.name
        task_data["key"] = f"{task_data.get('key', 'task')}_{entity.id}"
        db.add(models.Task(is_core=True, deleted=False, **task_data))

    await db.commit()
    return entity

@app.post("/entities/{entity_id}/assign")
async def assign_entity_member(entity_id: int, payload: schemas.AssignAdminPayload, db: AsyncSession = Depends(get_db),
                               current_admin: models.User = Depends(get_current_admin)):
    user_res = await db.execute(select(models.User).where(models.User.id == payload.admin_id))
    user = user_res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    entity_res = await db.execute(select(models.Entity).where(models.Entity.id == entity_id))
    entity = entity_res.scalar_one_or_none()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found.")

    existing = await db.execute(select(models.EntityMember).where(
        models.EntityMember.user_id == payload.admin_id, models.EntityMember.entity_id == entity_id
    ))
    if not existing.scalar_one_or_none():
        db.add(models.EntityMember(user_id=payload.admin_id, entity_id=entity_id))
        await db.commit()

    return {"status": "success", "message": "User assigned to entity successfully."}


@app.delete("/entities/{entity_id}/assign/{user_id}")
async def unassign_entity_member(entity_id: int, user_id: int, db: AsyncSession = Depends(get_db),
                                 current_admin: models.User = Depends(get_current_admin)):
    """Removes a user's access to a specific organization without deleting their account."""
    existing = await db.execute(select(models.EntityMember).where(
        models.EntityMember.user_id == user_id, models.EntityMember.entity_id == entity_id
    ))
    member_record = existing.scalar_one_or_none()
    if not member_record:
        raise HTTPException(status_code=404, detail="User is not assigned to this entity.")

    await db.delete(member_record)
    await db.commit()
    return {"status": "success", "message": "Access revoked."}

@app.delete("/entities/{entity_id}")
async def delete_entity(entity_id: int, db: AsyncSession = Depends(get_db),
                        current_admin: models.User = Depends(get_current_admin)):
    #Deletes an entity and cascades to remove all associated tasks and logs
    result = await db.execute(select(models.Entity).where(models.Entity.id == entity_id))
    entity = result.scalar_one_or_none()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found.")

    await db.delete(entity)
    await db.commit()
    return {"status": "success", "message": "Entity and associated records purged."}


@app.get("/entities/", response_model=List[schemas.EntityResponse])
async def list_entities(db: AsyncSession = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    res = await db.execute(select(models.Entity))
    return res.scalars().all()


@app.get("/memberships/")
async def list_memberships(db: AsyncSession = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    """Returns all user-entity assignments to build the Admin mapping table."""
    res = await db.execute(select(models.EntityMember))
    memberships = res.scalars().all()

    # Returns a simple list of dicts for the frontend to parse
    return [{"id": m.id, "user_id": m.user_id, "entity_id": m.entity_id} for m in memberships]


# Tasks & Logs (Protected)
@app.get("/tasks/", response_model=List[schemas.TaskResponse])
async def list_tasks(skip: int = 0, limit: int = 2000, db: AsyncSession = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)):
    if current_user.role == "super_admin":
        query = select(models.Task).where(models.Task.deleted == False)
    else:
        mem_res = await db.execute(
            select(models.EntityMember.entity_id).where(models.EntityMember.user_id == current_user.id))
        allowed_entities = mem_res.scalars().all()
        if not allowed_entities:
            return []
        query = select(models.Task).where(models.Task.deleted == False, models.Task.entity_id.in_(allowed_entities))

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@app.post("/tasks/", response_model=schemas.TaskResponse)
async def create_task(payload: schemas.TaskCreate, db: AsyncSession = Depends(get_db),
                      editor: models.User = Depends(get_current_editor)):
    if payload.entity_id:
        await verify_org_access(db, editor, payload.entity_id)

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
                      editor: models.User = Depends(get_current_editor)):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if task:
        await verify_org_access(db, editor, task.entity_id)
        task.deleted = True
        log_result = await db.execute(select(models.ComplianceLog).where(models.ComplianceLog.task_id == task_id))
        for log in log_result.scalars().all():
            await db.delete(log)
        await db.commit()
    return {"status": "success"}


@app.get("/logs/", response_model=List[schemas.LogResponse])
async def list_logs(task_id: Optional[int] = None, fiscal_year: Optional[int] = None, skip: int = 0, limit: int = 2000,
                    db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = select(models.ComplianceLog).join(models.Task)

    if current_user.role != "super_admin":
        mem_res = await db.execute(
            select(models.EntityMember.entity_id).where(models.EntityMember.user_id == current_user.id))
        allowed_entities = mem_res.scalars().all()
        if not allowed_entities:
            return []
        query = query.where(models.Task.entity_id.in_(allowed_entities))

    if task_id: query = query.where(models.ComplianceLog.task_id == task_id)
    if fiscal_year: query = query.where(models.ComplianceLog.fiscal_year == fiscal_year)
    result = await db.execute(query.order_by(models.ComplianceLog.timestamp.asc()).offset(skip).limit(limit))
    return result.scalars().all()


@app.post("/logs/", response_model=schemas.LogResponse)
async def create_log(payload: schemas.LogCreate, db: AsyncSession = Depends(get_db),
                     editor: models.User = Depends(get_current_editor)):
    task_res = await db.execute(select(models.Task).where(models.Task.id == payload.task_id))
    task = task_res.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await verify_org_access(db, editor, task.entity_id)

    saved_file_path = None
    if payload.file_data and payload.file_data.startswith("data:"):
        try:
            header, encoded = payload.file_data.split(",", 1)
            file_ext = header.split(";")[0].split("/")[1]
            file_bytes = base64.b64decode(encoded)
            filename = f"{uuid.uuid4().hex}.{file_ext}"

            os.makedirs(UPLOADS_DIR, exist_ok=True)
            saved_file_path = f"/uploads/{filename}"

            with open(os.path.join(UPLOADS_DIR, filename), "wb") as f:
                f.write(file_bytes)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid base64 file data payload.")

    log_data = payload.model_dump()
    log_data["file_data"] = saved_file_path

    log = models.ComplianceLog(actor_id=editor.id, **log_data)
    db.add(log)

    try:
        await db.commit()
        await db.refresh(log)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409,
                            detail="A compliance log for this exact task and fiscal year already exists.")

    return log


@app.delete("/logs/{log_id}")
async def delete_log(log_id: int, db: AsyncSession = Depends(get_db),
                     editor: models.User = Depends(get_current_editor)):
    result = await db.execute(select(models.ComplianceLog).where(models.ComplianceLog.id == log_id))
    if log := result.scalar_one_or_none():
        task_res = await db.execute(select(models.Task).where(models.Task.id == log.task_id))
        task = task_res.scalar_one_or_none()
        if task:
            await verify_org_access(db, editor, task.entity_id)
        await db.delete(log)
        await db.commit()
    return {"status": "success"}


@app.delete("/logs/")
async def clear_all_logs(task_id: Optional[int] = None, fiscal_year: Optional[int] = None,
                         db: AsyncSession = Depends(get_db), editor: models.User = Depends(get_current_editor)):
    query = select(models.ComplianceLog)
    if task_id: query = query.where(models.ComplianceLog.task_id == task_id)
    if fiscal_year: query = query.where(models.ComplianceLog.fiscal_year == fiscal_year)
    result = await db.execute(query)
    for log in result.scalars().all():
        task_res = await db.execute(select(models.Task).where(models.Task.id == log.task_id))
        if task := task_res.scalar_one_or_none():
            await verify_org_access(db, editor, task.entity_id)
            await db.delete(log)
    await db.commit()
    return {"status": "success"}


@app.get("/auth/is-initialized")
async def is_initialized(db: AsyncSession = Depends(get_db)):
    # Check if any admin exists in the database
    result = await db.execute(select(models.User).where(models.User.role == "super_admin"))
    admin_exists = result.scalar_one_or_none() is not None
    return {"initialized": admin_exists}


@app.patch("/tasks/{task_id}")
async def update_task(task_id: int, update_data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.due_type = update_data.due_type
    task.due_month = update_data.due_month
    task.due_day = update_data.due_day
    task.due_text = update_data.due_text

    await db.commit()
    return {"status": "success"}