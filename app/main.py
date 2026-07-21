import binascii
import os
import base64
import hmac
import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query, status, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, select, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field
import redis.asyncio as aioredis

logger = logging.getLogger("bookr.compliance")

from app.database import engine, Base, get_db
from app import models, schemas
from app.auth import hash_password, verify_password, create_access_token, get_current_user, ENVIRONMENT

from app.seed_data import (
    STATE_TASKS_MAP,
    CORE_TASKS,
    CA_FOR_PROFIT_TASKS,
    DELAWARE_CCORP_TASKS,
    GENERAL_CORP_TASKS,
    PEBBLE_TASKS,
    NON_PROFIT_TASKS,
    GENERAL_LLC_TASKS
)

VALID_ROLES = ["super_admin", "co_admin", "editor", "viewer"]
ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp"
}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10MB

# Fixed keys for Postgres transaction-scoped advisory locks on global (not
# per-entity) invariants. Arbitrary but must stay stable and distinct from
# any entity_id (entity_id starts at 1 and grows small; these are large and
# won't collide in practice).
_FIRST_USER_LOCK_KEY = 0x4649525354  # "FIRST"
_SUPER_ADMIN_COUNT_LOCK_KEY = 0x53555045524144  # "SUPERAD"


async def _lock_global_invariant(db: AsyncSession, key: int):
    """Transaction-scoped advisory lock for invariants that span the whole `users`
    table (e.g. "at least one super_admin must always exist") rather than a single
    entity — auto-released on commit/rollback. Postgres-only; see _next_task_num."""
    if engine.dialect.name == "postgresql":
        await db.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": key})

redis_client: Optional[aioredis.Redis] = None


def _entities_table_missing_is_restricted(sync_conn) -> bool:
    insp = inspect(sync_conn)
    if "entities" not in insp.get_table_names():
        return False
    columns = {c["name"] for c in insp.get_columns("entities")}
    return "is_restricted" not in columns


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://cache:6379/0")
    try:
        redis_client = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    except Exception as e:
        logger.warning("Redis connection disabled or unreachable: %s", e)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # create_all() only creates missing tables — it never alters an existing
        # one, so a table that predates the `is_restricted` column needs a manual
        # backfill. There's no migration framework wired up in this app, so this
        # is a targeted, idempotent patch rather than a general solution.
        if await conn.run_sync(_entities_table_missing_is_restricted):
            await conn.execute(text("ALTER TABLE entities ADD COLUMN is_restricted BOOLEAN NOT NULL DEFAULT FALSE"))
    yield
    if redis_client:
        await redis_client.close()
    await engine.dispose()


app = FastAPI(title="Bookr Compliance API", version="2.5.0", lifespan=lifespan)

_allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000")
ALLOWED_ORIGINS = [o.strip() for o in _allowed_origins_env.split(",") if o.strip()]

# Browsers (and spec-compliant HTTP clients) silently drop `Secure` cookies over
# plain HTTP. Only require it in production, where the app should sit behind TLS.
COOKIE_SECURE = ENVIRONMENT == "production"

app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


class TaskUpdate(BaseModel):
    due_type: str
    due_month: Optional[int] = Field(None, ge=1, le=12)
    due_day: Optional[int] = Field(None, ge=1, le=31)
    due_text: Optional[str] = None


@app.get("/")
async def serve_dashboard():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


# RBAC & Organizational Verification
async def get_current_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["super_admin", "co_admin"]:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


async def get_current_editor(current_user: models.User = Depends(get_current_user)):
    if current_user.role == "viewer":
        raise HTTPException(status_code=403, detail="Editor write privileges required")
    return current_user


async def verify_org_access(db: AsyncSession, user: models.User, entity_id: int):
    """Ensures the entity exists and the user belongs to it, enforcing hard exclusivity
    on restricted entities. Non-super-admins get the identical error whether the entity
    doesn't exist, is restricted, or just isn't theirs — distinguishing those cases
    would let a caller enumerate entity existence/restricted-status they have no
    business knowing about."""
    entity_res = await db.execute(select(models.Entity).where(models.Entity.id == entity_id))
    entity = entity_res.scalar_one_or_none()

    if user.role == "super_admin":
        if not entity:
            raise HTTPException(status_code=404, detail="Organization entity not found.")
        return True

    if not entity or entity.is_restricted:
        raise HTTPException(status_code=403, detail="Cross-organization security violation blocked.")

    res = await db.execute(select(models.EntityMember).where(
        models.EntityMember.user_id == user.id, models.EntityMember.entity_id == entity_id
    ))
    if not res.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Cross-organization security violation blocked.")
    return True


async def get_admin_entity_ids(db: AsyncSession, admin: models.User) -> set:
    res = await db.execute(select(models.EntityMember.entity_id).where(models.EntityMember.user_id == admin.id))
    return set(res.scalars().all())


async def _next_task_num(db: AsyncSession, entity_id: int) -> int:
    """Atomically computes the next display-order `num` for a new custom task within
    one entity's task list (num is only ever sorted/compared within a single entity's
    own list on the frontend, never globally). Under concurrent task creation for the
    same entity, a plain count-then-insert races; a transaction-scoped Postgres advisory
    lock keyed by entity_id closes that window. SQLite (local dev only) has no
    equivalent — that path is unlocked and accepts the (much rarer, non-fatal) race."""
    if engine.dialect.name == "postgresql":
        await db.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": entity_id})
    count_result = await db.execute(select(models.Task.id).where(models.Task.entity_id == entity_id))
    return len(count_result.all()) + 1


async def verify_shared_org_access(db: AsyncSession, admin: models.User, target_user_id: int):
    if admin.role == "super_admin":
        return True
    admin_entities = await get_admin_entity_ids(db, admin)
    if admin_entities:
        res = await db.execute(select(models.EntityMember.entity_id).where(
            models.EntityMember.user_id == target_user_id, models.EntityMember.entity_id.in_(admin_entities)
        ))
        if res.scalars().first():
            return True
    raise HTTPException(status_code=403, detail="Cross-organization security violation blocked.")


# Auth & User Management
@app.post("/auth/register")
async def register(payload: schemas.UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    # Lock + check "is registration still open" before anything else. This closes two
    # issues at once: (1) an email-enumeration leak — an anonymous caller used to be
    # able to tell "email already exists" (400) apart from "registration closed" (403)
    # even after the system was initialized; checking registration-open first means
    # this endpoint only ever returns the generic "disabled" message once any user
    # exists, and a genuinely-empty DB has no existing emails to collide with anyway.
    # (2) a TOCTOU race — two simultaneous first-ever registrations could otherwise
    # both observe zero users and both become super_admin.
    await _lock_global_invariant(db, _FIRST_USER_LOCK_KEY)

    count_result = await db.execute(select(models.User.id))
    if len(count_result.all()) > 0:
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
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=60 * 24 * 7 * 60
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
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=60 * 24 * 7 * 60
    )
    return {"status": "success", "user": user.email}


@app.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(key="bookr_token", httponly=True, secure=COOKIE_SECURE, samesite="lax")
    return {"status": "success"}


class EmergencyResetPayload(BaseModel):
    email: str
    new_password: str = Field(..., min_length=8)
    master_key: str


_EMERGENCY_RESET_WINDOW_SECONDS = 15 * 60
_EMERGENCY_RESET_MAX_ATTEMPTS = 5


async def _check_emergency_reset_rate_limit(client_ip: str):
    if not redis_client:
        return  # Fallback to unrestricted if Redis is disabled in dev

    key = f"rate_limit:emergency_reset:{client_ip}"
    try:
        current_attempts = await redis_client.get(key)
        if current_attempts and int(current_attempts) >= _EMERGENCY_RESET_MAX_ATTEMPTS:
            raise HTTPException(status_code=429, detail="Too many reset attempts. Try again later.")

        pipe = redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, _EMERGENCY_RESET_WINDOW_SECONDS)
        await pipe.execute()
    except HTTPException:
        raise
    except Exception as e:
        # Fail closed: a Redis outage should not silently disable rate limiting
        # on a master-key-gated endpoint.
        logger.warning("Redis rate limiter error, denying request: %s", e)
        raise HTTPException(status_code=503, detail="Rate limiting temporarily unavailable. Try again shortly.")


@app.post("/auth/emergency-reset")
async def emergency_password_reset(payload: EmergencyResetPayload, request: Request,
                                   db: AsyncSession = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    await _check_emergency_reset_rate_limit(client_ip)

    expected_key = os.getenv("MASTER_RESET_KEY")
    if not expected_key or not hmac.compare_digest(payload.master_key, expected_key):
        logger.warning("Emergency reset: invalid master key attempt from %s for %s", client_ip, payload.email)
        raise HTTPException(status_code=403, detail="Invalid or disabled master key.")

    result = await db.execute(select(models.User).where(models.User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user:
        logger.warning("Emergency reset: valid key, unknown email %s from %s", payload.email, client_ip)
        raise HTTPException(status_code=400, detail="Reset could not be completed.")

    user.password_hash = hash_password(payload.new_password)
    await db.commit()
    logger.warning("Emergency reset: password forcefully reset for %s from %s", payload.email, client_ip)
    return {"status": "success", "message": "Password forcefully reset."}


@app.get("/auth/me", response_model=schemas.UserResponse)
async def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/users/", response_model=List[schemas.UserResponse])
async def list_users(db: AsyncSession = Depends(get_db), admin: models.User = Depends(get_current_admin)):
    if admin.role == "super_admin":
        result = await db.execute(select(models.User))
        return result.scalars().all()

    admin_entities = await get_admin_entity_ids(db, admin)
    if not admin_entities:
        return []
    user_ids_res = await db.execute(
        select(models.EntityMember.user_id).where(models.EntityMember.entity_id.in_(admin_entities)).distinct()
    )
    result = await db.execute(select(models.User).where(models.User.id.in_(user_ids_res.scalars().all())))
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

    if (payload.role == "super_admin" or user.role == "super_admin") and admin.role != "super_admin":
        raise HTTPException(status_code=403, detail="Only Super Admins can grant or revoke Super Admin privileges.")

    if user.role == "super_admin" and payload.role != "super_admin":
        # Lock before counting: two concurrent demotes of two different super_admins
        # could otherwise both read count=2 and both pass, leaving zero.
        await _lock_global_invariant(db, _SUPER_ADMIN_COUNT_LOCK_KEY)
        admin_count_result = await db.execute(select(models.User.id).where(models.User.role == "super_admin"))
        if len(admin_count_result.all()) <= 1:
            raise HTTPException(status_code=403, detail="Cannot demote the last remaining Super Admin.")

    await verify_shared_org_access(db, admin, user.id)

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
    if payload.role == "super_admin" and admin.role != "super_admin":
        raise HTTPException(status_code=403, detail="Only Super Admins can create Super Admin accounts.")
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
        await _lock_global_invariant(db, _SUPER_ADMIN_COUNT_LOCK_KEY)
        admin_count_result = await db.execute(select(models.User.id).where(models.User.role == "super_admin"))
        if len(admin_count_result.all()) <= 1:
            raise HTTPException(status_code=403, detail="Cannot delete the last remaining Super Admin.")

    await verify_shared_org_access(db, admin, target_user.id)

    await db.delete(target_user)
    await db.commit()
    return {"status": "success", "message": "User deleted"}


# Entity Control & Architecture Core
@app.post("/entities/", response_model=schemas.EntityResponse)
async def create_entity(payload: schemas.EntityCreate, db: AsyncSession = Depends(get_db),
                        admin: models.User = Depends(get_current_admin)):
    # Auto-flag primary Bookr entities as restricted
    is_restricted = payload.is_restricted or (payload.creation_template == "bookr")

    entity = models.Entity(
        name=payload.name,
        org_type=payload.org_type,
        incorporation_state=payload.incorporation_state.value,
        headquarters=payload.headquarters,
        naics_code=payload.naics_code,
        is_restricted=is_restricted
    )
    db.add(entity)
    await db.flush()  # assigns entity.id without committing — the whole entity
                       # (row + seeded tasks + co_admin membership) commits as one
                       # transaction below, so a failure partway through rolls back
                       # cleanly instead of leaving an entity with zero tasks or a
                       # co_admin unable to see the org they just created.

    if payload.creation_template == "bookr":
        template = list(CORE_TASKS)
    elif payload.creation_template == "pebble":
        template = list(PEBBLE_TASKS)
    else:
        org = payload.org_type.lower()
        state = payload.incorporation_state.value

        if "non-profit" in org:
            template = list(NON_PROFIT_TASKS)
        elif "llc" in org:
            template = list(GENERAL_LLC_TASKS)
        elif "corp" in org and state == "Delaware":
            template = list(DELAWARE_CCORP_TASKS)
        elif "corp" in org and state == "California":
            template = list(CA_FOR_PROFIT_TASKS)
        elif "corp" in org:
            template = list(GENERAL_CORP_TASKS)
        else:
            # Generic fallback for an org_type that matched none of the substrings
            # above (e.g. "Partnership", "Trust", or free text from a direct API
            # call) — CORE_TASKS is not a generic template, it's Bookr's own
            # internal checklist (vendor-specific tasks like Sterling HSA/Anthem),
            # so an unrelated org must not land there.
            template = list(GENERAL_CORP_TASKS)

    # "bookr"/"pebble" already encode their own state-specific tasks (e.g. bk_si550,
    # peb_soi) — layering STATE_TASKS_MAP on top of them would duplicate those.
    selected_state = payload.incorporation_state.value
    if payload.creation_template not in ("bookr", "pebble") and selected_state in STATE_TASKS_MAP:
        template.extend(STATE_TASKS_MAP[selected_state])

    for t in template:
        task_data = t.copy()
        task_data["entity_id"] = entity.id
        task_data["entity_name"] = entity.name
        task_data["entity"] = entity.name
        task_data["key"] = f"{task_data.get('key', 'task')}_{entity.id}_{uuid.uuid4().hex}"
        db.add(models.Task(is_core=True, deleted=False, **task_data))

    if admin.role == "co_admin":
        db.add(models.EntityMember(user_id=admin.id, entity_id=entity.id))

    await db.commit()
    await db.refresh(entity)
    return entity


@app.post("/entities/{entity_id}/assign")
async def assign_entity_member(entity_id: int, payload: schemas.AssignAdminPayload, db: AsyncSession = Depends(get_db),
                               current_admin: models.User = Depends(get_current_admin)):
    # Check org access before anything else — an existence check on entity_id run
    # ahead of this would leak entity existence to a caller who has no access to it.
    await verify_org_access(db, current_admin, entity_id)

    user_res = await db.execute(select(models.User).where(models.User.id == payload.admin_id))
    user = user_res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

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
    await verify_org_access(db, current_admin, entity_id)

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
    # verify_org_access confirms existence + access together — checking existence
    # separately first would leak entity existence to a caller who has no access.
    await verify_org_access(db, current_admin, entity_id)

    result = await db.execute(select(models.Entity).where(models.Entity.id == entity_id))
    entity = result.scalar_one_or_none()

    await db.delete(entity)
    await db.commit()
    return {"status": "success", "message": "Entity and associated records purged."}


@app.get("/entities/", response_model=List[schemas.EntityResponse])
async def list_entities(db: AsyncSession = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    if current_admin.role == "super_admin":
        res = await db.execute(select(models.Entity))
        return res.scalars().all()

    admin_entities = await get_admin_entity_ids(db, current_admin)
    if not admin_entities:
        return []
    res = await db.execute(select(models.Entity).where(
        models.Entity.id.in_(admin_entities), models.Entity.is_restricted == False
    ))
    return res.scalars().all()


@app.get("/memberships/")
async def list_memberships(db: AsyncSession = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    query = select(models.EntityMember)

    if current_admin.role != "super_admin":
        admin_entities = await get_admin_entity_ids(db, current_admin)
        if not admin_entities:
            return []
        query = query.where(models.EntityMember.entity_id.in_(admin_entities))

    res = await db.execute(query)
    memberships = res.scalars().all()
    return [{"id": m.id, "user_id": m.user_id, "entity_id": m.entity_id} for m in memberships]


# Tasks & Logs
@app.get("/tasks/", response_model=List[schemas.TaskResponse])
async def list_tasks(skip: int = Query(0, ge=0), limit: int = Query(2000, ge=1, le=5000),
                     db: AsyncSession = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)):
    if current_user.role == "super_admin":
        query = select(models.Task).where(models.Task.deleted == False)
    else:
        mem_res = await db.execute(
            select(models.EntityMember.entity_id).where(models.EntityMember.user_id == current_user.id))
        allowed_entities = mem_res.scalars().all()

        # Dynamic Security Check: Exclude all restricted entities from non-super_admins
        restr_res = await db.execute(select(models.Entity.id).where(models.Entity.is_restricted == True))
        restricted_ids = set(restr_res.scalars().all())

        allowed_entities = [e_id for e_id in allowed_entities if e_id not in restricted_ids]

        if not allowed_entities:
            return []

        query = select(models.Task).where(models.Task.deleted == False, models.Task.entity_id.in_(allowed_entities))

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@app.post("/tasks/", response_model=schemas.TaskResponse)
async def create_task(payload: schemas.TaskCreate, db: AsyncSession = Depends(get_db),
                      editor: models.User = Depends(get_current_editor)):
    if not payload.entity_id:
        raise HTTPException(status_code=400, detail="Entity assignment is mandatory.")

    await verify_org_access(db, editor, payload.entity_id)

    # Derive entity_name/entity from the real entity instead of trusting whatever
    # the client sent in the payload — otherwise a task with entity_id=5 could be
    # stored with an unrelated entity_name, since only entity_id is actually used
    # for authorization/scoping.
    entity_name = (await db.execute(
        select(models.Entity.name).where(models.Entity.id == payload.entity_id)
    )).scalar_one()

    key = f"cust_{uuid.uuid4().hex}"
    next_num = await _next_task_num(db, payload.entity_id)
    task_data = payload.model_dump()
    task_data["entity_name"] = entity_name
    task_data["entity"] = entity_name
    task = models.Task(key=key, is_core=False, deleted=False, num=next_num, created_by=editor.id,
                       **task_data)
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
async def list_logs(task_id: Optional[int] = None, fiscal_year: Optional[int] = None,
                    skip: int = Query(0, ge=0), limit: int = Query(2000, ge=1, le=5000),
                    db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = select(models.ComplianceLog).join(models.Task)

    if current_user.role != "super_admin":
        mem_res = await db.execute(
            select(models.EntityMember.entity_id).where(models.EntityMember.user_id == current_user.id))
        allowed_entities = mem_res.scalars().all()

        restr_res = await db.execute(select(models.Entity.id).where(models.Entity.is_restricted == True))
        restricted_ids = set(restr_res.scalars().all())

        allowed_entities = [e_id for e_id in allowed_entities if e_id not in restricted_ids]

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
    if payload.file_data:
        # Reject anything that isn't a fresh upload rather than silently dropping it
        # (there's no "resubmit a previously-saved path" flow, so any other value is
        # either a mistake or an attempt to store an arbitrary client-controlled string).
        if not payload.file_data.startswith("data:"):
            raise HTTPException(status_code=400, detail="file_data must be a base64 data: URI.")

        try:
            header, encoded = payload.file_data.split(",", 1)
            mime_type = header.split(";")[0].split(":")[1].lower()

            if mime_type not in ALLOWED_MIME_TYPES:
                raise HTTPException(status_code=400, detail="Invalid file type. Allowed formats: PDF, JPG, PNG, WEBP.")

            # Base64 inflates size by ~4/3 — check the encoded length before decoding
            # so an oversized payload isn't fully materialized in memory first.
            if len(encoded) > MAX_UPLOAD_BYTES * 4 // 3:
                raise HTTPException(status_code=400, detail="File too large (max 10MB).")

            file_ext = ALLOWED_MIME_TYPES[mime_type]
            file_bytes = base64.b64decode(encoded)
        except HTTPException:
            raise
        except (binascii.Error, ValueError, IndexError):
            raise HTTPException(status_code=400, detail="Invalid base64 file payload.")

        # Outside the parsing try/except: a disk I/O failure here is a genuine server
        # error (500), not a client input mistake, so it shouldn't be mislabeled 400.
        filename = f"{uuid.uuid4().hex}{file_ext}"
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        with open(os.path.join(UPLOADS_DIR, filename), "wb") as f:
            f.write(file_bytes)
        saved_file_path = f"/uploads/{filename}"

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
            try:
                await verify_org_access(db, editor, task.entity_id)
            except HTTPException:
                # Skip logs the caller can't access instead of aborting the whole
                # bulk clear — an unfiltered call previously died on the first log
                # belonging to another org.
                continue
            await db.delete(log)
    await db.commit()
    return {"status": "success"}


@app.get("/auth/is-initialized")
async def is_initialized(db: AsyncSession = Depends(get_db)):
    # limit(1): multiple super_admins is a normal, supported state (see the
    # "last remaining Super Admin" checks elsewhere) — scalar_one_or_none()
    # without it throws MultipleResultsFound once a second one exists.
    result = await db.execute(select(models.User.id).where(models.User.role == "super_admin").limit(1))
    admin_exists = result.scalar_one_or_none() is not None
    return {"initialized": admin_exists}


@app.patch("/tasks/{task_id}")
async def update_task(task_id: int, update_data: TaskUpdate, db: AsyncSession = Depends(get_db),
                      editor: models.User = Depends(get_current_editor)):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await verify_org_access(db, editor, task.entity_id)

    task.due_type = update_data.due_type
    task.due_month = update_data.due_month
    task.due_day = update_data.due_day
    task.due_text = update_data.due_text

    await db.commit()
    return {"status": "success"}